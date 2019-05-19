import time
import socket
import threading

import pytest
import pymlconf
from nanohttp import settings
from nanohttp.configuration import configure

from wolf.iso8583 import listen


TEST_CONFIGURATION = '''
    iso8583:
        backlog: 1
'''


@pytest.fixture
def free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((socket.gethostname(), 0))
        return s.getsockname()[1]
    finally:
        s.close()


@pytest.fixture
def run_iso8583_server(free_port):
    time.sleep(1)
    try:
        settings.merge(TEST_CONFIGURATION)
    except pymlconf.ConfigurationNotInitializedError:
        configure(TEST_CONFIGURATION)

    thread = threading.Thread(
        target=listen,
        args=('localhost', free_port),
        daemon=True
    )
    def wrapper(*args, **kw):
        thread.start()
        return 'localhost', free_port
    yield wrapper
    thread.join(1)

