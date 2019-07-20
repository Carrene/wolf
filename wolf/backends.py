import base64
import urllib
import binascii

import requests
from requests import Request, Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import zeep
from nanohttp import settings, HTTPKnownStatus
from restfulpy.logging_ import get_logger

from .helpers import create_soap_client
from .exceptions import DeviceNotFoundError, SSMInternalError, \
    SSMIsNotAvailableError, MaskanInvalidSessionIdError, \
    MaskanRepetitiousRequestNumberError, MaskanInvalidRequestTimeError, \
    MaskanInvalidDigitalSignatureError, MaskanUserNotPermitedError, \
    MaskanPersonNotFoundError, MaskanIncompleteParametersError, \
    MaskanMiscellaneousError, SSMUnauthorizedError


logger = get_logger()


class FingerprintAdapter(HTTPAdapter):

    def __init__(self, fingerprint=None, **kwargs):
        self.fingerprint = str(fingerprint)
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            assert_fingerprint=self.fingerprint
        )


class LionClient:

    def __init__(self):
        self.base_url = f'{settings.ssm.url}/apiv1'
        self.token = settings.ssm.token

    def send_request(self, *args, **kwargs):
        session = Session()
        session.verify = False
        if settings.ssm.tls.verify:
            session.mount(
                f'{self.base_url}/keys',
                FingerprintAdapter(settings.ssm.tls.fingerprint)
            )

        request = Request(*args, **kwargs)
        prepped = session.prepare_request(request)
        response = session.send(prepped)
        return response

    def encrypt(self, bank_id, phone, data, checksum=4):
        data = base64.urlsafe_b64encode(data)
        parameters = dict(
            data=dict(
                data=data,
                checksumLength=checksum
            ),
            headers={'Authorization': self.token}
        )

        try:
            response = self.send_request(
                'ENCRYPT',
                f'{self.base_url}/keys/{bank_id}{phone}',
                **parameters
            )
            if response.status_code == 401:
                raise SSMUnauthorizedError()

            if response.status_code == 404:
                raise DeviceNotFoundError(f'{bank_id}{phone}')

            if response.status_code == 502:
                raise SSMIsNotAvailableError()

            if response.status_code != 200:
                logger.exception(response.content.decode())
                raise SSMInternalError()

        except requests.RequestException as ex:  # pragma: no cover
            logger.exception(ex)
            raise SSMIsNotAvailableError()
        else:
            return base64.urlsafe_b64decode(response.json().encode())


class MaskanClient:
    def __init__(self):
        self.configuration = settings.maskan_web_service.person_info
        self.wsdl_url = self.configuration.wsdl_url
        self.exceptions = {
            1: MaskanInvalidSessionIdError,
            2: MaskanRepetitiousRequestNumberError,
            3: MaskanInvalidRequestTimeError,
            4: MaskanInvalidDigitalSignatureError,
            5: MaskanUserNotPermitedError,
            6: MaskanPersonNotFoundError,
            10: MaskanIncompleteParametersError,
            11: MaskanMiscellaneousError,
        }

    def get_person_info(
        self,
        customer_code,
        session_id,
        signature,
        datetime,
        request_number
    ):
        client = create_soap_client(self.wsdl_url)
        digital_signature = binascii.hexlify(signature)

        request_data = {
            'customerCode': customer_code,
            'requestNumber': request_number,
            'requestTime': datetime,
            'sessionId': session_id,
            'digitalSignature': digital_signature
        }

        if hasattr(self.configuration, 'test_url'):
            client.wsdl.services['AllAccountsOfPersonService'] \
                .ports['AllAccountsOfPersonServiceSoap12HttpPort'] \
                .binding_options['address'] = self.configuration.test_url

        response = client.service.getIndividualPersonInfo(request_data)
        message_id = int(response.messageId[-2:])

        if message_id != 0:
            exception = self.exceptions[message_id]
            raise exception()

        return {
            'customer_code': response.objectValue.customerCode,
            'national_id': response.objectValue.nationalId,
            'name': response.objectValue.name,
            'family': response.objectValue.family,
            'mobile': response.objectValue.mobileNumber
        }

