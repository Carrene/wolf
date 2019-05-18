import socket

import pytest


def test_iso8583_server(run_iso8583_server):
    host, port = run_iso8583_server()
    print(host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(b'Hello, world')

