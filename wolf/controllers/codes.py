
from nanohttp import action, settings, RestController, HttpBadRequest
from restfulpy.orm import DBSession
from restfulpy.validation import prevent_form

from ..excpetions import ExpiredTokenError, LockedTokenError, DeactivatedTokenError
from ..cryptoutil import EncryptedISOPinBlock


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

        if not self.token.is_active:
            raise DeactivatedTokenError()

        pinblock = EncryptedISOPinBlock(self.token.id)
        is_valid = self.token.verify_totp(pinblock.decode(code.encode()))
#         try:
#             is_valid, ___ = self.token.create_one_time_password_algorithm().verify(pinblock.decode(code), window)
#         except ValueError:
#             is_valid = False

        if is_valid is True:
            self.token.consecutive_tries = 0
            DBSession.commit()
        else:
            # Code is not verified
            self.token.consecutive_tries += 1
            DBSession.commit()
            raise HttpBadRequest('Invalid Code')

