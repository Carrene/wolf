import binascii
import socket
from contextlib import contextmanager

from iso8583.models import Envelope
from nanohttp import settings, RegexRouteController, json, context, HTTPStatus
from restfulpy.mockup import MockupApplication, mockup_http_server

from wolf.models import Cryptomodule
from wolf.tests.helpers import LocalApplicationTestCase


_lion_status = 'idle'


@contextmanager
def lion_mockup_server():
    class Root(RegexRouteController):
        def __init__(self):
            super().__init__([
                (r'/apiv1/keys/(?P<keyname>\w+)', self.encrypt),
            ])

        @json(verbs=['encrypt'])
        def encrypt(self, keyname):
            if _lion_status != 'idle':
                raise HTTPStatus(_lion_status)

            checksum_length = int(context.form.get('checksumLength', '0'))
            assert checksum_length == 4

            return \
                'Ro4WsXckQscBovDEaOH3IrQHQeFNfu_7pxe54MgeQz33UbtMiLgKDYx3_46' \
                'aVoe6JDhWhYHna31YG-_W6D0L0g=='

    app = MockupApplication('lion-mockup', Root())
    with mockup_http_server(app) as (server, url):
        settings.merge(f'''
          ssm:
            url: {url}
        ''')
        yield app


@contextmanager
def lion_status(status):
    global _lion_status
    _lion_status = status
    yield
    _lion_status = 'idle'


REQUEST = \
    b'027111006030050008E100011662802314007513' \
    b'5966000076242719052313153821140121124410' \
    b'191431376242701111102000001111102   65\xc8\xc7' \
    b'\xe4\xdf \xe3\xd3\xdf\xe4             \xca\xe5' \
    b'\xd1\xc7\xe4        THRIR00' \
    b'00011234567890070212290073P13006762427CI' \
    b'F012111001209483PHN01109121902288TKT003S' \
    b'FTTOK003000TKR0020272CCB6661787BFE6'


MACKEY = binascii.unhexlify(b'1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C')


class TestEnsureMaskan(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        session = cls.create_session()

        cryptomodule1 = Cryptomodule()
        session.add(cryptomodule1)

        cryptomodule2 = Cryptomodule()
        session.add(cryptomodule2)
        session.commit()

    def test_iso8583_server(self, run_iso8583_server):
        host, port = run_iso8583_server()

        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(REQUEST)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

        envelope = Envelope.loads(message, MACKEY)

        assert envelope.mti == 1110
        assert envelope[2].value == b'6280231400751359'
        assert envelope[3].value == b'660000'
        assert envelope[11].value == b'762427'
        assert envelope[12].value == b'190523131538'
        assert envelope[22].value == b'211401211244'
        assert envelope[24].value == b'101'
        assert envelope[37].value == b'914313762427'
        assert envelope[41].value == b'01111102'
        assert envelope[42].value == b'000001111102   '
        assert envelope[48].value \
            == b'P13006762427CIF012111001209483PHN01109121902288TKT003SFT' \
            b'TOK003000TKR00202ACT128468e16b1772442c701a2f0c468e1f722b4074' \
            b'1e14d7eeffba717b9e0c81e433df751bb4c88b80a0d8c77ff8e9a5687ba2' \
            b'438568581e76b7d581befd6e83d0bd2'

        assert binascii.hexlify(envelope[64].value).decode().upper() \
            == 'E86631B4A2BC93A6'

