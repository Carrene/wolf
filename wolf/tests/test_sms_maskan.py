from contextlib import contextmanager

import pytest
from nanohttp import settings, action, RegexRouteController
from restfulpy.mockup import mockup_http_server, MockupApplication

from wolf.helpers import MaskanSmsProvider
from wolf.tests.helpers import LocalApplicationTestCase
from wolf.exceptions import MaskanSendSmsError


_maskan_status = 'idle'


@contextmanager
def maskan_status(status):
    global _maskan_status
    _maskan_status = status
    yield
    _maskan_status = 'idle'


@contextmanager
def maskan_mockup_server():
    class MaskanMockupSoap(RegexRouteController):
        def __init__(self):
            super().__init__([
                ('', self.send_sms),
            ])

        @action
        def send_sms(self):
            result = 1 if _maskan_status == 'idle' else 0
            response = f'''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope
                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                <SendSMS_SingleResponse>
                <SendSMS_SingleResult>{result}</SendSMS_SingleResult>
                </SendSMS_SingleResponse>
                </soap:Body>
                </soap:Envelope>'''

            return response

    app = MockupApplication('maskan-mockup', MaskanMockupSoap())
    with mockup_http_server(app) as (server, url):
        global _sms_service_url
        settings.merge(f'''
          maskan_web_service:
            sms:
              test_url: {url}
        ''')
        yield app


class TestMaskanSmsProvider(LocalApplicationTestCase):
    def test_maskan_provider(self):
        with maskan_mockup_server():
            response = MaskanSmsProvider().send(
                '09187710445',
                'test message',
            )

            assert response == None

            with maskan_status('Sms is not sending error'), \
                pytest.raises(MaskanSendSmsError):
                assert MaskanSmsProvider().send(
                    '09187710445',
                    'test message',
                )

