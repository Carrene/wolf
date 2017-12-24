
from nanohttp import action, HttpNotFound, HttpConflict, settings, RestController, HttpBadRequest
from restfulpy.orm import commit, DBSession
from restfulpy.validation import prevent_form


class CodesController(RestController):

    def __init__(self, token):
        self.token = token

    @action
    @prevent_form
    def verify(self, code):

        if not self.token.cryptomodule:
            raise HttpNotFound('Token does not have cryptomodule.', 'cryptomodule-not-exists')

        if not self.token.is_active:
            raise HttpConflict('Token has been deactivated', 'token-deactivated')

        if self.token.is_locked:
            raise HttpConflict('You reached the consecutive tries limit', 'token-blocked')

        if self.token.is_expired:
            raise HttpConflict('Token has been expired', 'token-expired')

        window = settings.oath.window
        try:
            is_valid, ___ = self.token.create_one_time_password_algorithm().verify(code, window)
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
