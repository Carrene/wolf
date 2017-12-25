from os.path import join, dirname

from restfulpy import Application as BaseApplication

from wolf import basedata
from wolf.controllers.root import Root

__version__ = '0.13.0-dev.5'


class Application(BaseApplication):
    builtin_configuration = """
    db: 
      url: postgresql://postgres:postgres@localhost/wolf
      test_url: postgresql://postgres:postgres@localhost/wolf_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres
      
    token:
      max_consecutive_tries: 5
      
      seed:
        max_random_try: 3
        min_sleep_millis: 10
        max_sleep_millis: 50
      
    oath:
      window: 2

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


wolf = Application()
