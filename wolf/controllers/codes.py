import time

import oathcy
from sqlalchemy.sql import text
from nanohttp import action, settings, RestController, HttpBadRequest, HttpNotFound, LazyAttribute
from restfulpy.orm import DBSession
from restfulpy.validation import prevent_form

from ..cryptoutil import EncryptedISOPinBlock
from ..excpetions import ExpiredTokenError, DeactivatedTokenError
from ..models import BaseToken, Token


cached_cryptomodules = None


class MiniToken(BaseToken):

    def __init__(self, id, seed, expire_date, activated_at, cryptomodule_id):
        self.id = id
        self.seed = seed
        self.expire_date = expire_date
        self.activated_at = activated_at
        self.cryptomodule_id = cryptomodule_id

    @classmethod
    def load_from_database(cls, token_id):
        row = DBSession.query(
            Token.id,
            Token.seed,
            Token.expire_date,
            Token.activated_at,
            Token.cryptomodule_id,
        ).filter(Token.id == token_id).one_or_none()
        return cls(*row)

    @classmethod
    def load(cls, token_id):
        return cls.load_from_database(token_id)

    @property
    def is_active(self):
        return self.activated_at is not None

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
        token = MiniToken.load(token_id)
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

