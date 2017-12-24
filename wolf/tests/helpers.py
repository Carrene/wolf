import time
import uuid

from nanohttp import settings
from restfulpy.principal import JwtPrincipal
from restfulpy.testing import ModelRestCrudTestCase

from wolf import wolf, cryptoutil
from wolf.models import Token


class WebTestCase(ModelRestCrudTestCase):
    application = wolf

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge('''
            db: 
              administrative_url: postgresql://postgres:postgres@localhost/postgres
              test_url: postgresql://postgres:postgres@localhost/wolf_test

            logging:
              handlers:
                console:
                  level: warning
        ''')

    def login_as_device_manager(self):
        self.wsgi_app.jwt_token = self.create_jwt_principal('device_manager').dump().decode()

    def login_as_provider(self):
        self.wsgi_app.jwt_token = self.create_jwt_principal('provider').dump().decode()

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


class TokenCounterMonkeyPatch:
    """
    For faking token counter
    """

    def __init__(self, session, token_id, fake_counter):
        self.session = session
        self.token_id = token_id
        self.fake_counter = fake_counter

    def _fetch_token(self):
        return self.session.query(Token).filter(Token.id == self.token_id).one_or_none()

    def __enter__(self):
        token = self._fetch_token()
        self.real_counter = token.counter
        token.counter = self.fake_counter
        self.session.commit()
        return self

    def set_fake_counter(self, fake_counter):
        self.fake_counter = fake_counter
        token = self._fetch_token()
        token.counter = fake_counter
        self.session.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        token = self._fetch_token()
        token.counter = self.real_counter
        self.session.commit()
