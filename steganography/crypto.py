from base64 import encode
import sys
from cryptography.fernet import Fernet
import base64
import hashlib


def encrypt_data(data: bytes, key: str) -> bytes:
    key = base64.urlsafe_b64encode(hashlib.md5(key.encode()).hexdigest().encode())

    f = Fernet(key)
    encoded_data = f.encrypt(data)
    return encoded_data


def decrypt_data(data: bytes, key: str) -> bytes:
    try:
        key = base64.urlsafe_b64encode(hashlib.md5(key.encode()).hexdigest().encode())

        f = Fernet(key)
        decrypted_data = f.decrypt(data)
        return decrypted_data

    except:
        print('Invalid data or password')
        sys.exit()
