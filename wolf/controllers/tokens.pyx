import functools

from datetime import date
from nanohttp import json, context, HttpNotFound, HttpBadRequest, HttpConflict
from restfulpy.controllers import ModelRestController
from restfulpy.orm import commit, DBSession
from restfulpy.validation import validate_form

from ..models import Token, Device, Cryptomodule
from ..excpetions import DeviceNotFoundError, ExpiredTokenError, LockedTokenError, DeactivatedTokenError,\
    ActivatedTokenError, NotLockedTokenError
from .codes import CodesController


validate_submit = functools.partial(
    validate_form,
    types={'name': str, 'phone': int, 'cryptomoduleId': int, 'expireDate': str},
    pattern={'expireDate': '^\d{4}-\d{2}-\d{2}$'}
)


class TokenController(ModelRestController):
    __model__ = Token

    def __init__(self):
        super().__init__()
        self.codes_controller = CodesController()
    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'codes':
            return self.codes_controller(remaining_paths[0], *remaining_paths[2:])
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

        if not token.is_active:
            raise DeactivatedTokenError()

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

    @json
    @validate_form(
        exact=['expireDate'],
        types={'expireDate': float}
    )
    @Token.expose
    @commit
    def extend(self, token_id: int):
        token = self._ensure_token(token_id)
        expire_date = date.fromtimestamp(context.form['expireDate'])

        if expire_date <= max(token.expire_date, date.today()):
            raise HttpBadRequest(info='expireDate must be grater that current expireDate.')
        token.expire_date = expire_date
        DBSession.add(token)
        return token

    @json
    @Token.expose
    @commit
    def unlock(self, token_id: int):
        token = self._ensure_token(token_id)

        if not token.is_locked:
            raise NotLockedTokenError()

        token.consecutive_tries = 0
        DBSession.add(token)
        return token

    @json
    @Token.expose
    @commit
    def delete(self, token_id: int):
        token = self._ensure_token(token_id)
        result = token.to_dict()
        DBSession.delete(token)
        return result

    @json
    @Token.expose
    @commit
    def activate(self, token_id: int):
        token = self._ensure_token(token_id)

        if token.is_active:
            raise ActivatedTokenError()

        token.is_active = True
        DBSession.add(token)
        return token

    @json
    @Token.expose
    @commit
    def deactivate(self, token_id: int):
        token = self._ensure_token(token_id)

        if not token.is_active:
            raise DeactivatedTokenError()

        token.is_active = False
        DBSession.add(token)
        return token
