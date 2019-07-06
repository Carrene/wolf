import time
import struct
import binascii
import pickle
import uuid
from datetime import date
from collections import deque

import redis
from nanohttp import settings
from oathcy.otp import TOTP
from restfulpy.orm import DeclarativeBase, ModifiedMixin, FilteringMixin, \
    PaginationMixin, DeactivationMixin, Field, DBSession, OrderingMixin, \
    TimestampMixin
from sqlalchemy import Integer, Unicode, ForeignKey, Date, LargeBinary, \
    UniqueConstraint, BigInteger, event, extract, text, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.session import object_session

from .backends import LionClient
from . import cryptoutil
from .exceptions import DuplicateSeedError


class Cryptomodule(DeclarativeBase):
    __tablename__ = 'cryptomodule'

    id = Field(Integer, primary_key=True)
    time_interval = Field(Integer, default=60)
    one_time_password_length = Field(Integer, default=4)


class Token(ModifiedMixin, PaginationMixin, FilteringMixin, DeactivationMixin,
            OrderingMixin, DeclarativeBase):
    __tablename__ = 'token'

    id = Field(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid1
    )
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

    def initialize_seed(self, max_retry=1):
        session = object_session(self)
        while max_retry > 0:
            seed = cryptoutil.random(20)
            count = session.query(self.__class__) \
                .filter(self.__class__.seed == seed) \
                .count()
            if count == 0:
                self.seed = seed
                return

            max_retry = max_retry - 1

        raise DuplicateSeedError()

    def to_dict(self):
        result = super().to_dict()
        result['provisioning'] = None
        return result

    def provision(self, phone):
        """
        version:1+expdate:4+cryptomoduleId:1+length:1+timeInterval:1+bankId:1+seed:20+name:~14
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

        encrypted_binary = LionClient().encrypt(self.bank_id, phone, binary, checksum=4)
        hexstring = binascii.hexlify(encrypted_binary).decode()
        return f'mt://oath/totp/{hexstring}'


cached_cryptomodules = None


class MiniToken:
    _redis = None

    def __init__(self, id, bank_id, seed, expire_date, is_active, cryptomodule_id,
                 last_codes=None, final=False):
        if type(id) is str:
            self.id = uuid.UUID(id)

        else:
            self.id = id

        self.bank_id = bank_id
        self.seed = seed
        self.expire_date = expire_date
        self.is_active = is_active
        self.cryptomodule_id = cryptomodule_id
        self.final = final

        queue_size = int(settings.oath.window) + 2

        if last_codes is None:
            self.last_codes = deque(maxlen=queue_size)
        else:
            self.last_codes = last_codes

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
            Token.bank_id,
            Token.seed,
            extract('epoch', Token.expire_date),
            Token.activated_at.isnot(None),
            Token.cryptomodule_id,
        ).filter(Token.id == token_id).one_or_none()
        return cls(*row) if row else None

    @classmethod
    def load(cls, token_id, cache=False):
        if cache:  # pragma: no cover
            token = cls.load_from_cache(uuid.UUID(token_id))
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

    def verify(self, code, window, primitive=False):
        if code in self.last_codes:
            if self.final:
                return False

        else:
            self.last_codes.append(code)

        self.final = not primitive

        pinblock = cryptoutil.EncryptedISOPinBlock(self)
        otp = pinblock.decode(code)
        return TOTP(
            self.seed,
            time.time(),
            self.length,
            step=self.time_interval
        ).verify(otp, window)

    def cache(self):  # pragma: no cover
        self.redis().set(
            self.id.bytes,
            b'%s,%s,%d,%d,%d,%s,%d' % (
                str(self.bank_id).encode(),
                binascii.hexlify(self.seed),
                int(self.expire_date),
                int(self.is_active),
                self.cryptomodule_id,
                pickle.dumps(self.last_codes, 1),
                int(self.final)
            ),
            settings.token.redis.ttl
        )

    @classmethod
    def load_from_cache(cls, token_id):  # pragma: no cover
        cache_key = token_id.bytes
        redis = cls.redis()
        if redis.exists(cache_key):
            token = redis.get(cache_key).split(b',')
            return cls(
                token_id,
                int(token[0]),
                binascii.unhexlify(token[1]),
                float(token[2]),
                bool(token[3]),
                int(token[4]),
                pickle.loads(token[5]),
                int(token[6])
            ) if token else None
        return None

    @classmethod
    def invalidate(cls, token_id):  # pragma: no cover
        cls.redis().delete(token_id.bytes)

    @classmethod
    def after_update(cls, mapper, connection, target):  # pragma: no cover
        if settings.token.redis.enabled:
            cls.invalidate(target.id.bytes)


class Person(TimestampMixin, DeclarativeBase):
    __tablename__ = 'person'

    id = Field(Integer, primary_key=True)

    customer_code = Field(String(15), nullable=True)
    national_id = Field(String(12), nullable=True)
    name = Field(Unicode(40), nullable=True)
    family = Field(Unicode(60), nullable=True)
    mobile = Field(String(13), nullable=True)

event.listen(Token, 'after_update', MiniToken.after_update)

