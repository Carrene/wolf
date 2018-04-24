import binascii
import time
from datetime import date
from random import randrange

from nanohttp import settings, HttpConflict
from restfulpy.cryptography import AESCipher
from restfulpy.orm import DeclarativeBase, ModifiedMixin, FilteringMixin, PaginationMixin, \
    ActivationMixin, Field, DBSession, OrderingMixin
from sqlalchemy import Integer, Unicode, ForeignKey, Date, Binary, UniqueConstraint, BigInteger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates

from .. import cryptoutil


class DuplicateSeedError(Exception):
    pass


class Cryptomodule(DeclarativeBase):
    __tablename__ = 'cryptomodule'

    id = Field(Integer, primary_key=True)
    time_interval = Field(Integer, default=60)
    one_time_password_length = Field(Integer, default=4)

    @validates('time_interval')
    def validate_time_interval(self, key, new_value):
        if new_value == 0:
            raise ValueError('Time interval should not be zero')
        elif 60 <= new_value <= 59 * 60 and new_value % 60 != 0:
            raise ValueError('60 <= time_interval <= 59 * 60 and time_interval % 60 != 0')
        elif 60 * 60 <= new_value <= (48 * 60 * 60) and new_value % (60 * 60) != 0:
            raise ValueError('60 <= time_interval <= 59 * 60 and time_interval % 60 != 0')
        return new_value

    @validates('one_time_password_length')
    def validate_one_time_password(self, key, new_value):
        new_value = int(new_value)
        if not 4 <= new_value <= 10:
            raise ValueError('Length should be between 4 and 10')
        return new_value


class BaseToken:
    @hybrid_property
    def is_expired(self):
        return self.expire_date <= date.today()


class Token(BaseToken, ModifiedMixin, PaginationMixin, FilteringMixin, ActivationMixin, OrderingMixin, DeclarativeBase):
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

    __table_args__ = (
        UniqueConstraint(
            name, phone, cryptomodule_id,
            name='uix_name_phone_cryptomodule_id'
        ),
    )

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

    def to_dict(self):
        result = super().to_dict()
        result['provisioning'] = None
        return result

    def provision(self, secret):
        encrypted_seed = AESCipher(secret, random=cryptoutil.random).encrypt(self.seed)
        hexstring_seed = binascii.hexlify(encrypted_seed).decode()
        cryptomodule_id = str(self.cryptomodule_id).zfill(2)
        expire_date = self.expire_date.strftime('%y%m%d')
        token_string = f'{self.name}{hexstring_seed}{cryptomodule_id}{expire_date}'.upper()
        return f'mt://oath/totp/{token_string}{cryptoutil.totp_checksum(token_string.encode())}'

