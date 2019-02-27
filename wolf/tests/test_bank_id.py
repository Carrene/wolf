from contextlib import contextmanager
from datetime import date, timedelta

from bddrest import when, response, status, given
from nanohttp import settings, RegexRouteController, json, context, HTTPStatus
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


class TestEnsureTokenBankId(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.mockup_cryptomodule = mockup_cryptomodule = Cryptomodule()
        session.add(mockup_cryptomodule)

        token = Token()
        token.name = 'ExpiredToken'
        token.phone = 989122451075
        token.expire_date = date.today() - timedelta(days=1)
        token.seed = \
            b'\xdb!.\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        token.is_active = True
        token.cryptomodule = mockup_cryptomodule
        token.bank_id = 2
        session.add(token)
        session.commit()

    def test_ensure_token_bank_id(self):
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

            when(
                'Form give bank id',
                form=given + dict(bankId=62)
            )
            assert status == 200

            when(
                'BankId is not an integer',
                form=given | dict(bankId='NotInteger')
            )
            assert status == '710 BankId must be Integer'

