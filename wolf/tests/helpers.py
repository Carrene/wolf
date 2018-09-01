import time
from os import path

from restfulpy.testing import ApplicableTestCase

from wolf import cryptoutil, Wolf

HERE = path.abspath(path.dirname(__file__))
DATA_DIRECTORY = path.abspath(path.join(HERE, '../../data'))


class LocalApplicationTestCase(ApplicableTestCase):
    __application_factory__ = Wolf
    __story_directory__ = path.join(DATA_DIRECTORY, 'stories')
    __api_documentation_directory__ = path.join(DATA_DIRECTORY, 'documents')


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

