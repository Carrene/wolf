
from sqlalchemy import update
from nanohttp import action, settings, RestController, HttpBadRequest, HttpNotFound
from restfulpy.orm import DBSession
from restfulpy.validation import prevent_form

from ..excpetions import ExpiredTokenError, LockedTokenError, DeactivatedTokenError
from ..cryptoutil import EncryptedISOPinBlock
from ..models import MiniToken, Token


class CodesController(RestController):

    def __init__(self, token_id):
        self.token_id = token_id

    @action
    @prevent_form
    def verify(self, code):
        query = DBSession.query(MiniToken).filter(MiniToken.id == self.token_id)
        token = query.one_or_none()

        if token is None:
            raise HttpNotFound()

        if token.is_locked:
            raise LockedTokenError()

        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

        pinblock = EncryptedISOPinBlock(token.id)
        is_valid = token.verify_totp(pinblock.decode(code.encode()))

        if is_valid:
 #       if is_valid is True:
            DBSession.execute(
                update(Token).where(Token.id == self.token_id).values(consecutive_tries=0)
            )
            DBSession.commit()
        else:
            # Code is not verified
            DBSession.execute(
                update(Token).where(Token.id == self.token_id).values(
                    consecutive_tries=token.consecutive_tries+1
                )
            )
            DBSession.commit()
            raise HttpBadRequest('Invalid Code')

