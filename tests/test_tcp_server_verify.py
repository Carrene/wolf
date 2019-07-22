import binascii
import socket
import time
from datetime import datetime, timedelta

from iso8583.cryptohelpers import iso9797_mac
from iso8583.models import Envelope
from nanohttp import settings
import redis

from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.models import Cryptomodule, Token
from wolf.iso8583 import ISOFIELD_PAN, ISOFIELD_FUNCTION_CODE, \
    ISOFIELD_RESPONSECODE, ISOFIELD_ADDITIONAL_DATA, ISOFIELD_PIN_BLOCK, \
    ISOFIELD_PROCESS_CODE, ISOFIELD_SYSTEM_TRACE_AUDIT_NUMBER, \
    ISOFIELD_LOCAL_TRANSACTION_TIME, ISOFIELD_MERCHANT_TYPE, \
    ISOFIELD_CONDITION_CODE, ISOFIELD_FUNCTION_CODE, \
    ISOFIELD_CAPTURE_CODE, ISOFIELD_RETRIEVAL_REFERENCE_NUMBER, \
    ISOFIELD_TERMINAL_ID, ISOFIELD_MERCHANT_ID, \
    ISOFIELD_TERMINAL_LOCALTION, ISOFIELD_MAC
from .helpers import TimeMonkeyPatch, LocalApplicationTestCase


