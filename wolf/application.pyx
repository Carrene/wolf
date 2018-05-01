from os.path import join, dirname

from nanohttp import settings
from restfulpy import Application as BaseApplication
from restfulpy.cryptography import AESCipher

from . import basedata
from .cli import PinBlockLauncher
from .controllers.root import Root


class Application(BaseApplication):
    __configuration_cipher__ = AESCipher(b'ced&#quevbot2(Sc')
    builtin_configuration = """
    db:
      url: postgresql://postgres:postgres@localhost/wolf
      test_url: postgresql://postgres:postgres@localhost/wolf_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    token:
      seed:
        max_random_try: 3
        min_sleep_milliseconds: 10
        max_sleep_milliseconds: 50
      redis:
        enabled: False
        host: localhost
        port: 6379
        password: ~
        db: 0
        max_connections: 10
        socket_timeout: 1
      verify_limit: 1

    oath:
      window: 2

    pinblock:
      key: 1234567890ABCDEF1234567890ABCDEF

    """

    def __init__(self, version):
        super().__init__(
            'wolf',
            root=Root(),
            root_path=dirname(__file__),
            version=version
        )

    # noinspection PyArgumentList
    def insert_basedata(self):
        basedata.insert()

    def insert_mockup(self, args=[]):
        from . import mockup
        mockup.insert(*args)

    # noinspection PyMethodMayBeStatic
    def register_cli_launchers(self, subparsers):
        """
        This is a template method
        """
        PinBlockLauncher.register(subparsers)

    def configure(self, files=None, **kwargs):
        super().configure(**kwargs)
        files = ([files] if isinstance(files, str) else files) or []

        for filename in files:
            with open(filename, 'rb') as f:
                header = f.read(4)
                if header == b'#enc':
                    content = self.__configuration_cipher__.decrypt(f.read())
                else:
                    content = header + f.read()
                settings.merge(content.decode())


