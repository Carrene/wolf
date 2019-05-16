import socket

import pytest


def test_iso8583_server(run_iso8583_server):
    host, port = run_iso8583_server()
    print(host, port)

