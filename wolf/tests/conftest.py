import time
import socket
import threading
from os.path import dirname

import pytest
import pymlconf
from nanohttp import settings
from nanohttp.configuration import configure

from wolf.iso8583 import listen
from wolf.application import Wolf


context = dict(
    process_name='wolf-tcpserver',
    root_path=dirname(__file__),
)


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
        settings.merge(Wolf.__configuration__)
    except pymlconf.ConfigurationNotInitializedError:
        configure(Wolf.__configuration__, context=context)

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

