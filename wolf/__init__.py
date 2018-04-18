from os.path import join, dirname

from restfulpy import Application as BaseApplication

from .authentication import Authenticator
from . import basedata
from .controllers.root import Root
from .cli import PinBlockLauncher, ConfigLauncher


__version__ = '0.20.2b4'


class Application(BaseApplication):
    __authenticator__ = Authenticator()

    builtin_configuration = """
    db:
      url: postgresql://postgres:postgres@localhost/wolf
      test_url: postgresql://postgres:postgres@localhost/wolf_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    token:
      max_consecutive_tries: 5

      seed:
        max_random_try: 3
        min_sleep_milliseconds: 10
        max_sleep_milliseconds: 50

    oath:
      window: 2

    pinblock:
      key: 1234567890ABCDEF1234567890ABCDEF

    """

    def __init__(self):
        super().__init__(
            'wolf',
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    # noinspection PyArgumentList
    def insert_basedata(self):
        basedata.insert()

    # noinspection PyMethodMayBeStatic
    def register_cli_launchers(self, subparsers):
        """
        This is a template method
        """
        PinBlockLauncher.register(subparsers)
        ConfigLauncher.register(subparsers)

wolf = Application()
