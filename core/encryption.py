from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import os

#  Constants
SALT_SIZE = 16
KEY_SIZE = 32  #  AES-256
ITERATIONS = 100_000

  #  Key derivation
def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)

# Encrypt message
def encrypt_message(message: str, password: str) -> str:
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    encrypted_data = salt + cipher.nonce + tag + ciphertext
    return base64.b64encode(encrypted_data).decode()

# Decrypt message
def decrypt_message(encrypted_data_b64: str, password: str) -> str:
    encrypted_data = base64.b64decode(encrypted_data_b64)
    salt = encrypted_data[:SALT_SIZE]
    nonce = encrypted_data[SALT_SIZE:SALT_SIZE+16]
    tag = encrypted_data[SALT_SIZE+16:SALT_SIZE+32]
    ciphertext = encrypted_data[SALT_SIZE+32:]

    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted.decode()
    except (ValueError, KeyError):
        return "[Decryption failed]"
