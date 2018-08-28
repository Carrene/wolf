import base64

import requests
from nanohttp import settings, HTTPKnownStatus
from restfulpy.logging_ import get_logger

from .exceptions import DeviceNotFoundError


logger = get_logger()


class SSMIsNotAvailableError(HTTPKnownStatus):
    status = '801 SSM is not available'


class SSMInternalError(HTTPKnownStatus):
    status = '802 SSM internal error'


class LionClient:

    def __init__(self):
        self.base_url = f'{settings.ssm.url}/apiv1'

    def encrypt(self, keyname, data):
        data = base64.encodebytes(data)
        try:
            response = requests.request(
                'ENCRYPT', f'{self.base_url}/keys/{keyname}',
                data=dict(data=data)
            )
            if response.status_code == 404:
                raise DeviceNotFoundError()

            if response.status_code != 200:
                logger.exception(response.content.decode())
                raise SSMInternalError()

        except requests.RequestException as ex:
            logger.exception(ex)
            raise SSMIsNotAvailableError()

        return base64.decodebytes(response.json().encode())
