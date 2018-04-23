from nanohttp import action, settings, RestController, HttpBadRequest, HttpNotFound, LazyAttribute
from restfulpy.orm import DBSession
from restfulpy.validation import prevent_form

from ..cryptoutil import EncryptedISOPinBlock
from ..excpetions import ExpiredTokenError, DeactivatedTokenError
from ..models import MiniToken


class CodesController(RestController):

    @LazyAttribute
    def window(self):
        return settings.oath.window

    @action
    @prevent_form
    def verify(self, token_id, code):
        token = DBSession.query(MiniToken).filter(MiniToken.id == token_id).one_or_none()
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

