import base64
import urllib
import binascii

import requests
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


class LionClient:

    def __init__(self):
        self.base_url = f'{settings.ssm.url}/apiv1'
        self.token = settings.ssm.token

    def _request(self, key, verb, data):
        try:
            response = requests.request(
                verb,
                f'{self.base_url}/keys/{key}',
                data=data,
                headers={'Authorization': self.token}
            )

            if response.status_code == 401:
                raise SSMUnauthorizedError()

            if response.status_code == 404:
                raise DeviceNotFoundError(key)

            if response.status_code == 502:
                raise SSMIsNotAvailableError()

            if response.status_code != 200:
                logger.exception(response.content.decode())
                raise SSMInternalError()

        except requests.RequestException as ex:  # pragma: no cover
            logger.exception(ex)
            raise SSMIsNotAvailableError()
        else:
            return response

    def encrypt(self, bank_id, phone, data, checksum=4):
        data = base64.urlsafe_b64encode(data)
        response = self._request(
            f'{bank_id}{phone}',
            'ENCRYPT',
            dict(data=data, checksumLength=checksum)
        )
        return base64.urlsafe_b64decode(response.json().encode())


class MaskanClient:
    def __init__(self):
        self.configuration = settings.maskan_web_service.person_info
        self.wsdl = self.configuration.url
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
        client = create_soap_client(self.wsdl)
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

