import uuid
import binascii
import functools

from nanohttp import settings

from wolf import wolf
from wolf.cryptoutil import ISCPinBlock, PlainISO0PinBlock, PouyaPinBlock


def test_plain_iso_pinblock():
    pinblock = PlainISO0PinBlock(
        pan=b'\x00\x00\x11\x11\x11\x11\x11\x11'
    )
    assert pinblock.encode('1234') == b'\x04\x12%\xee\xee\xee\xee\xee'


def test_ISC_pinblock():
    wolf.configure(force=True)
    pinblock = ISCPinBlock(
        tokenid=uuid.UUID('99bcdcf4-a24f-11e9-a099-382c4a0f5138').bytes
    )
    assert pinblock.encode('2379') == b"=\x06\x9d'\x17\xbf\xbf."  # '042327B2717BFBF2'
    #assert pinblock.encode('1348976') == '071316DAE17BFBF2'


def test_pouya_pinblock():
    _configuration = '''
        pinblock:
          algorithm: pouya
    '''
    settings.merge(_configuration)
    pinblock = PouyaPinBlock(
        pan=b'6280231400751318',
        key=binascii.unhexlify(b'1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C')
    )
    assert pinblock.encode('1234567') == b'C5C37BB0192D007C'
    assert pinblock.decode('C5C37BB0192D007C') == b'1234567'

    assert pinblock.encode('8224152') == b'3FDB435915A061DF'
    assert pinblock.decode('3FDB435915A061DF') == b'8224152'

    assert pinblock.encode('7654321') == b'9A9ADB0992707AC3'
    assert pinblock.decode('9A9ADB0992707AC3') == b'7654321'

