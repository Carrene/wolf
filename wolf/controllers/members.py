from nanohttp import RestController, json, context, HttpBadRequest
from restfulpy.logging_ import get_logger


logger = get_logger('auth')


class MembersController(RestController):

    @json
    def login(self):
        username = context.form.get('username')
        password = context.form.get('password')

        def bad():
            logger.info('Login failed: %s' % username)
            raise HttpBadRequest('Invalid username or password')

        if not (username and password):
            bad()

        logger.info('Trying to login: %s' % username)
        principal = context.application.__authenticator__.login((username, password))
        if principal is None:
            bad()

        return dict(token=principal.dump())
