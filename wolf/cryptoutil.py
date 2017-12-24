import os
import hashlib

from Crypto.Cipher import AES


hashlib_map = {
    'SHA-1': hashlib.sha1,
    'SHA-256': hashlib.sha256,
    'SHA-384': hashlib.sha384,
    'SHA-512': hashlib.sha512
}


hash_algorithm_sizes = {
    'SHA-1': 20,
    'SHA-256': 32,
    'SHA-384': 48,
    'SHA-512': 64,
}


def hash_algorithm_to_hashlib(hash_algorithm):
    return hashlib_map[hash_algorithm]


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
