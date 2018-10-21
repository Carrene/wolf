import time
import unittest
from datetime import date, timedelta
from contextlib import contextmanager

from nanohttp import settings, RegexRouteController, json, context, \
    HTTPNotFound, HTTPStatus
from bddrest import when, response, status, given
from restfulpy.mockup import MockupApplication, mockup_http_server

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import RandomMonkeyPatch, LocalApplicationTestCase


HOUR = 3600
DAY = HOUR * 24


_lion_status = 'idle'


@contextmanager
def lion_mockup_server():
    class Root(RegexRouteController):
        def __init__(self):
            super().__init__([
                (r'/apiv1/keys/(?P<keyname>\w+)', self.encrypt),
            ])

        @json(verbs=['encrypt'])
        def encrypt(self, keyname):
            if _lion_status != 'idle':
                raise HTTPStatus(_lion_status)

            checksum_length = int(context.form.get('checksumLength', '0'))
            assert checksum_length == 4

            return \
                'Ro4WsXckQscBovDEaOH3IrQHQeFNfu_7pxe54MgeQz33UbtMiLgKDYx3_46' \
                'aVoe6JDhWhYHna31YG-_W6D0L0g=='


    app = MockupApplication('lion-mockup', Root())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
          ssm:
            url: {url}
        ''')
        yield app


@contextmanager
def lion_status(status):
    global _lion_status
    _lion_status = status
    yield
    _lion_status = 'idle'


class TestEnsureToken(LocalApplicationTestCase):
    __metadata__ = {
        r'^/apiv1/tokens.*': Token.json_metadata()['fields']
    }

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.mockup_cryptomodule = mockup_cryptomodule = Cryptomodule()
        session.add(mockup_cryptomodule)

        expired_token = Token()
        expired_token.name = 'ExpiredToken'
        expired_token.phone = 989122451075
        expired_token.expire_date = date.today() - timedelta(days=1)
        expired_token.seed = \
            b'\xdb!.\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        expired_token.is_active = True
        expired_token.cryptomodule = mockup_cryptomodule
        session.add(expired_token)

        deactivated_token = Token()
        deactivated_token.name = 'DeactivatedToken'
        deactivated_token.phone = 989122451075
        deactivated_token.expire_date = '2099-12-07T18:14:39.558891'
        deactivated_token.seed = \
            b'\xeb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule
        session.add(deactivated_token)
        session.commit()

    def test_ensure_token(self):
        with RandomMonkeyPatch(
            b'F\x8e\x16\xb1w$B\xc7\x01\xa2\xf0\xc4h\xe1\xf7"\xf8\x98w\xcf'
        ), lion_mockup_server(), self.given(
            'Provisioning',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'name': 'DummyTokenName',
                'cryptomoduleId': self.mockup_cryptomodule.id,
                'expireDate': 1613434403,
            }
        ):

            assert status == 200
            result = response.json
            assert 'provisioning' in result
            assert result['expireDate'] == '2021-02-16'
            token = result['provisioning']
            assert token == \
                'mt://oath/totp/468e16b1772442c701a2f0c468e1f722b40741e14d7e' \
                'effba717b9e0c81e433df751bb4c88b80a0d8c77ff8e9a5687ba2438568' \
                '581e76b7d581befd6e83d0bd2'

            when('Ensure the same token again')
            assert status == 200
            assert 'provisioning' in response.json
            assert response.json['provisioning'] == token

            when(
                'Expire date is a float value',
                form=given | dict(expireDate=1613434403.3)
            )
            assert status == 200

            with lion_status('404 Not Found'):
                when('Device is not found')
                assert status == '605 Device is not found: 989122451075'

            when(
                'CryptomoduleId is not integer',
                form=given | dict(cryptomoduleId='NotInteger')
            )
            assert status == '701 CryptomoduleId must be Integer'

            when(
                'CryptomoduleId does not exists',
                form=given | dict(cryptomoduleId=0)
            )
            assert status == '601 Cryptomodule does not exists: 0'

            when(
                'Provisioning with an empty token name',
                form=given | dict(name='')
            )
            assert status == \
                '702 Name length should be between 6 and 50 characters'

            when(
                'Provisioning with a long token name',
                form=given | dict(name='a' * (50+1))
            )
            assert status == \
                '702 Name length should be between 6 and 50 characters'

            when(
                'Provisioning with an expired token',
                form=given | dict(name='ExpiredToken')
            )
            assert status == '602 Token is expired'

            when(
                'Provisioning with a deactivated token',
                form=given | dict(name='DeactivatedToken')
            )
            assert status == '603 Token is deactivated'

            when(
                'Name is not given',
                form=given - 'name'
            )
            assert status == '703 name is required'

            when(
                'Phone is not given',
                form=given - 'phone'
            )
            assert status == '704 phone is required'

            when(
                'Phone is not an integer',
                form=given | dict(phone='NotInteger')
            )
            assert status == '705 phone should be Integer'

            when(
                'Cryptomodule is not given',
                form=given - 'cryptomoduleId'
            )
            assert status == '706 cryptomoduleId is required'

            when(
                'Expire date is not given',
                form=given - 'expireDate'
            )
            assert status == '707 expireDate is required'

            when(
                'Expire date is not an integer or float',
                form=given | dict(expireDate='NotInteger')
            )
            assert status == '708 expireDate should be Integer or Float'

            when(
                'Form field is unknown',
                form=given + dict(a=1)
            )
            assert status == '400 Field: a Not Allowed'

            with lion_status('502 Bad Gateway'):
                when('SSM is not available')
                assert status == '801 SSM is not available'

            with lion_status('500 Internal Server Error'):
                when('SSM is not working properly')
                assert status == '802 SSM internal error'

            with lion_status('400 Internal Server Error'):
                when('SSM Returns 400 Bad request ')
                assert status == '802 SSM internal error'

            when(
                'Seed is duplicated, it\'s a very rare exception',
                form=given | dict(phone=989122451010)
            )
            assert status == \
                '666 Cannot generate and randomize seed, please try again'

