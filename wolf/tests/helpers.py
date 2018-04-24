import time
from collections import namedtuple
from os import path, pardir, makedirs

from nanohttp import settings
from restfulpy.documentary import FileDocumentaryMiddleware, RestfulpyApplicationTestCase
from restfulpy.testing import WebAppTestCase
from bddrest.authoring import given, response, Composer

from wolf import cryptoutil, wolf


HERE = path.abspath(path.dirname(__file__))

roles = namedtuple('roles', ['provider', 'device_manager'])('provider', 'DeviceManager')


class BDDTestClass(WebAppTestCase):
    application = wolf

    @classmethod
    def configure_app(cls):
        super().configure_app()
        settings.merge("""
            messaging:
              default_messenger: restfulpy.testing.MockupMessenger
            logging:
              loggers:
                default:
                  level: debug
            """)


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

    @classmethod
    def get_spec_filename(cls, story: Composer):
        filename = f'{story.base_call.verb}-{story.base_call.url.split("/")[2]}({story.title})'
        target = path.abspath(path.join(HERE, '../../data/specifications'))
        if not path.exists(target):
            makedirs(target, exist_ok=True)
        filename = path.join(target, f'{filename}.yml')
        return filename

    @classmethod
    def get_markdown_filename(cls, story: Composer):
        filename = f'{story.base_call.verb}-{story.base_call.url.split("/")[2]}({story.title})'
        target = path.abspath(path.join(HERE, '../../data/documentation'))
        if not path.exists(target):
            makedirs(target, exist_ok=True)
        filename = path.join(target, f'{filename}.md')
        return filename

    def logout(self):
        self.wsgi_app.jwt_token = ''

    def given(self, *args, **kwargs):
        if self.wsgi_app.jwt_token:
            headers = kwargs.setdefault('headers', [])
            headers.append(('AUTHORIZATION', self.wsgi_app.jwt_token))
        return given(
            self.application,
            autodump=self.get_spec_filename,
            autodoc=self.get_markdown_filename,
            *args,
            **kwargs
        )


# FIXME: remove it
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
