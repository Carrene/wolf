import hashlib
import urllib

from nanohttp import settings

from .exceptions import MaskanUsernamePasswordError, MaskanVersionNumberError
from .helpers import create_soap_client


class MaskanAuthenticator:
    def __init__(self):
        self.configuration = settings.maskan_web_service.login
        self.version_number = str(self.configuration.version_number)
        self.username = str(self.configuration.username)
        self.password = self._hash_password(
            self.username.encode(),
            str(self.configuration.password).encode()
        ) \
        .upper()
        self.wsdl = self.configuration.url

    @classmethod
    def _hash_password(cls, username, password):
        hashed_password = hashlib.md5()
        hashed_password.update(username)
        hashed_password.update(b'/')
        hashed_password.update(password)
        return hashed_password.hexdigest()

    def login(self):
        client = create_soap_client(self.wsdl)

        if hasattr(self.configuration, 'test_url'):
            client.wsdl.services['LoginService'] \
                .ports['LoginServicePort'] \
                .binding_options['address'] = self.configuration.test_url

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

