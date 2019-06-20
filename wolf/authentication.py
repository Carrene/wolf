import os
import urllib
import hashlib

import zeep
from nanohttp import settings

from .exceptions import MaskanUsernamePasswordError, MaskanVersionNumberError


class MaskanAuthenticator:
    def __init__(self):
        self.username = '141770'
        self.password = '123456'
        self.password = f'{self.username}/{self.password}'.encode()
        self.version_number = settings.maskan_web_service.login.version_number
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
        client = zeep.Client(self.filename)
        response = client.service.login(
            username=self.username,
            password=self.password,
            versionnumber=self.version_number
        )

        if response.messageId == 1:
            raise MaskanUsernamePasswordError()

        if response.messageId == 2:
            raise MaskanVersionNumberError()

