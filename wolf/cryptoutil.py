import os
import binascii

from Crypto.Cipher import AES, DES3
from nanohttp import settings


def random(size):
    # This function is trying to be a secure random and it will be improved later.
    return os.urandom(size)


def pad(contents, block_size=16):
    remaining_bytes = len(contents) % block_size
    padding_bytes = block_size - remaining_bytes
    return contents + padding_bytes * bytes([padding_bytes])


def aes_encrypt(content, secret):
    # FIXME: rename it to aes_encrypt and add iv
    iv = random(AES.block_size)
    cipher = AES.new(secret, AES.MODE_CBC, iv)
    content = pad(content, block_size=AES.block_size)
    return iv + cipher.encrypt(content)


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

