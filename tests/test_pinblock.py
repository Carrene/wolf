import uuid

from nanohttp.contexts import Context
from nanohttp import settings

from wolf import wolf
from wolf.cryptoutil import EncryptedISOPinBlock


class Token:
    def __init__(self, id, bank_id):
        self.id = id
        self.bank_id = bank_id


def test_ISC_pinblock(db):
    with Context(dict()):
        wolf.configure(force=True)
        token = Token(
            id=uuid.UUID('f4f8cc86-abaa-11e9-9550-309c235f7352'),
            bank_id=2,
        )
        pinblock = EncryptedISOPinBlock(token.id.bytes, token.bank_id)
        assert pinblock.encode('7110').decode() == '06D3CE0C710B25D9'


_configuration = '''
    pinblock:
      algorithm: pouya
'''

def test_pouya_pinblock(db):
    with Context(dict()):
        settings.merge(_configuration)
        token = Token(
            id=uuid.UUID('f4f8cc86-abaa-11e9-9550-309c235f7352'),
            bank_id=8,
        )
        pinblock = EncryptedISOPinBlock(
            tokenid=b'6280231400751318',
            bankid=token.bank_id,
            key=b'1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C1C'
        )
        assert pinblock.encode('8224152').decode() == '3FDB435915A061DF'

