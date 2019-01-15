import time
import struct
import binascii
from datetime import date

import redis
from nanohttp import settings
from oathcy.otp import TOTP
from restfulpy.orm import DeclarativeBase, ModifiedMixin, FilteringMixin, \
    PaginationMixin, DeactivationMixin, Field, DBSession, OrderingMixin
from sqlalchemy import Integer, Unicode, ForeignKey, Date, LargeBinary, \
    UniqueConstraint, BigInteger, event, extract, text
from sqlalchemy.orm import relationship

from .backends import LionClient
from wolf import cryptoutil


class Cryptomodule(DeclarativeBase):
    __tablename__ = 'cryptomodule'

    id = Field(Integer, primary_key=True)
    time_interval = Field(Integer, default=60)
    one_time_password_length = Field(Integer, default=4)


class Token(ModifiedMixin, PaginationMixin, FilteringMixin, DeactivationMixin,
            OrderingMixin, DeclarativeBase):
    __tablename__ = 'token'

    id = Field(Integer, primary_key=True)
    name = Field(
        Unicode(50),
        required='703 name is required',
        min_length=(
            6,
            '702 Name length should be between 6 and 50 characters'
        ),
        max_length=(
            50,
            '702 Name length should be between 6 and 50 characters'
        ),
        not_none='709 Name cannot be null',
        python_type=str
    )
    phone = Field(
        BigInteger,
        index=True,
        required='704 phone is required',
        not_none='704 phone is required',
        python_type=(int, '705 phone should be Integer'),
    )
    seed = Field(LargeBinary(20), unique=True, protected=True)

    cryptomodule_id = Field(
        Integer,
        ForeignKey('cryptomodule.id'),
        protected=True,
        not_none=True,
        required='706 cryptomoduleId is required',
        python_type=(int, '701 CryptomoduleId must be Integer')
    )

    cryptomodule = relationship(
        'Cryptomodule',
        foreign_keys=[cryptomodule_id],
        uselist=False,
    )

    expire_date = Field(
        Date,
        required='707 expireDate is required',
        python_type=(float, '708 expireDate should be Integer or Float'),
        not_none=True
    )

    bank_id = Field(
        Integer,
        required='709 bankId is required',
        not_none='709 bankId is required',
        python_type=(int, '710 BankId must be Integer')
    )


    __table_args__ = (
        UniqueConstraint(
            name,
            phone,
            cryptomodule_id,
            bank_id,
            name='uix_name_phone_cryptomodule_id_bank_id'
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
        """
        version+seed+expdate+cryptomoduleid+name+bankid
        """
        expire_date = self.expire_date.strftime('%y%m%d')
        binary = struct.pack(
            '!BIBBBB',
            1,                      # Version
            int(expire_date),
            self.cryptomodule_id,
            self.cryptomodule.one_time_password_length,
            self.cryptomodule.time_interval,
            self.bank_id,
        )
        binary += self.seed
        binary += self.name.encode()

        encrypted_binary = LionClient().encrypt(phone, binary, checksum=4)
        hexstring = binascii.hexlify(encrypted_binary).decode()
        return f'mt://oath/totp/{hexstring}'


cached_cryptomodules = None


class MiniToken:
    _redis = None

    def __init__(self, id, seed, expire_date, is_active, cryptomodule_id,
                 last_code=None, same_code_verify_counter=0):
        self.id = id
        self.seed = seed
        self.expire_date = expire_date
        self.is_active = is_active
        self.cryptomodule_id = cryptomodule_id
        self.last_code = last_code
        self.same_code_verify_counter = same_code_verify_counter

    @staticmethod
    def create_blocking_redis_client():
        return redis.StrictRedis(
            host=settings.token.redis.host,
            port=settings.token.redis.port,
            db=settings.token.redis.db,
            password=settings.token.redis.password,
            max_connections=settings.token.redis.max_connections,
            socket_timeout=settings.token.redis.socket_timeout
        )

    @classmethod
    def redis(cls):
        if cls._redis is None:
            cls._redis = cls.create_blocking_redis_client()
        return cls._redis

    @classmethod
    def load_from_database(cls, token_id):
        row = DBSession.query(
            Token.id,
            Token.seed,
            extract('epoch', Token.expire_date),
            Token.activated_at.isnot(None),
            Token.cryptomodule_id,
        ).filter(Token.id == token_id).one_or_none()
        return cls(*row) if row else None

    @classmethod
    def load(cls, token_id, cache=False):
        if cache:  # pragma: no cover
            token = cls.load_from_cache(token_id)
            if token is not None:
                return token
        return cls.load_from_database(token_id)

    @property
    def is_expired(self):
        return self.expire_date <= time.time()

    @property
    def cryptomodules(self):
        global cached_cryptomodules
        if cached_cryptomodules is None:
            modules = {}
            for m in DBSession.execute(text(
                'SELECT id, time_interval, one_time_password_length '
                'FROM cryptomodule'
            )):
                modules[m[0]] = m
            cached_cryptomodules = modules
        return cached_cryptomodules

    @property
    def cryptomodule(self):
        return self.cryptomodules[self.cryptomodule_id]

    @property
    def time_interval(self):
        return self.cryptomodule[1]

    @property
    def length(self):
        return self.cryptomodule[2]

    def verify(self, code, window):
        if self.last_code == code:  # pragma: no cover
            self.same_code_verify_counter += 1
            if settings.token.verify_limit <= self.same_code_verify_counter:
                return False
        else:
            self.last_code = code
            self.same_code_verify_counter = 0

        pinblock = cryptoutil.EncryptedISOPinBlock(self.id)
        otp = pinblock.decode(code)
        return TOTP(
            self.seed,
            time.time(),
            self.length,
            step=self.time_interval
        ).verify(otp, window)

    def cache(self):  # pragma: no cover
        self.redis().set(
            str(self.id),
            b'%s,%d,%d,%d,%s,%d' % (
                binascii.hexlify(self.seed),
                int(self.expire_date),
                int(self.is_active),
                self.cryptomodule_id,
                self.last_code,
                self.same_code_verify_counter
            )
        )

    @classmethod
    def load_from_cache(cls, token_id):  # pragma: no cover
        cache_key = str(token_id)
        redis = cls.redis()
        if redis.exists(cache_key):
            token = redis.get(cache_key).split(b',')
            return cls(
                token_id,
                binascii.unhexlify(token[0]),
                float(token[1]),
                bool(token[2]),
                int(token[3]),
                token[4],
                int(token[5])
            ) if token else None
        return None

    @classmethod
    def invalidate(cls, token_id):  # pragma: no cover
        cls.redis().delete(token_id)

    @classmethod
    def after_update(cls, mapper, connection, target):  # pragma: no cover
        if settings.token.redis.enabled:
            cls.invalidate(target.id)


event.listen(Token, 'after_update', MiniToken.after_update)

