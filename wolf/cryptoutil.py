import os

from Crypto.Cipher import AES
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


class ISO0PinBlock:
    """
    http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/

    """
    def __init__(self, psk=None):
        psk = psk or settings.pinblock.psk
        self.pan = int('0000' + psk[-13:-1], 16)

    def encode(self, data):
        pin = int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16)
        return '%0.16x' % (pin ^ self.pan)

    def decode(self, encoded):
        block = '%0.16x' % (self.pan ^ int(encoded, 16))
        return block[2:2+int(block[:2])]
