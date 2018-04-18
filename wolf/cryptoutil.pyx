import os
import binascii
import base64
import hashlib

from Crypto.Cipher import AES, DES3
from nanohttp import settings


def random(size):
    # This function is trying to be a secure random and it will be improved later.
    return os.urandom(size)


class AESCipher(object):

    def __init__(self, key):
        self.bs = 16
        self.key = key

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = random(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(raw)

    def decrypt(self, enc):
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:]))

    def _pad(self, s):
        remaining_bytes = len(s) % self.bs
        padding_bytes = self.bs - remaining_bytes
        return s + padding_bytes * bytes([padding_bytes])

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


configuration_cipher = AESCipher(b'1234567890ABCDEF')

class PlainISO0PinBlock:
    """
    http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/

    """
    def __init__(self, token_id):
        pan = str(token_id).zfill(16)
        self.pan = int(f'0000{pan[-13:-1]}', 16)

    def encode(self, data):
        return b'%0.16x' % (self.pan ^ int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16))

    def decode(self, encoded):
        block = b'%0.16x' % (self.pan ^ int(encoded, 16))
        return block[2:2+int(block[:2])]


class EncryptedISOPinBlock(PlainISO0PinBlock):

    def __init__(self, token_id, key=None):
        super().__init__(token_id)
        self.key = binascii.unhexlify(key or settings.pinblock.key)

    def create_algorithm(self):
        return DES3.new(self.key, DES3.MODE_ECB)

    def encode(self, data):
        pinblock = super().encode(data)
        des_algorithm = self.create_algorithm()
        encrypted = des_algorithm.encrypt(binascii.unhexlify(pinblock))
        return binascii.hexlify(encrypted).upper()

    def decode(self, encoded):
        algorithm = self.create_algorithm()
        pinblock = algorithm.decrypt(binascii.unhexlify(encoded))
        return super().decode(binascii.hexlify(pinblock).upper())

