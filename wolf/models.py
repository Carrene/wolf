import binascii
import time
from datetime import date

import redis
from nanohttp import settings
from oathcy.otp import TOTP
from restfulpy.orm import DeclarativeBase, ModifiedMixin, FilteringMixin, \
    PaginationMixin, DeactivationMixin, Field, DBSession, OrderingMixin
from sqlalchemy import Integer, Unicode, ForeignKey, Date, Binary, \
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
        if cache:
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
        if self.last_code == code:
            self.same_code_verify_counter += 1
            if settings.token.verify_limit < self.same_code_verify_counter:
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

    def cache(self):
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
    def load_from_cache(cls, token_id):
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
    def invalidate(cls, token_id):
        cls.redis().delete(token_id)

    @classmethod
    def after_update(cls, mapper, connection, target):
        if settings.token.redis.enabled:
            cls.invalidate(target.id)


event.listen(Token, 'after_update', MiniToken.after_update)

