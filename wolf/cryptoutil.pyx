import os
import binascii
import base64
import hashlib
import io

from Crypto.Cipher import DES3
from nanohttp import settings


def random(size):
    # This function is trying to be a secure random and it will be improved later.
    return os.urandom(size)



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
        if len(encoded) % 2 != 0:
            raise ValueError('Odd-length string')
        pinblock = algorithm.decrypt(binascii.unhexlify(encoded))
        return super().decode(binascii.hexlify(pinblock).upper())


# FIXME: Migrate to oath.cy
def totp_checksum(data: bytes, length=4):
    """
    https://tools.ietf.org/html/rfc6238  [page 13]

    byte[] hash = hmac_sha(crypto, k, msg);
    // put selected bytes into result int
    int offset = hash[hash.length - 1] & 0xf;
    int binary =
        ((hash[offset] & 0x7f) << 24) |
        ((hash[offset + 1] & 0xff) << 16) |
        ((hash[offset + 2] & 0xff) << 8) |
        (hash[offset + 3] & 0xff);
    int otp = binary % DIGITS_POWER[codeDigits];
    result = Integer.toString(otp);
    while (result.length() < codeDigits) {
        result = "0" + result;
    }
    return result;
    """
    digest = hashlib.sha1(data).digest()
    offset = digest[-1] & 0xf

    return str(
        ((digest[offset] & 0x7f) << 24) |
        ((digest[offset + 1] & 0xff) << 16) |
        ((digest[offset + 2] & 0xff) << 8) |
        (digest[offset + 3] & 0xff)
    ).zfill(length)[-length:]


