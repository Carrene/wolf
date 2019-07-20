from contextlib import contextmanager
from datetime import date, timedelta

from bddrest import when, response, status, given
from nanohttp import settings, RegexRouteController, json, context, HTTPStatus
from restfulpy.mockup import MockupApplication, mockup_http_server

from wolf.models import Cryptomodule, Token
from .helpers import RandomMonkeyPatch, LocalApplicationTestCase


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


class TestEnsureCardToken(LocalApplicationTestCase):

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
        expired_token.bank_id = 1
        session.add(expired_token)

        deactivated_token = Token()
        deactivated_token.name = 'DeactivatedToken'
        deactivated_token.phone = 989122451075
        deactivated_token.expire_date = '2099-12-07T18:14:39.558891'
        deactivated_token.seed = \
            b'\xeb!\x2e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule
        deactivated_token.bank_id = 2
        session.add(deactivated_token)
        session.commit()

    def test_ensure_cardtoken(self):
        self.login_as_switchcard()

        with lion_mockup_server(), self.given(
            'Provisioning',
            '/apiv1/cardtokens',
            'ENSURE',
            form={
                'phone': 989122451075,
                'partialCardName': '603799DummyToken',
                'cryptomoduleId': self.mockup_cryptomodule.id,
                'expireDate': 1613434403,
                'bankId': 1,
            }
        ):

            assert status == 200
            result = response.json
            assert 'provisioning' in result
            assert 'partialCardName' in result
            assert 'name' not in result
            assert result['expireDate'] == '2021-02-16'
            token = result['provisioning']
            assert token == \
                'mt://oath/totp/468e16b1772442c701a2f0c468e1f722b40741e14d7e' \
                'effba717b9e0c81e433df751bb4c88b80a0d8c77ff8e9a5687ba2438568' \
                '581e76b7d581befd6e83d0bd2'

            when(
                'Expire date is a float value',
                form=given | dict(
                    expireDate=1613434403.3,
                    partialCardName='603799DummyToken'
                )
            )
            assert status == 200

            when(
                'Partial card name is invalid',
                form=given | dict(partialCardName='636214DummyTokenName2')
            )
            assert status == '711 Invalid partial card name'

            with lion_status('404 Not Found'):
                when('Device is not found')
                assert status == '605 Device is not found: 1989122451075'

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
                'Provisioning with a long token partial card name',
                form=given | dict(partialCardName='a' * (50+1))
            )
            assert status == '714 partial card name length '\
                'should be between 6 and 50 characters'

            when(
                'Partial card name is not given',
                form=given - 'partialCardName'
            )
            assert status == '712 partial card name is required'

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

            with lion_status('401 Unauthorized'):
                when('SSM Returns 401 Unauthorized')
                assert status == '803 SSM Unauthorized error'

