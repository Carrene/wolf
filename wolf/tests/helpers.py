import time
from os import path

from restfulpy.testing import ApplicableTestCase
from restfulpy.principal import JwtPrincipal

from wolf import cryptoutil, Wolf
from wolf.models import Token

HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Wolf
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'markdown')
    __metadata__ = {
        r'^/apiv1/tokens.*': Token.json_metadata()['fields']
    }

    def login_as_switchcard(self, token=None):
        self._authentication_token = token or JwtPrincipal(dict(
            initial=True,
            platform='TEST',
            version='0.1.0'
        )).dump().decode()


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
    __stack = []

    def __init__(self, fake_time):
        self.fake_time = fake_time

    def __enter__(self):
        self.__stack.append(time.time)
        time.time = lambda: self.fake_time
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        time.time = self.__stack.pop()

