import socket
import threading
import time
from os.path import dirname

import pymlconf
import pytest
from nanohttp import settings
from nanohttp.configuration import configure
from restfulpy.orm import DBSession
from sqlalchemy.orm.session import close_all_sessions

from wolf.application import Wolf
from wolf.iso8583 import listen


context = dict(
    process_name='wolf-tcpserver',
    root_path=dirname(__file__),
)


start_event = threading.Event()


@pytest.fixture
def free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((socket.gethostname(), 0))
        return s.getsockname()[1]

    finally:
        s.close()


@pytest.fixture
def iso8583_server(free_port):
    time.sleep(1)
    try:
        settings.merge(Wolf.__configuration__)

    except pymlconf.ConfigurationNotInitializedError:
        configure(Wolf.__configuration__, context=context)

    thread = threading.Thread(
        target=listen,
        args=('localhost', free_port, start_event),
        daemon=True
    )
    thread.start()
    start_event.wait(1)
    yield 'localhost', free_port
    engine = DBSession.bind
    close_all_sessions()
    engine.dispose()

