import binascii
import functools
import os

from Crypto.Cipher import DES3
from OpenSSL import crypto


def random(size):  # pragma: no cover
    # This function is trying to be a secure random and it will be improved
    # later.
    return os.urandom(size)


def create_signature(key_filename, message, hash_algorithm='sha1'):
    with open(key_filename) as key:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key.read())

    signature = crypto.sign(private_key, message, hash_algorithm)

    return signature


byteorder = 'big'
frombytes = functools.partial(int.from_bytes, byteorder=byteorder)


class PlainISO0PinBlock:
    """
    http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/

    """
    def __init__(self, pan):
        self.pan = frombytes(pan)

    def encode(self, data) -> bytes:
        pin = int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16)
        return (self.pan ^ pin).to_bytes(8, byteorder)

    def decode(self, encoded):
        block = b'%0.16x' % (self.pan ^ int(encoded, 16))
        return block[2:2+int(block[:2])]


class ISCPinBlock(PlainISO0PinBlock):

    def __init__(self, tokenid: bytes, length=4):
        partone = frombytes(tokenid[:8])
        parttwo = frombytes(tokenid[8:])
        self.pan = (frombytes(tokenid[:8]) ^ frombytes(tokenid[8:]))
        self.pan = hex(self.pan)[5:17]
        self.pan = frombytes(binascii.unhexlify(self.pan))

    def encode(self, data):
        pinblock = super().encode(data)
        return binascii.hexlify(pinblock).upper()


class PouyaPinBlock(PlainISO0PinBlock):

    def __init__(self, pan, key):
        self.pan = int(f'0000{pan.decode()[3:15]}', 16)
        self.key = key

    def create_algorithm(self):
        return DES3.new(self.key, DES3.MODE_ECB)

    def encode(self, data):
        pinblock = super().encode(data)
        des_algorithm = self.create_algorithm()
        encrypted = des_algorithm.encrypt(pinblock)
        return binascii.hexlify(encrypted).upper()

    def decode(self, encoded):
        algorithm = self.create_algorithm()
        if len(encoded) % 2 != 0:
            raise ValueError('Odd-length string')
        pinblock = algorithm.decrypt(binascii.unhexlify(encoded))
        return super().decode(binascii.hexlify(pinblock).upper())

