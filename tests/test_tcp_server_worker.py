import binascii
import socket

from iso8583.models import Envelope
from nanohttp import settings

from wolf.iso8583 import ISOFIELD_RESPONSECODE
from .helpers import LocalApplicationTestCase


class TestTCPServer(LocalApplicationTestCase):

    def test_worker(self, iso8583_server):
        host, port = iso8583_server
        malformed_message = b'00101234567890'
        mackey = binascii.unhexlify(settings.iso8583.mackey)

        # Trying to pass with malformed message
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(malformed_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, mackey)

            assert envelope.mti == 1110
            assert envelope[ISOFIELD_RESPONSECODE].value == b'928'

        # Trying to pass without message length
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(b'Invalid message length')
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, mackey)

            assert envelope.mti == 1110
            assert envelope[ISOFIELD_RESPONSECODE].value == b'928'

