from os.path import dirname

from restfulpy import Application
from restfulpy.cryptography import AESCipher

from .controllers import Root


class Wolf(Application):
    __configuration_cipher__ = AESCipher(b'ced&#quevbot2(Sc')
    __configuration__ = '''
    process_name: %(process_name)s
    db:
      url: postgresql://postgres:postgres@localhost/wolf
      test_url: postgresql://postgres:postgres@localhost/wolf_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    migration:
      directory: %(root_path)s/migration
      ini: %(root_path)s/alembic.ini

    ssm:
      url: http://localhost:8081

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
        ttl: 60

    oath:
      window: 2

    pinblock:
      2:
        key: 1234567890ABCDEF1234567890ABCDEF
      3:
        key: 1234567890ABCDEF1234567890ABCDEF

    card_tokens:
      1:
        pattern: ^603799
      2:
        pattern: ^636214
      3:
        pattern: ^603769
      4:
        pattern: ^6(03770|39217)
      5:
        pattern: ^627648

    '''

    def __init__(self, application_name='wolf'):
        from wolf import __version__
        super().__init__(
            application_name,
            root=Root(),
            root_path=dirname(__file__),
            version=__version__
        )

    def insert_basedata(self, args):  # pragma: no cover
        from . import basedata
        basedata.insert(*args)

    def insert_mockup(self, args):  # pragma: no cover
        from . import mockup
        mockup.insert(*args)

    def register_cli_launchers(self, subparsers):
        from .cli import PinBlockLauncher, OTPLauncher
        PinBlockLauncher.register(subparsers)
        OTPLauncher.register(subparsers)

