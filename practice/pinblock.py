#! /usr/bin/env python3.6

import binascii

from Crypto.Cipher import DES3


# http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/
class ISO0PinBlock:
    def __init__(self, psk):
        self.pan = int('0000' + psk[-13:-1], 16)

    def encode(self, data):
        pin = int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16)
        return ('%0.16x' % (pin ^ self.pan)).upper()

    def decode(self, encoded):
        block = '%0.16x' % (self.pan ^ int(encoded, 16))
        return block[2:2 + int(block[:2])]


def encrypt(key, pan, code):
    alg = ISO0PinBlock(pan)
    pinblock = alg.encode(code)

    key = binascii.unhexlify(key)
    des = DES3.new(key, DES3.MODE_ECB)
    enc = des.encrypt(binascii.unhexlify(pinblock))
    enc = binascii.hexlify(enc).decode().upper()
    return pinblock, enc


def decrypt(key, pan, encrypted):
    key = binascii.unhexlify(key)
    des = DES3.new(key, DES3.MODE_ECB)
    dec = des.decrypt(binascii.unhexlify(encrypted))
    pinblock = binascii.hexlify(dec).decode().upper()

    alg = ISO0PinBlock(pan)
    dec = alg.decode(pinblock)
    return pinblock, dec


def try_(key, pan, code):
    pinblock, enc = encrypt(key, pan, code)
    pinblock, dec = decrypt(key, pan, enc)
    print('CLR:', code)
    print('BLK:', pinblock)
    print('ENC:', enc)
    print('BLK:', pinblock)
    print('DEC:', dec)


if __name__ == '__main__':
    key = '1234567890ABCDEF1234567890ABCDEF'
    try_(
        key=key,
        pan='6037991000024723',
        code='1234'
    )

    try_(
        key=key,
        pan='0000000000024723',
        code='123456'
    )
