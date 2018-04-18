import time
import binascii
from random import randrange
from datetime import date

import oathcy
from oathpy import TimeBasedOneTimePassword, TimeBasedChallengeResponse, OCRASuite, totp_checksum
from nanohttp import settings, HttpConflict
from restfulpy.orm import DeclarativeBase, ModifiedMixin, FilteringMixin, PaginationMixin, ActivationMixin, Field, \
    DBSession, OrderingMixin
from sqlalchemy import Integer, Unicode, ForeignKey, Date, Binary, UniqueConstraint, BigInteger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from wolf import cryptoutil


class DuplicateSeedError(Exception):
    pass


class Token(ModifiedMixin, PaginationMixin, FilteringMixin, ActivationMixin, OrderingMixin, DeclarativeBase):
    __tablename__ = 'token'

    id = Field(Integer, primary_key=True)
    name = Field(Unicode(50), min_length=1)
    phone = Field(BigInteger, index=True)
    seed = Field(Binary(20), unique=True, protected=True)

    # Cryptomodule
    cryptomodule_id = Field(Integer, ForeignKey('cryptomodule.id'), protected=True)
    cryptomodule = relationship(
        'Cryptomodule',
        foreign_keys=[cryptomodule_id],
        uselist=False,
    )

    expire_date = Field(Date)
    consecutive_tries = Field(Integer, default=0, protected=True)

    __table_args__ = (
        UniqueConstraint(
            name, phone, cryptomodule_id,
            name='uix_name_phone_cryptomodule_id'
        ),
    )

    @hybrid_property
    def is_locked(self):
        return self.consecutive_tries >= settings.token.max_consecutive_tries

    @hybrid_property
    def is_expired(self):
        return self.expire_date <= date.today()

    def initialize_seed(self, session=DBSession):
        current_seed = self.seed

        for i in range(settings.token.seed.max_random_try):
            try:
                new_seed = cryptoutil.random(20)

                # Check whether it has changed or not
                if current_seed == new_seed:
                    raise DuplicateSeedError()

                self.seed = new_seed

                # Check whether it is unique or not
                try:
                    session.flush()
                except IntegrityError:
                    # TODO: Perhaps its not required.
                    session.rollback()
                    raise DuplicateSeedError()

                # Everything is OK, terminating
                return

            except DuplicateSeedError:
                if i < settings.token.seed.max_random_try - 1:
                    sleep_millis = randrange(
                        settings.token.seed.min_sleep_milliseconds, settings.token.seed.max_sleep_milliseconds
                    )
                    time.sleep(sleep_millis / 1000)

        # Oh my god, this is impossible !!!
        self.seed = current_seed
        raise HttpConflict(info='We could not initialize token for you!', reason='token-initialization-error')

    @property
    def ocra_suite(self):
        if not self.cryptomodule:
            return None

        return str(OCRASuite(
            'time',
            self.cryptomodule.challenge_response_length,
            'SHA-1',
            time_interval=self.cryptomodule.time_interval
        ))

    def to_dict(self):
        result = super().to_dict()
        result['ocraSuite'] = self.ocra_suite
        result['provisioning'] = None
        return result

    def verify_totp(self, otp):
        return oathcy.totp_verify(
            self.seed,
            time.time(),
            settings.oath.window,
            otp,
            self.cryptomodule.time_interval
        )

    def create_one_time_password_algorithm(self):
        return TimeBasedOneTimePassword(
            'SHA-1',
            self.seed,
            self.cryptomodule.one_time_password_length,
            self.cryptomodule.time_interval,
        )

    def create_challenge_response_algorithm(self):
        return TimeBasedChallengeResponse(
            self.ocra_suite,
            self.seed,
        )

    def provision(self, secret):
        encrypted_seed = cryptoutil.aes_encrypt(self.seed, secret)
        hexstring_seed = binascii.hexlify(encrypted_seed).decode()
        cryptomodule_id = str(self.cryptomodule_id).zfill(2)
        expire_date = self.expire_date.strftime('%y%m%d')
        token_string = f'{self.name}{hexstring_seed}{cryptomodule_id}{expire_date}'.upper()
        return f'mt://oath/totp/{token_string}{totp_checksum(token_string.encode())}'
