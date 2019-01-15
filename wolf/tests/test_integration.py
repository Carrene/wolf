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
            assert 'AQAC5wYBBDwCYWJjZGVmZ2hpamtsbW5vcHFyc3RhYmNkZWZnaGlqa2x'\
                'tbg==' == context.form['data']

            return \
                'YWJjZGVmZ2hpamtsbW5vcBcFs-AP01FjYg3ZkBUdcvQmGe71FdJcCL7ZT0S'\
                'RvPSeveC5atl6QRELTliO6zTn7g=='


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
                'expireDate': 1550133902,
                'bankId': 2
            }
        ):

            assert status == 200
            result = response.json
            assert 'provisioning' in result
            assert result['expireDate'] == '2019-02-14'
            token = result['provisioning']
            assert token == \
                'mt://oath/totp/6162636465666768696a6b6c6d6e6f701'\
                '705b3e00fd35163620dd990151d72f42619eef515d25c08b'\
                'ed94f4491bcf49ebde0b96ad97a41110b4e588eeb34e7ee'

