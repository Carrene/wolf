import os
import binascii
import base64
import hashlib
import io
import hmac
import functools

from Crypto.Cipher import DES3
from nanohttp import settings
from OpenSSL import crypto

from .iso9797 import iso9797_mac


def random(size):  # pragma: no cover
    # This function is trying to be a secure random and it will be improved
    # later.
    return os.urandom(size)


def create_signature(key_filename, message, hash_algorithm='sha1'):
    with open(key_filename) as key:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key.read())

    signature = crypto.sign(private_key, message, hash_algorithm)

    return signature


frombytes = functools.partial(int.from_bytes, byteorder='big', signed=False)


class PlainISO0PinBlock:
    """
    http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/

    """
    def __init__(self, pan, bankid, length=4):
        if settings.pinblock.algorithm == 'isc':
            tokenbytes = pan
            partone = frombytes(tokenbytes[:8])
            parttwo = frombytes(tokenbytes[8:])
            self.pan = partone ^ parttwo

        elif settings.pinblock.algorithm == 'pouya':
            self.pan = int(f'0000{pan.decode()[3:15]}', 16)

    def encode(self, data):
        return b'%0.16x' % (
            self.pan ^ int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16)
        )

    def decode(self, encoded):
        block = b'%0.16x' % (self.pan ^ int(encoded, 16))
        return block[2:2+int(block[:2])]


class EncryptedISOPinBlock(PlainISO0PinBlock):

    def __init__(self, pan, bankid, key=None):
        self.key = binascii.unhexlify(key or settings.pinblock[bankid].key)
        super().__init__(pan, bankid)

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

