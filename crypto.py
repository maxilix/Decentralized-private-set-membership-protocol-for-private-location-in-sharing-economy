import random

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256

aes_nonce = b'0123456789abcdef'

def aes_encrypt(message, key):
    global aes_nonce
    cipher = AES.new(key, AES.MODE_EAX, nonce=aes_nonce)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return ciphertext, tag

def aes_decrypt(data, key):
    global aes_nonce
    ciphertext, tag = data
    cipher = AES.new(key, AES.MODE_EAX, nonce=aes_nonce)
    plaintext = cipher.decrypt(ciphertext).decode()
    cipher.verify(tag)
    return plaintext

def _to_bytes(data: bytes | int | str) -> bytes:
    if isinstance(data, bytes):
        return data
    elif isinstance(data, int):
        return data.to_bytes(256, "big")
    elif isinstance(data, str):
        return data.encode("utf-8")
    else:
        raise TypeError("Unsupported data type")

def hashmac_to_str(message, key) -> str:
    key = _to_bytes(key)
    message = _to_bytes(message)
    hmac = HMAC.new(key, msg=message, digestmod=SHA256)
    return hmac.hexdigest()

def hash_to_str(message) -> str:
    message = _to_bytes(message)
    h = SHA256.new(message)
    return h.hexdigest()

def hash_to_bytes(message) -> bytes:
    message = _to_bytes(message)
    h = SHA256.new(message)
    return h.digest()

def hash_to_int(message) -> int:
    message = _to_bytes(message)
    h = SHA256.new(message)
    rop = int.from_bytes(h.digest(), "big")
    assert rop != 0
    return rop

def rand_int():
    return random.randrange(1, 2 ** 256)
