import datetime
import time
from random import randrange
import binascii

from nanohttp import settings, HttpConflict
from restfulpy.orm import DeclarativeBase, OrderingMixin, FilteringMixin, PaginationMixin, ModifiedMixin, \
    ActivationMixin, Field
from sqlalchemy import Integer, Unicode, ForeignKey, Date, Binary, UniqueConstraint, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from wolf import cryptoutil
from oathpy import MacBasedOneTimePassword, TimeBasedOneTimePassword, MacBasedChallengeResponse, \
    TimeBasedChallengeResponse, OCRASuite, totp_checksum, split_seed
from wolf.excpetions import LockedTokenError, DeactivatedTokenError


class DuplicateSeedError(Exception):
    pass


class Token(ActivationMixin, ModifiedMixin, PaginationMixin, FilteringMixin, OrderingMixin, DeclarativeBase):
    __tablename__ = 'token'

    id = Field(Integer, primary_key=True)
    name = Field(Unicode(50), min_length=1)

    provider_reference = Field(Integer, index=True, default=0)
    client_reference = Field(Integer, index=True)

    # The final seed is the concat of seed_head and seed_body. Why?! Because we want to make sure the final seed is
    # always unique. The smallest required seed length is for SHA-1 (20 bytes), so if we make it unique, we can
    # make sure the seed is unique with any hash type.
    _seed_head = Field('seed_head', Binary(20), unique=True, protected=True)
    _seed_body = Field('seed_body', Binary(44), protected=True)

    counter = Field(Integer, default=0, protected=True)

    # Cryptomodule
    cryptomodule_id = Field(Integer, ForeignKey('cryptomodule.id'), protected=True)
    cryptomodule = relationship(
        'Cryptomodule',
        foreign_keys=[cryptomodule_id],
        uselist=False
    )

    expire_date = Field(Date)

    consecutive_tries = Field(Integer, default=0, protected=True)

    __table_args__ = (
        UniqueConstraint(
            name, client_reference, provider_reference, cryptomodule_id,
            name='uix_name_client_reference_provider_reference_cryptomodule_id'
        ),
    )

    @property
    def seed(self):
        return self._seed_head + self._seed_body

    @seed.setter
    def seed(self, seed):
        if len(seed) != 64:
            raise ValueError('Invalid length')

        self._seed_head = seed[:20]
        self._seed_body = seed[20:]

    @hybrid_property
    def is_locked(self):
        return self.consecutive_tries >= settings.token.max_consecutive_tries

    # noinspection PyUnresolvedReferences
    @is_locked.expression
    def is_locked(self):
        return self.consecutive_tries >= settings.token.max_consecutive_tries

    @hybrid_property
    def is_expired(self):
        return (self.expire_date is not None) and (time.mktime(self.expire_date.timetuple()) <= time.time())

    # noinspection PyUnresolvedReferences
    @is_expired.expression
    def is_expired(self):
        return and_(self.expire_date.isnot(None), self.expire_date <= datetime.datetime.now())

    def initialize_seed(self, session):
        current_seed_head = self._seed_head

        for i in range(settings.token.seed.max_random_try):
            try:
                new_seed_head = cryptoutil.random(20)

                # Check whether it has changed or not
                if current_seed_head == new_seed_head:
                    raise DuplicateSeedError()

                self._seed_head = new_seed_head

                # Check whether it is unique or not
                try:
                    session.flush()
                except IntegrityError:
                    # TODO: Perhaps its not required.
                    session.rollback()
                    raise DuplicateSeedError()

                # Everything is OK, choose a seed_body and leave
                self._seed_body = cryptoutil.random(44)
                return

            except DuplicateSeedError:
                if i < settings.token.seed.max_random_try - 1:
                    sleep_millis = randrange(settings.token.seed.min_sleep_millis, settings.token.seed.max_sleep_millis)
                    time.sleep(sleep_millis / 1000)

        # Oh my god, this is impossible !!!
        self._seed_head = current_seed_head
        raise HttpConflict(info='We could not initialize token for you!', reason='token-initialization-error')

    @property
    def ocra_suite(self):
        if not self.cryptomodule:
            return None

        return str(OCRASuite(
            counter_type=self.cryptomodule.counter_type,
            length=self.cryptomodule.challenge_response_length,
            hash_algorithm=self.cryptomodule.hash_algorithm,
            time_interval=self.cryptomodule.time_interval if self.cryptomodule.counter_type == 'time' else None,
        ))

    def to_dict(self):
        result = super().to_dict()
        result['ocraSuite'] = self.ocra_suite
        result['provisioning'] = None
        return result

    def create_one_time_password_algorithm(self):
        if self.cryptomodule.counter_type == 'counter':
            return MacBasedOneTimePassword(
                self.cryptomodule.hash_algorithm,
                self.seed,
                self.cryptomodule.one_time_password_length,
                self.counter,
            )
        else:
            return TimeBasedOneTimePassword(
                self.cryptomodule.hash_algorithm,
                self.seed,
                self.cryptomodule.one_time_password_length,
                self.cryptomodule.time_interval,
            )

    def create_challenge_response_algorithm(self):
        if self.cryptomodule.counter_type == 'counter':
            return MacBasedChallengeResponse(
                self.ocra_suite,
                self.seed,
                self.counter,
            )
        else:
            return TimeBasedChallengeResponse(
                self.ocra_suite,
                self.seed,
            )

    def provision(self, secret):
        if not self.is_active:
            raise DeactivatedTokenError()
        if self.is_locked:
            raise LockedTokenError()
        encrypted_seed = cryptoutil.aes_encrypt(split_seed(self.seed, self.cryptomodule.hash_algorithm), secret)
        hexstring_seed = binascii.hexlify(encrypted_seed).decode()
        algorithm = 'totp' if self.cryptomodule.counter_type == 'time' else 'hotp'
        cryptomodule_id = str(self.cryptomodule_id).zfill(2)
        expire_date = self.expire_date.strftime('%y%m%d')
        token_string = f'{self.name}{hexstring_seed}{cryptomodule_id}{expire_date}'.upper()
        return f'mt://oath/{algorithm}/{token_string}{totp_checksum(token_string.encode())}'