class TestTCPServerVerify(LocalApplicationTestCase):
    _redis = None
    __configuration__ = '''
      oath:
        window: 10
      pinblock:
        algorithm: pouya
    '''
    @staticmethod
    def create_blocking_redis_client():
        return redis.StrictRedis(
            host=settings.token.redis.host,
            port=settings.token.redis.port,
            db=settings.token.redis.db,
            password=settings.token.redis.password,
            max_connections=settings.token.redis.max_connections,
            socket_timeout=settings.token.redis.socket_timeout
        )

    @classmethod
    def redis(cls):
        if cls._redis is None:
            cls._redis = cls.create_blocking_redis_client()
        return cls._redis

    def setup(self):
        self.redis().flushdb()

    @classmethod
    def mockup(cls):
        card_number = '6280231400751359'
        cls.mackey = binascii.unhexlify(settings.iso8583.mackey)
        session = cls.create_session()
        cls.active_token = active_token = Token()
        active_token.name = f'{card_number[0:6]}-{card_number[-4:]}-02'
        active_token.phone = 1
        active_token.bank_id = 8
        active_token.expire_date = datetime.now() + timedelta(minutes=1)
        active_token.seed = \
            b'\xda!\x9e\xb6a\xff\x8a9\xf9\x8b\x06\xab\x0b5\xf8h\xf5j\xaaz'
        active_token.is_active = True

        mockup_cryptomodule_length_4 = Cryptomodule()
        active_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(active_token)

        deactivated_card_number = '6280231234567890'
        cls.deactivated_token = deactivated_token = Token()
        deactivated_token.name = '6280231234567890'
        deactivated_token.name = \
            f'{deactivated_card_number[0:6]}-{deactivated_card_number[-4:]}-02'
        deactivated_token.phone = 2
        deactivated_token.bank_id = 8
        deactivated_token.expire_date = datetime.now() + timedelta(minutes=1)
        deactivated_token.seed = \
            b'u*1\'D\xb9\xcb\xa6Z.>\x88j\xbeZ\x9b3\xc6\xca\x84%\x87\n\x89'
        deactivated_token.is_active = False
        deactivated_token.cryptomodule = mockup_cryptomodule_length_4
        session.add(deactivated_token)
        session.commit()

        cls.pinblock = EncryptedISOPinBlock(
            card_number.encode(),
            active_token.bank_id,
        )
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

        cls.malformad_pinblock_message = message % card_number.encode()
        cls.malformad_pinblock_message += b'MALFORMEDPIN0000'
        cls.malformad_pinblock_message += binascii.hexlify(iso9797_mac(
            cls.malformad_pinblock_message[4:],
            binascii.unhexlify(settings.iso8583.mackey))
        ).upper()

        cls.malformed_message = b'00101234567890'

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
            envelope = Envelope.loads(message, self.mackey)

            assert envelope.mti == 1110
            assert envelope[ISOFIELD_PAN].value == b'6280231400751359'
            assert envelope[ISOFIELD_PROCESS_CODE].value == b'670000'
            assert envelope[ISOFIELD_SYSTEM_TRACE_AUDIT_NUMBER].value == \
                b'763245'
            assert envelope[ISOFIELD_LOCAL_TRANSACTION_TIME].value == \
                b'190602142754'
            assert envelope[ISOFIELD_MERCHANT_TYPE].value == b'5312'
            assert envelope[ISOFIELD_CONDITION_CODE].value == b'61050061317C'
            assert envelope[ISOFIELD_FUNCTION_CODE].value == b'302'
            assert envelope[ISOFIELD_CAPTURE_CODE].value == b'5312'
            assert envelope[ISOFIELD_RETRIEVAL_REFERENCE_NUMBER].value == \
                b'000000351929'
            assert envelope[ISOFIELD_RESPONSECODE].value == b'000'
            assert envelope[ISOFIELD_TERMINAL_ID].value == b'09999402'
            assert envelope[ISOFIELD_MERCHANT_ID].value == b'000009999402   '
            assert envelope[ISOFIELD_ADDITIONAL_DATA].value == \
                b'CIF012111000090389TKR00207'
            assert 'B18300E3FE2A4044' == \
                binascii.hexlify(envelope[ISOFIELD_MAC].value) \
                .decode() \
                .upper()

            assert 52 not in envelope

        # Verifying a valid code within invalid time span
        with TimeMonkeyPatch(self.invalid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[ISOFIELD_RESPONSECODE].value == b'117'

        # Trying to pass with invalid pinblock
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.invalid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[ISOFIELD_RESPONSECODE].value == b'117'

        # Trying to pass with deactive token
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.block_user_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[ISOFIELD_RESPONSECODE].value == b'106'

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
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[ISOFIELD_RESPONSECODE].value == b'928'

        # Trying to pass with malformed pinblock
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.malformad_pinblock_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[ISOFIELD_RESPONSECODE].value == b'117'

        # Trying to pass with invalid card number(token not found)
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.invalid_card_number_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope.mti == 1110
            assert envelope[ISOFIELD_RESPONSECODE].value == b'117'

    def test_verify_with_redis(self, iso8583_server):
        settings.token.redis.enabled = True
        host, port = iso8583_server

        real_time = time.time
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope.mti == 1110
            assert envelope[ISOFIELD_PAN].value == b'6280231400751359'
            assert envelope[ISOFIELD_PROCESS_CODE].value == b'670000'
            assert envelope[ISOFIELD_SYSTEM_TRACE_AUDIT_NUMBER].value == \
                b'763245'
            assert envelope[ISOFIELD_LOCAL_TRANSACTION_TIME].value == \
                b'190602142754'
            assert envelope[ISOFIELD_MERCHANT_TYPE].value == b'5312'
            assert envelope[ISOFIELD_CONDITION_CODE].value == b'61050061317C'
            assert envelope[ISOFIELD_FUNCTION_CODE].value == b'302'
            assert envelope[ISOFIELD_CAPTURE_CODE].value == b'5312'
            assert envelope[ISOFIELD_RETRIEVAL_REFERENCE_NUMBER].value == \
                b'000000351929'
            assert envelope[ISOFIELD_RESPONSECODE].value == b'000'
            assert envelope[ISOFIELD_TERMINAL_ID].value == b'09999402'
            assert envelope[ISOFIELD_MERCHANT_ID].value == b'000009999402   '
            assert envelope[ISOFIELD_ADDITIONAL_DATA].value == \
                b'CIF012111000090389TKR00207'
            assert 'B18300E3FE2A4044' == \
                binascii.hexlify(envelope[ISOFIELD_MAC].value) \
                .decode() \
                .upper()
            assert 52 not in envelope

        # Trying again with same pinblock
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(self.valid_pin_message)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))
            envelope = Envelope.loads(message, self.mackey)

            assert envelope[ISOFIELD_RESPONSECODE].value == b'117'

