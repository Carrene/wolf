import binascii
import socket
import time
from datetime import datetime, timedelta

from iso8583.models import Envelope

from wolf.cryptoutil import EncryptedISOPinBlock
from wolf.models import Cryptomodule, Token
from wolf.tests.helpers import TimeMonkeyPatch, LocalApplicationTestCase


REQUEST = \
    b'018111006030454008C110011662802314007513596700007632451906021427545312' \
    b'61050061317C302531200000035192909999402000009999402   026CIF0121110000' \
    b'90389TKR002076407B83C0150032543FF823602365CDE'


MACKEY = binascii.unhexlify(b'1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C')


class TestTCPServerVerify(LocalApplicationTestCase):

    __configuration__ = '''
      oath:
        window: 10

      pinblock:
        2:
          key: 1234567890ABCDEF1234567890ABCDEF
        3:
          key: 1234567890ABCDEF1234567890ABCDEF
    '''

    @classmethod
    def mockup(cls):
        session = cls.create_session()
        cls.active_token = active_token = Token()
        active_token.name = '6280231400751359'
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
        deactivated_token.name = 'DeactivatedToken'
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
        cls.valid_otp_token1_time1 = cls.pinblock.encode('7110').decode()
        cls.invalid_otp_token1_time1 = cls.pinblock.encode('123456').decode()

    def test_verify(self, run_iso8583_server):
        host, port = run_iso8583_server()

        real_time = time.time
        with TimeMonkeyPatch(self.valid_time), \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) \
                as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall(REQUEST)
            length_message = client_socket.recv(4)
            message = length_message + client_socket.recv(int(length_message))

        envelope = Envelope.loads(message, MACKEY)

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

