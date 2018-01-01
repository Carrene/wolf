#! /usr/bin/env python3.6


# http://www.paymentsystemsblog.com/2010/03/03/pin-block-formats/
class ISO0PinBlock:
    def __init__(self, psk):
        self.pan = int('0000' + psk[-13:-1], 16)

    def encode(self, data):
        pin = int(f'{len(data):02}{data}{"F" * (14-len(data))}', 16)
        return '%0.16x' % (pin ^ self.pan)

    def decode(self, encoded):
        block = '%0.16x' % (self.pan ^ int(encoded, 16))
        return block[2:2+int(block[:2])]


if __name__ == '__main__':
    alg = ISO0PinBlock('1700191111116685')
    code = '123456'
    enc = alg.encode(code)
    print('CLR:', code)
    print('ENC:', enc)
    print('DEC:', alg.decode(enc))
