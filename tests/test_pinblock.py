import uuid

from nanohttp import settings

from wolf import wolf
from wolf.cryptoutil import EncryptedISOPinBlock


class Token:
    def __init__(self, id, bank_id):
        self.id = id
        self.bank_id = bank_id


def test_ISC_pinblock():
    wolf.configure(force=True)
    pinblock = EncryptedISOPinBlock(
        pan=uuid.UUID('f4f8cc86-abaa-11e9-9550-309c235f7352').bytes,
        bankid=2
    )
    assert pinblock.encode('7110').decode() == '06D3CE0C710B25D9'


def test_pouya_pinblock():
    _configuration = '''
        pinblock:
          algorithm: pouya
    '''
    settings.merge(_configuration)
    pinblock = EncryptedISOPinBlock(
        pan=b'6280231400751318',
        bankid=8,
        key='1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C'
    )
    assert pinblock.encode('1234567').decode() == 'C5C37BB0192D007C'
    assert pinblock.decode('C5C37BB0192D007C').decode() == '1234567'

    assert pinblock.encode('8224152').decode() == '3FDB435915A061DF'
    assert pinblock.decode('3FDB435915A061DF').decode() == '8224152'

    assert pinblock.encode('7654321').decode() == '9A9ADB0992707AC3'
    assert pinblock.decode('9A9ADB0992707AC3').decode() == '7654321'

