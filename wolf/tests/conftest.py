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
        return 'localhost', free_port
    yield wrapper

