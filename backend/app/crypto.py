import base64
import json
from hashlib import md5
from typing import Any, Dict

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int = 32, iv_len: int = 16) -> tuple[bytes, bytes]:
    """Derive an AES key and IV using the OpenSSL/EVP legacy flow used by CryptoJS."""
    derived = b""
    key_iv = b""
    while len(key_iv) < key_len + iv_len:
        derived = md5(derived + password + salt).digest()
        key_iv += derived
    return key_iv[:key_len], key_iv[key_len : key_len + iv_len]


def decrypt_sso_payload(encrypted_data: str, shared_secret: str) -> Dict[str, Any]:
    """Decrypt an AES-256-CBC payload that follows the GHL OpenSSL/Salted__ format."""
    raw = base64.b64decode(encrypted_data)
    if raw[:8] != b"Salted__":
        raise ValueError("Invalid payload: missing 'Salted__' header")

    salt = raw[8:16]
    ciphertext = raw[16:]

    key, iv = evp_bytes_to_key(shared_secret.encode("utf-8"), salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return json.loads(plaintext.decode("utf-8"))
