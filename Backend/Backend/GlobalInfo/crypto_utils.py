# Backend/crypto_utils.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

def get_key():
    return os.environ.get('ENCRYPTION_KEY').encode()  # Usar una clave segura de entorno

def encrypt_data(data):
    cipher = AES.new(get_key(), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ':' + ct

def decrypt_data(encrypted_data):
    iv, ct = encrypted_data.split(':')
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(get_key(), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')