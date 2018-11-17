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
            checksum_length = int(context.form.get('checksumLength', '0'))
            assert checksum_length == 4
            assert 'AQADW8UBBDxhYmNkZWZnaGlqa2xtbm9wcXJzdGFiY2RlZmdoaWprbG1u' \
                == context.form['data']

            return \
                'YWJjZGVmZ2hpamtsbW5vcKiw48-fEhSGJEqHPBWoVMnhZH4PYuXujJ9e2qn' \
                'wqcCPz_MG_XIzTwPNM5OBsetuWg=='


    app = MockupApplication('lion-mockup', Root())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
          ssm:
            url: {url}
        ''')
        yield app


class TestIntegration(LocalApplicationTestCase):
    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.mockup_cryptomodule = mockup_cryptomodule = Cryptomodule()
        session.add(mockup_cryptomodule)
        session.commit()

    def test_ensure_token(self):
        with RandomMonkeyPatch(b'abcdefghijklmnopqrst'), \
                lion_mockup_server(), self.given(
            'Provisioning for integration test',
            '/apiv1/tokens',
            'ENSURE',
            form={
                'phone': 989121234567,
                'name': 'abcdefghijklmn',
                'cryptomoduleId': self.mockup_cryptomodule.id,
                'expireDate': 1640982600,
            }
        ):

            assert status == 200
            result = response.json
            assert 'provisioning' in result
            assert result['expireDate'] == '2022-01-01'
            token = result['provisioning']
            assert token == \
                'mt://oath/totp/6162636465666768696a6b6c6d6e6f70a8b0e3cf9f12' \
                '1486244a873c15a854c9e1647e0f62e5ee8c9f5edaa9f0a9c08fcff306f' \
                'd72334f03cd339381b1eb6e5a'

