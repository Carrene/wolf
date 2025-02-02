from contextlib import contextmanager

import pytest
from nanohttp import settings, action, RegexRouteController
from restfulpy.mockup import mockup_http_server, MockupApplication

from wolf.authentication import MaskanAuthenticator
from wolf.exceptions import MaskanUsernamePasswordError, \
    MaskanVersionNumberError
from .helpers import LocalApplicationTestCase


_maskan_status = 'idle'


@contextmanager
def maskan_status(status):
    global _maskan_status
    _maskan_status = status
    yield
    _makan_status = 'idle'


@contextmanager
def maskan_mockup_server():
    class MaskanMockupSoap(RegexRouteController):
        def __init__(self):
            super().__init__([
                ('', self.login),
            ])

        @action
        def login(self):
            if _maskan_status == 'invalid username or password':
                message_id = 1

            elif _maskan_status == 'invalid version number':
                message_id = 2

            else:
                message_id = 0

            string_value = '0123456789ABCDEF'

            response = f'''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope
                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                <loginResponse>
                <return>
                <messageId>{message_id}</messageId>
                <numberValue></numberValue>
                <objectValue></objectValue>
                <stringValue>{string_value}</stringValue>
                </return>
                </loginResponse>
                </soap:Body>
                </soap:Envelope>'''

            return response

    app = MockupApplication('maskan-mockup', MaskanMockupSoap())
    with mockup_http_server(app) as (server, url):
        global _login_service_url
        settings.merge(f'''
          maskan_web_service:
            login:
              test_url: {url}
        ''')
        yield app


class TestMaksanAuthentication(LocalApplicationTestCase):
    def test_login(self):
        with maskan_mockup_server():
            response = \
                MaskanAuthenticator().login()

            assert response == '0123456789ABCDEF'

            with maskan_status('invalid username or password'), \
                pytest.raises(MaskanUsernamePasswordError):
                assert \
                    MaskanAuthenticator().login()

            with maskan_status('invalid version number'), \
                pytest.raises(MaskanVersionNumberError):
                assert \
                    MaskanAuthenticator().login()

