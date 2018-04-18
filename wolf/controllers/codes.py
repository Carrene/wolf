import time
from datetime import date

import oathcy
from sqlalchemy import update, select
from sqlalchemy.sql import text
from nanohttp import action, settings, RestController, HttpBadRequest, HttpNotFound, LazyAttribute
from restfulpy.validation import prevent_form
from restfulpy.orm import DBSession

from ..excpetions import ExpiredTokenError, LockedTokenError, DeactivatedTokenError
from ..cryptoutil import EncryptedISOPinBlock
from ..models import MiniToken, Token, Cryptomodule


class CodesController(RestController):

    @LazyAttribute
    def window(self):
        return settings.oath.window

    @LazyAttribute
    def max_tries(self):
        return settings.token.max_consecutive_tries

#     @LazyAttribute
#     def connection(self):
#         from wolf import wolf
#         return wolf.engine.connect()

    @LazyAttribute
    def cryptomodules(self):
        modules = {}
        for m in DBSession.execute(text(
            'SELECT id, time_interval, one_time_password_length FROM cryptomodule'
            )):
            modules[m[0]] = m
        return modules

    @action
    @prevent_form
    def verify(self, token_id, code):
        tokens = DBSession.execute(text(
            'SELECT seed, consecutive_tries, expire_date, activated_at, cryptomodule_id '
            'FROM token WHERE id = :token_id'),
            dict(token_id=token_id)
        ).fetchall()
        if tokens:
            token = tokens[0]
        else:
            raise HttpNotFound()

        if self.max_tries <= token[1]:
            raise LockedTokenError()

        if date.today() > token[2]:
            raise ExpiredTokenError()

        if token[3] is None:
            raise DeactivatedTokenError()

        pinblock = EncryptedISOPinBlock(token_id)
        is_valid = oathcy.totp_verify(
            bytes(token[0]),  # Seed
            time.time(),
            self.window,
            pinblock.decode(code.encode()),
            self.cryptomodules[token[4]][1],  # Time Interval
        )
        if is_valid:
            DBSession.execute(
                text('UPDATE token SET consecutive_tries=0 WHERE id = :token_id'),
                dict(token_id=token_id)
            )
            DBSession.commit()
        else:
            # Code is not verified
            DBSession.execute(text(
                f'UPDATE token SET consecutive_tries={token[1]+1} WHERE id=:token_id'),
                dict(token_id=token_id)
            )
            DBSession.commit()
            raise HttpBadRequest('Invalid Code')

