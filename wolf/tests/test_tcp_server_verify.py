import binascii
import socket
import time
from datetime import datetime, timedelta

from iso8583.cryptohelpers import iso9797_mac
from iso8583.models import Envelope
from nanohttp import settings

from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import TimeMonkeyPatch, LocalApplicationTestCase


class TestTCPServerVerify(LocalApplicationTestCase):

    __configuration__ = '''
      oath:
        window: 10

    '''

    @classmethod
    def mockup(cls):
        card_number = '6280231400751359'
        session = cls.create_session()
        cls.active_token = active_token = Token()
        active_token.name = card_number
        active_token.phone = 1
        active_token.bank_id = 2
        active_token.expire_date = datetime.now() + timedelta(minutes=1)
        active_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        active_token.is_active = True

        mockup_cryptomodule_length_4 = Cryptomodule()
        active_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(active_token)

        cls.deactivated_token = deactivated_token = Token()
        deactivated_token.name = '6280231234567890'
        deactivated_token.phone = 2
        deactivated_token.bank_id = 2
        deactivated_token.expire_date = datetime.now() + timedelta(minutes=1)
        deactivated_token.seed = \
            b'u*1\'D\xb9\xcb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(deactivated_token)
        session.commit()

        cls.pinblock = EncryptedISOPinBlock(active_token)
        cls.valid_time = 10001000
        cls.invalid_time = 123456

        message = \
            b'018111006030454008C1100116%s6700007632451906021427545312610500' \
            b'61317C302531200000035192909999402000009999402   026CIF01211100' \
            b'0090389TKR00207'

        cls.valid_pin_message = message % card_number.encode()
        cls.valid_pin_message += cls.pinblock.encode('7110')
        cls.valid_pin_message += binascii.hexlify(iso9797_mac(
            cls.valid_pin_message[4:],
            binascii.unhexlify(settings.iso8583.mackey))
        ).upper()

        cls.invalid_pin_message = message % card_number.encode()
        cls.invalid_pin_message += cls.pinblock.encode('1234')
        cls.invalid_pin_message += binascii.hexlify(iso9797_mac(
            cls.invalid_pin_message[4:],
            binascii.unhexlify(settings.iso8583.mackey))
        ).upper()

        cls.invalid_card_number_message = message % b'1234567890123456'
        cls.invalid_card_number_message += cls.pinblock.encode('7110')
        cls.invalid_card_number_message += binascii.hexlify(iso9797_mac(
            cls.invalid_card_number_message[4:],
            binascii.unhexlify(settings.iso8583.mackey))
        ).upper()

        cls.block_user_message = message % b'6280231234567890'
        cls.block_user_message += cls.pinblock.encode('7110')
        cls.block_user_message += binascii.hexlify(iso9797_mac(
            cls.block_user_message[4:],
            binascii.unhexlify(settings.iso8583.mackey))
        ).upper()

    def test_verify(self, iso8583_server):
        host, port = iso8583_server

        real_time = time.time
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

            envelope = Envelope.loads(
                message,
                binascii.unhexlify(settings.iso8583.mackey)
            )

            assert envelope.mti == 1110
            assert envelope[2].value == b'6280231400751359'
            assert envelope[3].value == b'670000'
            assert envelope[11].value == b'763245'
            assert envelope[12].value == b'190602142754'
            assert envelope[18].value == b'5312'
            assert envelope[22].value == b'61050061317C'
            assert envelope[24].value == b'302'
            assert envelope[26].value == b'5312'
            assert envelope[37].value == b'000000351929'
            assert envelope[39].value == b'000'
            assert envelope[41].value == b'09999402'
            assert envelope[42].value == b'000009999402   '
            assert envelope[48].value == b'CIF012111000090389TKR00207'
            assert binascii.hexlify(envelope[64].value).decode().upper() \
                == 'B18300E3FE2A4044'

            assert 52 not in envelope

        # Verifying a valid code within invalid time span
        with TimeMonkeyPatch(self.invalid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

            envelope = Envelope.loads(
                message,
                binascii.unhexlify(settings.iso8583.mackey)
            )

            assert envelope.mti == 1110
            assert envelope[2].value == b'6280231400751359'
            assert envelope[3].value == b'670000'
            assert envelope[11].value == b'763245'
            assert envelope[12].value == b'190602142754'
            assert envelope[18].value == b'5312'
            assert envelope[22].value == b'61050061317C'
            assert envelope[24].value == b'302'
            assert envelope[26].value == b'5312'
            assert envelope[37].value == b'000000351929'
            assert envelope[39].value == b'117'
            assert envelope[41].value == b'09999402'
            assert envelope[42].value == b'000009999402   '
            assert envelope[48].value == b'CIF012111000090389TKR00207'
            assert binascii.hexlify(envelope[64].value).decode().upper() \
                == '19120F147C6975B5'

            assert 52 not in envelope

        # Trying to pass with invalid pinblock
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.invalid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

            envelope = Envelope.loads(
                message,
                binascii.unhexlify(settings.iso8583.mackey)
            )

            assert envelope.mti == 1110
            assert envelope[2].value == b'6280231400751359'
            assert envelope[3].value == b'670000'
            assert envelope[11].value == b'763245'
            assert envelope[12].value == b'190602142754'
            assert envelope[18].value == b'5312'
            assert envelope[22].value == b'61050061317C'
            assert envelope[24].value == b'302'
            assert envelope[26].value == b'5312'
            assert envelope[37].value == b'000000351929'
            assert envelope[39].value == b'117'
            assert envelope[41].value == b'09999402'
            assert envelope[42].value == b'000009999402   '
            assert envelope[48].value == b'CIF012111000090389TKR00207'
            assert binascii.hexlify(envelope[64].value).decode().upper() \
                == '19120F147C6975B5'

            assert 52 not in envelope

        # Trying to pass with deactive token
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.block_user_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

            envelope = Envelope.loads(
                message,
                binascii.unhexlify(settings.iso8583.mackey)
            )

            assert envelope.mti == 1110
            assert envelope[2].value == b'6280231234567890'
            assert envelope[3].value == b'670000'
            assert envelope[11].value == b'763245'
            assert envelope[12].value == b'190602142754'
            assert envelope[18].value == b'5312'
            assert envelope[22].value == b'61050061317C'
            assert envelope[24].value == b'302'
            assert envelope[26].value == b'5312'
            assert envelope[37].value == b'000000351929'
            assert envelope[39].value == b'106'
            assert envelope[41].value == b'09999402'
            assert envelope[42].value == b'000009999402   '
            assert envelope[48].value == b'CIF012111000090389TKR00207'
            assert binascii.hexlify(envelope[64].value).decode().upper() \
                == 'E9A64AE158750007'

            assert 52 not in envelope

        # Trying to pass with invalid function code
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            envelope = Envelope(
                '0200',
                binascii.unhexlify(settings.iso8583.mackey)
            )
            envelope.set(24, b'222')
            client_socket.connect((host, port))
            client_socket.sendall(envelope.dumps())
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

            envelope = Envelope.loads(
                message,
                binascii.unhexlify(settings.iso8583.mackey)
            )

            assert envelope.mti == 210
            assert envelope[24].value == b'222'
            assert envelope[39].value == b'928'

