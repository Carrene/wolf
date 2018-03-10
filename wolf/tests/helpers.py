import time
from collections import namedtuple

from nanohttp import settings
from restfulpy.documentary import FileDocumentaryMiddleware, RestfulpyApplicationTestCase
from restfulpy.testing import WebAppTestCase
from bddrest.authoring import given, response

from wolf import cryptoutil, Application as Wolf


roles = namedtuple('roles', ['provider', 'device_manager'])('provider', 'DeviceManager')


class BDDTestClass(WebAppTestCase):
    application = Wolf()

    def login(self, username, password):
        call = dict(
            title='Login',
            description='Login to system as admin',
            url='/apiv1/members',
            verb='LOGIN',
            form={
                'username': username,
                'password': password,
            }
        )
        with self.given(**call):
            self.wsgi_app.jwt_token = response.json['token']

        return username, password

    def logout(self):
        self.wsgi_app.jwt_token = ''

    def given(self, *args, **kwargs):
        if self.wsgi_app.jwt_token:
            headers = kwargs.setdefault('headers', [])
            headers.append(('AUTHORIZATION', self.wsgi_app.jwt_token))
        return given(self.application, *args, **kwargs)


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
        return super().call(*args, role=roles.device_manager, **kwargs)

    def call_as_bank(self, *args, **kwargs):
        return super().call(*args, role=roles.provider, **kwargs)


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
