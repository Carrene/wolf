import os

from Crypto.Cipher import AES


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
