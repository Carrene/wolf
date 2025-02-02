import uuid
import binascii
import functools

from nanohttp import settings

from wolf import wolf
from wolf.cryptoutil import ISCPinblock, PlainISO0Pinblock, PouyaPinblock


def test_plain_iso_pinblock():
    pinblock = PlainISO0Pinblock(
        pan=binascii.unhexlify(b'0000111111111111')
    )
    assert pinblock.encode('1234') == b'041225EEEEEEEEEE'


def test_ISC_pinblock():
    wolf.configure(force=True)
    pinblock = ISCPinblock(
        tokenid=uuid.UUID('99bcdcf4-a24f-11e9-a099-382c4a0f5138').bytes
    )
    assert pinblock.encode('2379') == b'042327B2717BFBF2'
    assert pinblock.encode('1348976') == b'071316DAE17BFBF2'

    assert pinblock.decode('042327B2717BFBF2') == b'2379'
    assert pinblock.decode('071316DAE17BFBF2') == b'1348976'


def test_pouya_pinblock():
    _configuration = '''
        pinblock:
          algorithm: pouya
    '''
    settings.merge(_configuration)
    pinblock = PouyaPinblock(
        pan=b'6280231400751318',
        key=binascii.unhexlify(b'1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C')
    )
    assert pinblock.encode('1234567') == b'C5C37BB0192D007C'
    assert pinblock.encode('8224152') == b'3FDB435915A061DF'
    assert pinblock.encode('7654321') == b'9A9ADB0992707AC3'

    assert pinblock.decode('9A9ADB0992707AC3') == b'7654321'
    assert pinblock.decode('C5C37BB0192D007C') == b'1234567'
    assert pinblock.decode('3FDB435915A061DF') == b'8224152'

