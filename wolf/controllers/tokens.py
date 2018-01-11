import functools

from nanohttp import json, context, HttpNotFound, HttpBadRequest
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from restfulpy.validation import validate_form

from ..models import Token, Device, Cryptomodule
from ..excpetions import DeviceNotFoundError, ExpiredTokenError, LockedTokenError
from .codes import CodesController


validate_submit = functools.partial(
    validate_form,
    types={'name': str, 'phone': int, 'cryptomoduleId': int, 'expireDate': str},
    pattern={'expireDate': '^\d{4}-\d{2}-\d{2}$'}
)


class TokenController(ModelRestController):
    __model__ = Token

    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'codes':
            token = self._ensure_token(remaining_paths[0])
            return CodesController(token)(*remaining_paths[2:])
        return super().__call__(*remaining_paths)

    @staticmethod
    def _ensure_token(token_id):
        token = Token.query.filter(Token.id == token_id).one_or_none()
        if not token:
            raise HttpNotFound()

        return token

    @staticmethod
    def _validate_token(token):
        if token.is_expired:
            raise ExpiredTokenError()

        if token.is_locked:
            raise LockedTokenError()

    @staticmethod
    def _ensure_device():
        phone = int(context.form['phone'])

        # Checking the device
        device = Device.query.filter(Device.phone == phone).one_or_none()
        # Adding a device also
        if device is None:
            raise DeviceNotFoundError()
        return device

    @staticmethod
    def _find_or_create_token():
        name = context.form['name']
        phone = context.form['phone']
        cryptomodule_id = context.form['cryptomoduleId']

        if Cryptomodule.query.filter(Cryptomodule.id == cryptomodule_id).count() <= 0:
            raise HttpBadRequest(info='Invalid cryptomodule id.')

        token = Token.query.filter(
            Token.name == name,
            Token.cryptomodule_id == cryptomodule_id,
            Token.phone == phone
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.update_from_request()
            token.is_active = True
            token.initialize_seed()
            DBSession.add(token)
        DBSession.flush()
        return token

    @json
    @validate_form(
        exact=['name', 'phone', 'cryptomoduleId', 'expireDate'],
        types={'cryptomoduleId': int, 'expireDate': float, 'phone': int}
    )
    @Token.expose
    @commit
    def ensure(self):
        # TODO: type validation
        device = self._ensure_device()
        token = self._find_or_create_token()
        self._validate_token(token)
        DBSession.flush()
        result = token.to_dict()
        result['provisioning'] = token.provision(device.secret)
        return result

    @json
    @Token.expose
    def list(self):
        return Token.query

    @json
    @Token.expose
    def get(self, token_id: int):
        return self._ensure_token(token_id)
