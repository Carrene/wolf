import binascii
import socket
from contextlib import contextmanager
from datetime import date, timedelta

from iso8583.cryptohelpers import iso9797_mac
from iso8583.models import Envelope
from nanohttp import settings, RegexRouteController, json, context, HTTPStatus
from restfulpy.mockup import MockupApplication, mockup_http_server

from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import LocalApplicationTestCase, RandomMonkeyPatch


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



class TestTCPServerEnsure(LocalApplicationTestCase):

    @classmethod
    def mockup(cls):
        cls.mackey = binascii.unhexlify(settings.iso8583.mackey)
        card_number = '6280231400751359'
        message = \
            b'027111006030050008E1000116%s66000076242719052313' \
            b'153821140121124410191431376242701111102000001111102   65' \
            b'\xc8\xc7\xe4\xdf \xe3\xd3\xdf\xe4             \xca\xe5\xd1' \
            b'\xc7\xe4        THRIR0000011234567890070212290073P13006762427C' \
            b'IF012111001209483PHN01109121902288TKT003SFTTOK003000TKR00202'

        cls.valid_message = message % card_number.encode()
        cls.valid_message += binascii.hexlify(iso9797_mac(
            cls.valid_message[4:],
            cls.mackey)
        ).upper()

        cls.duplicate_seed_message = message % b'6280231400751379'
        cls.duplicate_seed_message += binascii.hexlify(iso9797_mac(
            cls.duplicate_seed_message[4:],
            cls.mackey)
        ).upper()

        envelope = Envelope('1100', cls.mackey)
        envelope.set(24, b'101')
        cls.message_without_card_number = envelope.dumps()

        envelope = Envelope('1100', cls.mackey)
        envelope.set(2, b'1234567890123456')
        envelope.set(24, b'101')
        envelope.set(48, b'PHN00211')
        cls.message_with_invalid_card_number = envelope.dumps()

        envelope = Envelope('1100', cls.mackey)
        envelope.set(2, card_number.encode())
        envelope.set(24, b'101')
        cls.message_without_field48 = envelope.dumps()

        envelope = Envelope('1100', cls.mackey)
        envelope.set(2, card_number.encode())
        envelope.set(24, b'101')
        envelope.set(
            48,
            b'P13006762427CIF012111001209483TKT003SFTTOK003000TKR00202'
        )
        cls.message_without_tag_PHN = envelope.dumps()

    def test_ensure(self, iso8583_server):
        host, port = iso8583_server

        # Trying to pass without cryptomodule
        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[39].value == b'909'

        session = self.create_session()
        cryptomodule1 = Cryptomodule()
        session.add(cryptomodule1)

        cryptomodule2 = Cryptomodule()
        session.add(cryptomodule2)
        session.commit()

        # Trying to pass successfully
        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope.mti == 1110
            assert envelope[2].value == b'6280231400751359'
            assert envelope[3].value == b'660000'
            assert envelope[11].value == b'762427'
            assert envelope[12].value == b'190523131538'
            assert envelope[22].value == b'211401211244'
            assert envelope[24].value == b'101'
            assert envelope[37].value == b'914313762427'
            assert envelope[39].value == b'000'
            assert envelope[41].value == b'01111102'
            assert envelope[42].value == b'000001111102   '
            assert envelope[48].value == \
                b'P13006762427CIF012111001209483PHN01109121902288TKT003SFT' \
                b'TOK003000TKR00202ACT128468e16b1772442c701a2f0c468e1f722b' \
                b'40741e14d7eeffba717b9e0c81e433df751bb4c88b80a0d8c77ff8e9' \
                b'a5687ba2438568581e76b7d581befd6e83d0bd2'

            assert binascii.hexlify(envelope[64].value).decode().upper() \
                == 'E86631B4A2BC93A6'

        # Trying to pass without card number
        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.message_without_card_number)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[39].value == b'928'

        # Trying to pass with invalid card number
        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.message_with_invalid_card_number)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[39].value == b'928'

        # Trying to pass without field 48
        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.message_without_field48)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[39].value == b'928'

        # Trying to pass without tag PHN
        with lion_mockup_server(), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.message_without_tag_PHN)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[39].value == b'928'

        seed = b'\xdb!.\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        expired_token = Token()
        expired_token.name = '6280231400751379'
        expired_token.phone = 989122451075
        expired_token.expire_date = date.today() - timedelta(days=1)
        expired_token.seed = seed
        expired_token.is_active = True
        expired_token.cryptomodule = cryptomodule1
        expired_token.bank_id = 1
        session.add(expired_token)
        session.commit()

        # Trying to pass with duplicate seed
        with lion_mockup_server(), \
                RandomMonkeyPatch(seed), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.duplicate_seed_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[39].value == b'909'

