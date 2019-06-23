import hashlib
import urllib

from nanohttp import settings

from .exceptions import MaskanUsernamePasswordError, MaskanVersionNumberError
from .helpers import create_soap_client


class MaskanAuthenticator:
    def __init__(self):
        configuration = settings.maskan_web_service.login
        self.version_number = str(configuration.version_number)
        self.username = str(configuration.username)
        self.password = self._hash_password(
            self.username.encode(),
            str(configuration.password).encode()
        ) \
        .upper()
        self.filename = urllib.parse.urljoin(
            'file:',
            urllib.request.pathname2url(
                configuration.filename
            )
        )

    @classmethod
    def _hash_password(cls, username, password):
        hashed_password = hashlib.md5()
        hashed_password.update(username)
        hashed_password.update(b'/')
        hashed_password.update(password)
        return hashed_password.hexdigest()

    def login(self):
        client = create_soap_client(self.filename)
        response = client.service.login(
            username=self.username,
            password=self.password,
            versionnumber=self.version_number
        )

        if response.messageId == 1:
            raise MaskanUsernamePasswordError()

        if response.messageId == 2:
            raise MaskanVersionNumberError()

        return response.stringValue

