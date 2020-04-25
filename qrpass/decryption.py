import base64
import binascii
import json
from hashlib import md5

from Crypto import Random
from Crypto.Cipher import AES
from django.conf import settings

BLOCK_SIZE = 16


def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length) * length).encode()


def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


def bytes_to_key(data, salt, output=48):
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]


def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32 + 16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))


def qr_pass_decrypt(qr_hash):
    secret_key = settings.PASS_SECRET_KEY.encode()
    try:
        qr_hash = base64.b64decode(qr_hash)
        return decrypt(qr_hash, secret_key).decode("UTF-8")
    except binascii.Error:
        return False


def qr_pass_validate(qr_hash):
    try:
        user_id = json.loads(qr_pass_decrypt(qr_hash))
        return user_id.__contains__('user-id')
    except TypeError:
        return False
