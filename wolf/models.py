import binascii
import time
from datetime import date
from random import randrange

from nanohttp import settings, HTTPConflict
from restfulpy.cryptography import AESCipher
from restfulpy.orm import DeclarativeBase, ModifiedMixin, FilteringMixin, \
    PaginationMixin, DeactivationMixin, Field, DBSession, OrderingMixin
from sqlalchemy import Integer, Unicode, ForeignKey, Date, Binary, \
    UniqueConstraint, BigInteger
from sqlalchemy.orm import relationship

from wolf import cryptoutil
from .backends import LionClient


class Cryptomodule(DeclarativeBase):
    __tablename__ = 'cryptomodule'

    id = Field(Integer, primary_key=True)
    time_interval = Field(Integer, default=60)
    one_time_password_length = Field(Integer, default=4)


class Token(ModifiedMixin, PaginationMixin, FilteringMixin, DeactivationMixin,
            OrderingMixin, DeclarativeBase):
    __tablename__ = 'token'

    id = Field(Integer, primary_key=True)
    name = Field(Unicode(50), min_length=1)
    phone = Field(BigInteger, index=True)
    seed = Field(Binary(20), unique=True, protected=True)

    # Cryptomodule
    cryptomodule_id = Field(
        Integer,
        ForeignKey('cryptomodule.id'),
        protected=True
    )
    cryptomodule = relationship(
        'Cryptomodule',
        foreign_keys=[cryptomodule_id],
        uselist=False,
    )

    expire_date = Field(Date)

    __table_args__ = (
        UniqueConstraint(
            name,
            phone,
            cryptomodule_id,
            name='uix_name_phone_cryptomodule_id'
        ),
    )

    @property
    def is_expired(self):
        return self.expire_date <= date.today()

    def initialize_seed(self):
        self.seed = cryptoutil.random(20)

    def to_dict(self):
        result = super().to_dict()
        result['provisioning'] = None
        return result

    def provision(self, phone):
        encrypted_seed = LionClient().encrypt(phone, self.seed)
        hexstring_seed = binascii.hexlify(encrypted_seed).decode()
        cryptomodule_id = str(self.cryptomodule_id).zfill(2)
        expire_date = self.expire_date.strftime('%y%m%d')
        token_string = \
            f'{self.name}{hexstring_seed}{cryptomodule_id}{expire_date}' \
            .upper()
        checksum = LionClient().checksum(phone, token_string)
        return f'mt://oath/totp/{token_string}{checksum}'

