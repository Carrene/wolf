import os
import urllib
import hashlib

import zeep
from nanohttp import settings

from .exceptions import MaskanUsernamePasswordError, MaskanVersionNumberError
from . import cryptoutil


class MaskanAuthenticator:
    def __init__(self):
        self.version_number = settings.maskan_web_service.login.version_number
        self.username = settings.maskan_web_service.login.username
        self.password = settings.maskan_web_service.login.password
        self.password = cryptoutil.md5_hasher(
            self.username.encode(),
            '/'.encode(),
            self.password.encode()
        ) \
        .hexdigest() \
        .upper()

        self.filename = urllib.parse.urljoin(
            'file:',
            urllib.request.pathname2url(
                settings.maskan_web_service.login.filename
            )
        )

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

