import base64

import requests
from nanohttp import settings, HTTPKnownStatus
from restfulpy.logging_ import get_logger

from .exceptions import DeviceNotFoundError, SSMInternalError, \
    SSMIsNotAvailableError


logger = get_logger()


class LionClient:

    def __init__(self):
        self.base_url = f'{settings.ssm.url}/apiv1'

    def _request(self, key, verb, data):
        try:
            response = requests.request(
                verb,
                f'{self.base_url}/keys/{key}',
                data=data
            )
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

    def encrypt(self, phone, data):
        data = base64.encodebytes(data)
        response = self._request(str(phone), 'ENCRYPT', dict(data=data))
        return base64.decodebytes(response.json().encode())

    def checksum(self, phone, data):
        response = self._request(str(phone), 'CHECKSUM', dict(data=data))
        return response.json()

