import re
import time

from nanohttp import json, context, action, settings, RestController, \
    HTTPStatus, HTTPNotFound, LazyAttribute, Controller, validate, \
    int_or_notfound
from restfulpy.controllers import ModelRestController, RootController
from restfulpy.orm import commit, DBSession
from restfulpy.authorization import authorize
from sqlalchemy.exc import IntegrityError
from oathcy.otp import TOTP

import wolf
from .exceptions import DeactivatedTokenError, ExpiredTokenError, \
    DuplicateSeedError, InvalidPartialCardNameError
from .models import Cryptomodule, Token, MiniToken


AYANDE_BANK_ID = 2


class CodesController(RestController):

    def __init__(self, token):
        self.token = token

    @LazyAttribute
    def window(self):
        return settings.oath.window

    @action(prevent_form='400 Form Not Allowed')
    @authorize
    def verify(self, code):
        primitive = context.query.get('primitive') == 'yes'
        try:
            is_valid = self.token.verify(
                code.encode(),
                self.window,
                primitive=primitive
            )
            self.token.cache()
        except ValueError:
            is_valid = False

        if not is_valid:
            raise HTTPStatus('604 Invalid code')

    @json(prevent_form='400 Form Not Allowed')
    @authorize
    def generate(self):
        code = TOTP(
            self.token.seed,
            int(time.time()),
            self.token.cryptomodule.one_time_password_length,
            step=self.token.cryptomodule.time_interval
        ).generate().decode()

        return dict(code=code)


class TokenController(ModelRestController):
    __model__ = Token

    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'codes':
            token = self._get_token(remaining_paths[0])
            self._validate_token(token)
            return CodesController(token=token)(*remaining_paths[2:])

        return super().__call__(*remaining_paths)

    def _get_token(self, id):
        id = int_or_notfound(id)
        token = MiniToken.load(id, cache=settings.token.redis.enabled)
        if token is None:
            raise HTTPNotFound()

        return token

    @staticmethod
    def _validate_token(token):
        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

    @staticmethod
    def _find_or_create_token(name, phone):
        cryptomodule_id = context.form['cryptomoduleId']
        context.form.setdefault('bankId', AYANDE_BANK_ID)
        bank_id = context.form['bankId']

        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            raise HTTPStatus(
                f'601 Cryptomodule does not exists: {cryptomodule_id}'
            )

        token = DBSession.query(Token).filter(
            Token.name == name,
            Token.cryptomodule_id == cryptomodule_id,
            Token.phone == phone,
            Token.bank_id == bank_id
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.update_from_request()
            token.is_active = True
            DBSession.add(token)

        token.initialize_seed()

        try:
            DBSession.flush()
        except IntegrityError as ex:
            raise DuplicateSeedError()
        else:
            return token

    @json(
        form_whitelist=[
            'name', 'phone', 'cryptomoduleId', 'expireDate','bankId'
        ]
    )
    @Token.validate(strict=True, fields=dict(
        bankId=dict(
            required=False,
            not_none=False,
        )
    ))
    @Token.expose
    @commit
    @authorize
    def exsure(self):
        phone = context.form['phone']
        name = context.form['name']
        token = self._find_or_create_token(name, phone)
        self._validate_token(token)
        DBSession.flush()
        result = token.to_dict()
        result['provisioning'] = token.provision(phone)
        return result


class CardTokenController(ModelRestController):
    __model__ = Token

    @staticmethod
    def _validate_token(token):
        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

    @staticmethod
    def _find_or_create_token(partial_card_name, phone):
        cryptomodule_id = context.form['cryptomoduleId']
        context.form.setdefault('bankId', AYANDE_BANK_ID)
        bank_id = context.form['bankId']
        pattern = settings.card_tokens[bank_id].pattern

        if not re.match(pattern, partial_card_name):
            raise InvalidPartialCardNameError()

        if DBSession.query(Cryptomodule) \
                .filter(Cryptomodule.id == cryptomodule_id) \
                .count() <= 0:
            raise HTTPStatus(
                f'601 Cryptomodule does not exists: {cryptomodule_id}'
            )

        token = DBSession.query(Token).filter(
            Token.name == partial_card_name,
            Token.cryptomodule_id == cryptomodule_id,
            Token.phone == phone,
            Token.bank_id == bank_id
        ).one_or_none()

        if token is None:
            # Creating a new token
            token = Token()
            token.update_from_request()
            token.name = partial_card_name
            token.is_active = True
            DBSession.add(token)

        token.initialize_seed()

        try:
            DBSession.flush()
        except IntegrityError as ex:
            raise DuplicateSeedError()
        else:
            return token

    @json(
        form_whitelist=[
            'partialCardName', 'phone', 'cryptomoduleId', 'expireDate','bankId'
        ]
    )
    @Token.validate(strict=True, fields=dict(
        bankId=dict(
            required=False,
            not_none=False,
        ),
        name=dict(
            required=False,
            not_none=False,
        ),
        partialCardName=dict(
            required='712 partial card name is required',
            not_none='713 partial card name can not be empty',
            min_length=(
                6,
                '714 partial card name length '\
                'should be between 6 and 50 characters'
            ),
            max_length= (
                50,
                '714 partial card name length should '\
                'be between 6 and 50 characters'
            )
        )
    ))
    @Token.expose
    @commit
    @authorize
    def ensure(self):
        partial_card_name = context.form['partialCardName']
        phone = context.form['phone']
        token = self._find_or_create_token(partial_card_name, phone)
        self._validate_token(token)
        DBSession.flush()
        result = token.to_dict()
        result['provisioning'] = token.provision(phone)
        result['partialCardName'] = result.pop('name')
        return result


class ApiV1(Controller):
    tokens = TokenController()
    cardtokens = CardTokenController()

    @json
    def version(self):
        return {
            'version': wolf.__version__
        }

    @json
    def info(self):
        return {
            'version': wolf.__version__,
            'title': settings.process_name
        }


class Root(RootController):
    apiv1 = ApiV1()

