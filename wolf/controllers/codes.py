import time

import redis
import oathcy
from sqlalchemy.sql import text, func, extract
from nanohttp import action, settings, RestController, HttpBadRequest, HttpNotFound, LazyAttribute
from restfulpy.orm import DBSession
from restfulpy.validation import prevent_form

from ..cryptoutil import EncryptedISOPinBlock
from ..excpetions import ExpiredTokenError, DeactivatedTokenError
from ..models import Token


cached_cryptomodules = None


class MiniToken:
    _redis = None

    def __init__(self, id, seed, expire_date, is_active, cryptomodule_id):
        self.id = id
        self.seed = seed
        self.expire_date = expire_date
        self.is_active = is_active
        self.cryptomodule_id = cryptomodule_id

    @staticmethod
    def create_blocking_redis_client():
        return redis.StrictRedis(
            host=settings.token.redis.host,
            port=settings.token.redis.port,
            db=settings.token.redis.db,
            password=settings.token.redis.password
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
    def load_from_cache(cls, token_id):
        cache_key = str(token_id)
        redis = cls.redis()
        if redis.exists(cache_key):
            token = redis.get(cache_key).split(b',')
            return cls(
                int(token[0]),
                token[1],
                float(token[2]),
                bool(token[3]),
                int(token[4])
            ) if token else None
        return None

    @classmethod
    def load(cls, token_id, cache=False):
        if cache:
            token = cls.load_from_cache(token_id)
            if token is None:
                token = cls.load_from_database(token_id)

            if token is not None:
                token.cache()
        else:
            token = cls.load_from_database(token_id)

        return token

    def cache(self):
        self.redis().set(
            str(token_id),
            '%s,%s,%s,%s,%s' % (
                self.id, self.seed , self.expire_date, self.is_active, self.cryptomodule_id
            )
        )

    @property
    def is_expired(self):
        return self.expire_date <= time.time()

    @property
    def cryptomodules(self):
        global cached_cryptomodules
        if cached_cryptomodules is None:
            modules = {}
            for m in DBSession.execute(text(
                'SELECT id, time_interval, one_time_password_length FROM cryptomodule'
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

    def verify(self, otp, window):
        return oathcy.totp_verify(
            self.seed,
            time.time(),
            window,
            otp,
            self.time_interval
        )


class CodesController(RestController):

    @LazyAttribute
    def window(self):
        return settings.oath.window

    @action
    @prevent_form
    def verify(self, token_id, code):
        token = MiniToken.load(token_id, cache=settings.token.redis.enabled)
        if token is None:
            raise HttpNotFound()

        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

        pinblock = EncryptedISOPinBlock(token_id)
        is_valid = token.verify(
            pinblock.decode(code.encode()),
            self.window,
        )
        if not is_valid:
            raise HttpBadRequest('Invalid Code')

