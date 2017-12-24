import functools

from nanohttp import json, context, HttpNotFound
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from restfulpy.validation import validate_form

from ..models import Token, Device
from ..excpetions import DeviceNotFoundError
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
        phone = int(context.form['phone'])
        cryptomodule_id = int(context.form['cryptomoduleId'])

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
            token.initialize_seed(DBSession)
            DBSession.add(token)
        return token

    @json
    @validate_form(
        exact=['name', 'phone', 'cryptomoduleId', 'expireDate'],
        types={'cryptomoduleId': int, 'expireDate': float}
    )
    @Token.expose
    @commit
    def ensure(self):
        # TODO: type validation
        device = self._ensure_device()
        token = self._find_or_create_token()
        DBSession.flush()
        result = token.to_dict()
        result['provisioning'] = token.provision(device.secret)
        return result
