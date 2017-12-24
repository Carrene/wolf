import functools

from nanohttp import json, action, context, HttpNotFound, HttpConflict, settings
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from restfulpy.validation import validate_form

from wolf.models import Token, Device
from wolf.excpetions import DeviceNotFoundError


validate_submit = functools.partial(
    validate_form,
    types={'name': str, 'clientReference': int, 'providerReference': int, 'cryptomoduleId': int, 'expireDate': str},
    pattern={'expireDate': '^\d{4}-\d{2}-\d{2}$'}
)


class TokenController(ModelRestController):
    __model__ = Token

    @action
    # FIXME: Set pattern for challenge
    @validate_form(whitelist=['code', 'challenge'], requires=['code'], types={'code': str})
    @commit
    def verify(self, token_id: int, inner_resource: str):
        token = Token.query.filter(Token.id == token_id).one_or_none()
        if not token:
            raise HttpNotFound()

        if inner_resource == 'codes':
            if not token.cryptomodule:
                raise HttpNotFound('Token does not have cryptomodule.', 'cryptomodule-not-exists')
            if not token.is_active:
                raise HttpConflict('Token has been deactivated', 'token-deactivated')
            if token.is_locked:
                raise HttpConflict('You reached the consecutive tries limit', 'token-blocked')
            if token.is_expired:
                raise HttpConflict('Token has been expired', 'token-expired')

            code = context.form['code']
            challenge = context.form.get('challenge', None)
            window = settings.oath.window
            if challenge:
                try:
                    is_valid, ___ = token.create_challenge_response_algorithm().verify(code, challenge, window)
                except ValueError:
                    is_valid = False
            else:
                try:
                    is_valid, ___ = token.create_one_time_password_algorithm().verify(code, window)
                except ValueError:
                    is_valid = False

            if is_valid is True:
                token.consecutive_tries = 0
                if token.cryptomodule.counter_type == 'counter':
                    token.counter += 1
                return
            else:
                token.consecutive_tries += 1

            # We should commit the DBSession in order to prevent rollback of consecutive_tries value.
            DBSession.commit()

            raise HttpConflict('Not verified.', 'not-verified')

        raise HttpNotFound()

    def __ensure_device(self):
        client_reference = int(context.form['clientReference'])
        name = context.form['name']

        # Checking the device
        device = Device.query.filter(Device.reference_id == client_reference).one_or_none()
        # Adding a device also
        if device is None:
            raise DeviceNotFoundError()
        return device

    def __ensure_token(self):
        name = context.form['name']
        client_reference = int(context.form['clientReference'])
        cryptomodule_id = int(context.form['cryptomoduleId'])

        token = Token.query.filter(
            Token.name == name,
            Token.cryptomodule_id == cryptomodule_id,
            Token.client_reference == client_reference
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.update_from_request()
            token.is_active = True
            token.initialize_seed(DBSession)
            DBSession.add(token)
        return token

    @json
    @validate_form(
        whitelist=['name', 'clientReference', 'providerReference', 'cryptomoduleId', 'expireDate'],
        requires=['name', 'clientReference', 'cryptomoduleId'],
        types={'cryptomoduleId': int}
    )
    @Token.expose
    @commit
    def ensure(self):
        # TODO: type validation
        token = self.__ensure_token()
        device = self.__ensure_device()
        DBSession.flush()
        result = token.to_dict()
        result['provisioning'] = token.provision(device.secret)
        return result
