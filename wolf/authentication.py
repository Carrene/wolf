import os
import urllib
import hashlib

import suds
from nanohttp import settings

from .exceptions import MaskanAuthenticationError


class MaskanAuthenticator:
    def __init__(self):
        self.username = '141770'
        self.password = '123456'
        self.password = f'{self.username}/{self.password}'.encode()
        self.version_number = settings.maskan_web_service.login.version_number
        self.location = settings.maskan_web_service.login.location
        self.filename = urllib.parse.urljoin(
            'file:',
            urllib.request.pathname2url(
                settings.maskan_web_service.login.filename
            )
        )

        md5_hasher = hashlib.md5()
        md5_hasher.update(self.password)

        self.password = md5_hasher.hexdigest().upper()

    def login(self):
        client = suds.client.Client(url=self.filename, location=self.location)
        response = client.service.login(
            username=self.username,
            password=self.password,
            versionnumber=self.version_number
        )

        if hasattr(response, 'stringValue'):
            return response.stringValue

        raise MaskanAuthenticationError()

