import re

from nanohttp import json, context, action, settings, RestController, \
    HTTPStatus, HTTPNotFound, LazyAttribute, Controller, validate
from restfulpy.controllers import ModelRestController, RootController
from restfulpy.orm import commit, DBSession
from sqlalchemy.exc import IntegrityError

import wolf
from .exceptions import DeactivatedTokenError, ExpiredTokenError, \
    DuplicateSeedError, InvalidPartialCardNameError
from .models import Cryptomodule, Token, MiniToken


AYANDE_BANK_ID = 2


class CodesController(RestController):

    @LazyAttribute
    def window(self):
        return settings.oath.window

    @action(prevent_form='400 Form Not Allowed')
    def verify(self, token_id, code):
        token = MiniToken.load(token_id, cache=settings.token.redis.enabled)
        if token is None:
            raise HTTPNotFound()

        if token.is_expired:
            raise ExpiredTokenError()

        if not token.is_active:
            raise DeactivatedTokenError()

        primitive = context.query.get('primitive') == 'yes'
        try:
            is_valid = token.verify(
                code.encode(),
                self.window,
                primitive=primitive
            )
            token.cache()
        except ValueError:
            is_valid = False

        if not is_valid:
            raise HTTPStatus('604 Invalid code')


class TokenController(ModelRestController):
    __model__ = Token

    def __init__(self):
        super().__init__()
        self.codes_controller = CodesController()

    def __call__(self, *remaining_paths):
        if len(remaining_paths) > 1 and remaining_paths[1] == 'codes':
            return self.codes_controller(
                remaining_paths[0],
                *remaining_paths[2:]
            )
        return super().__call__(*remaining_paths)

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

