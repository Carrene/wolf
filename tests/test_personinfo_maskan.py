import os
from contextlib import contextmanager

import pytest
from nanohttp import RegexRouteController, action, settings
from restfulpy.mockup import MockupApplication, mockup_http_server

from wolf.backends import MaskanClient
from wolf.exceptions import MaskanInvalidSessionIdError, \
    MaskanRepetitiousRequestNumberError, \
    MaskanInvalidRequestTimeError, MaskanInvalidDigitalSignatureError, \
    MaskanUserNotPermitedError, MaskanPersonNotFoundError, \
    MaskanIncompleteParametersError, MaskanMiscellaneousError
from .helpers import LocalApplicationTestCase


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
                ('', self.get_person_info),
            ])

        @action
        def get_person_info(self):
            message_id = 0
            if _maskan_status == 'invalid session id':
                message_id = 1

            elif _maskan_status == 'invalid request number':
                message_id = 2

            elif _maskan_status == 'invalid request time':
                message_id = 3

            elif _maskan_status == 'invalid digital signature':
                message_id = 4

            elif _maskan_status == 'invalid permited':
                message_id = 5

            elif _maskan_status == 'person not found':
                message_id = 6

            elif _maskan_status == 'incomplete parameters':
                message_id = 10

            elif _maskan_status == 'miscellaneous error':
                message_id = 11

            response = f'''<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope
                xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
                <soap:Body>
                <getIndividualPersonInfoResponse>
                <return>
                <messageDescription></messageDescription>
                <messageId>{message_id}</messageId>
                <numberValue></numberValue>
                <objectValue>
                <customerCode>1</customerCode>
                <family>test family</family>
                <mobileNumber>09123456789</mobileNumber>
                <name>test name</name>
                <nationalId>1</nationalId>
                </objectValue>
                </return>
                </getIndividualPersonInfoResponse>
                </soap:Body>
                </soap:Envelope>'''

            return response

    app = MockupApplication('maskan-mockup', MaskanMockupSoap())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
          maskan_web_service:
             person_info:
               test_url: {url}
        ''')
        yield app


class TestPersonInfoMaskan(LocalApplicationTestCase):
    def test_person_info(self):
        customer_code = '1'
        session_id = '0123456789ABCDEF'
        signature = os.urandom(20)
        datetime = '1398/04/06 09:00:00'
        request_number = 1

        with maskan_mockup_server():
            response = MaskanClient().get_person_info(
                customer_code,
                session_id,
                signature,
                datetime,
                request_number
            )

            assert 'customer_code' in response
            assert 'national_id' in response
            assert 'name' in response
            assert 'family' in response
            assert 'mobile' in response
            assert response['customer_code'] == '1'
            assert response['national_id'] == '1'
            assert response['name'] == 'test name'
            assert response['family'] == 'test family'
            assert response['mobile'] == '09123456789'

            with maskan_status('invalid session id'), \
                pytest.raises(MaskanInvalidSessionIdError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('invalid request number'), \
                pytest.raises(MaskanRepetitiousRequestNumberError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('invalid request time'), \
                pytest.raises(MaskanInvalidRequestTimeError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('invalid digital signature'), \
                pytest.raises(MaskanInvalidDigitalSignatureError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('invalid permited'), \
                pytest.raises(MaskanUserNotPermitedError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('person not found'), \
                pytest.raises(MaskanPersonNotFoundError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('incomplete parameters'), \
                pytest.raises(MaskanIncompleteParametersError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

            with maskan_status('miscellaneous error'), \
                pytest.raises(MaskanMiscellaneousError):
                assert MaskanClient().get_person_info(
                    customer_code,
                    session_id,
                    signature,
                    datetime,
                    request_number
                )

