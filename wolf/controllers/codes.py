import functools

from nanohttp import action, settings, RestController, HttpBadRequest
from restfulpy.orm import DBSession
from restfulpy.validation import prevent_form
from pymlconf.proxy import ObjectProxy

from ..excpetions import ExpiredTokenError, LockedTokenError
from ..cryptoutil import ISO0PinBlock


pinblock = ObjectProxy(ISO0PinBlock)


class CodesController(RestController):

    def __init__(self, token):
        self.token = token

    @action
    @prevent_form
    def verify(self, code):

        if self.token.is_locked:
            raise LockedTokenError()

        if self.token.is_expired:
            raise ExpiredTokenError()

        window = settings.oath.window
        try:
            is_valid, ___ = self.token.create_one_time_password_algorithm().verify(pinblock.decode(code), window)
        except ValueError:
            is_valid = False

        if is_valid is True:
            self.token.consecutive_tries = 0
            DBSession.commit()
        else:
            # Code is not verified
            self.token.consecutive_tries += 1
            DBSession.commit()
            raise HttpBadRequest('Invalid Code')
