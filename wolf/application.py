from os.path import dirname

from restfulpy import Application
from restfulpy.cryptography import AESCipher

from .cli import PinBlockLauncher
from .controllers import Root


class Wolf(Application):
    __configuration_cipher__ = AESCipher(b'ced&#quevbot2(Sc')
    __configuration__ = '''
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

    '''

    def __init__(self, application_name='wolf'):
        from wolf import __version__
        super().__init__(
            application_name,
            root=Root(),
            root_path=dirname(__file__),
            version=__version__
        )

    def insert_basedata(self):
        from . import basedata
        basedata.insert()

    def insert_mockup(self, args=[]):
        from . import mockup
        mockup.insert(*args)

    def register_cli_launchers(self, subparsers):
        PinBlockLauncher.register(subparsers)

