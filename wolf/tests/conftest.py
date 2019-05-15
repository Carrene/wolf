import time
import socket

import pytest


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
    def wrapper(*args, **kw):
        terminate = quickstart(*args, block=False, port=free_port, **kw)
        time.sleep(.1)
        return f'http://localhost:{free_port}'
    yield wrapper

