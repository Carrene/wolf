import socket

import pytest


def test_iso8583_server(run_iso8583_server):
    with pytest.raises(NotImplementedError), socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    ) as client_socket:

        print('\033[38;5;206;1msomething')
        port = run_iso8583_server()
        client_socket.connect(('localhost', port))
        client_socket.send('Sample message')

