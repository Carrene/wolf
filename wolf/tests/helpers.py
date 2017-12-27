import time
import uuid
from collections import namedtuple

from nanohttp import settings
from restfulpy.principal import JwtPrincipal
from restfulpy.testing import ModelRestCrudTestCase
from restfulpy.documentary import FileDocumentaryMiddleware, RestfulpyApplicationTestCase

from wolf import wolf, cryptoutil, Application as Wolf


class DocumentaryMiddleware(FileDocumentaryMiddleware):
    def __init__(self, application):
        directory = settings.documentary.source_directory
        super().__init__(application, directory)


class DocumentaryTestCase(RestfulpyApplicationTestCase):
    documentary_middleware_factory = DocumentaryMiddleware

    @classmethod
    def application_factory(cls):
        app = Wolf()
        app.configure(force=True)
        return app

    def call_as_device_manager(self, *args, **kwargs):
        return super().call(*args, role='DeviceManager', **kwargs)

    def call_as_bank(self, *args, **kwargs):
        return super().call(*args, role='Bank', **kwargs)


class WebTestCase(ModelRestCrudTestCase):
    application = wolf

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge('''
            logging:
              handlers:
                console:
                  level: warning
        ''')

    @classmethod
    def create_jwt_principal(cls, role):
        session_id = str(uuid.uuid4())
        return JwtPrincipal(dict(
            roles=[role],
            sessionId=session_id
        ))


class As:
    provider = 'Provider'
    device_manager = 'DeviceManager'
    everyone = '|'.join((provider, device_manager))


class RandomMonkeyPatch:
    """
    For faking the random function
    """

    fake_random = None

    def __init__(self, fake_random):
        self.__class__.fake_random = fake_random

    @staticmethod
    def random(size):
        return RandomMonkeyPatch.fake_random[:size]

    def __enter__(self):
        self.real_random = cryptoutil.random
        cryptoutil.random = RandomMonkeyPatch.random

    def __exit__(self, exc_type, exc_val, exc_tb):
        cryptoutil.random = self.real_random


class TimeMonkeyPatch:
    """
    For faking time
    """

    def __init__(self, fake_time):
        self.fake_time = fake_time

    def __enter__(self):
        self.real_time = time.time
        time.time = lambda: self.fake_time
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.time = self.real_time


roles = namedtuple('roles', ['provider', 'device_manager'])('provider', 'DeviceManager')
