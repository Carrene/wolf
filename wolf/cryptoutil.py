import os
import binascii
import base64
import hashlib
import io
import hmac

from Crypto.Cipher import DES3
from nanohttp import settings


def random(size):  # pragma: no cover
    # This function is trying to be a secure random and it will be improved
    # later.
    return os.urandom(size)


class PlainISO0PinBlock:
    """
    http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/

    """
    def __init__(self, token, length=4):
        digest = hmac.new(self.key, token.id.bytes, hashlib.sha1).digest()
        offset = digest[-1] & 0xf

        self.pan = str(
            ((digest[offset + 1] & 0xff) << 16) |
            ((digest[offset + 2] & 0xff) << 8)
        ).zfill(length)[-length:]

    def encode(self, data):
        return b'%0.16x' % (
            int(self.pan) ^ int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16)
        )

    def decode(self, encoded):
        block = b'%0.16x' % (int(self.pan) ^ int(encoded, 16))
        return block[2:2+int(block[:2])]


class EncryptedISOPinBlock(PlainISO0PinBlock):

    def __init__(self, token, key=None):
        bank_id = token.bank_id

        self.key = \
            binascii.unhexlify(key or settings.pinblock[bank_id].key)

        super().__init__(token)

    def create_algorithm(self):
        return DES3.new(self.key, DES3.MODE_ECB)

    def encode(self, data):
        pinblock = super().encode(data)
        des_algorithm = self.create_algorithm()
        encrypted = des_algorithm.encrypt(binascii.unhexlify(pinblock))
        return binascii.hexlify(encrypted).upper()

    def decode(self, encoded):
        algorithm = self.create_algorithm()
        if len(encoded) % 2 != 0:
            raise ValueError('Odd-length string')
        pinblock = algorithm.decrypt(binascii.unhexlify(encoded))
        return super().decode(binascii.hexlify(pinblock).upper())

