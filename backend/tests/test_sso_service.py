import base64
import json
from hashlib import md5

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from app.crypto import decrypt_sso_payload
from app.services.jwt_service import JWTService
from app.services.sso_service import SSOService


def test_decrypt_sso_payload_with_salted_payload():
    secret = "shared-secret"
    payload = {
        "userId": "user-123",
        "companyId": "company-456",
        "role": "admin",
        "type": "agency",
        "email": "owner@example.com",
        "userName": "Owner",
        "isAgencyOwner": True,
        "versionId": "v1",
        "appStatus": "live",
        "whitelabelDetails": {"domain": "example.com", "logoUrl": "https://example.com/logo.png"},
    }

    salt = b"salt1234"
    key_iv = b""
    derived = b""
    while len(key_iv) < 32 + 16:
        derived = md5(derived + secret.encode("utf-8") + salt).digest()
        key_iv += derived

    key = key_iv[:32]
    iv = key_iv[32:48]
    ciphertext = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(json.dumps(payload).encode("utf-8"), AES.block_size))
    encrypted = base64.b64encode(b"Salted__" + salt + ciphertext).decode("utf-8")

    result = decrypt_sso_payload(encrypted, secret)

    assert result["userId"] == payload["userId"]
    assert result["companyId"] == payload["companyId"]
    assert result["role"] == payload["role"]
    assert result["type"] == payload["type"]


def test_session_payload_preserves_dashboard_fields():
    user_data = {
        "userId": "user-123",
        "companyId": "company-456",
        "role": "admin",
        "type": "agency",
        "email": "owner@example.com",
        "userName": "Owner",
        "isAgencyOwner": True,
        "activeLocation": "location-789",
        "versionId": "v1",
        "appStatus": "live",
        "whitelabelDetails": {"domain": "example.com", "logoUrl": "https://example.com/logo.png"},
    }

    jwt_service = JWTService(secret="test-secret", expire_minutes=60)
    token_payload = jwt_service.decode_token(jwt_service.create_token(user_data))
    session = SSOService(jwt_service=jwt_service).build_session_payload(token_payload)

    assert session["userId"] == user_data["userId"]
    assert session["companyId"] == user_data["companyId"]
    assert session["activeLocation"] == user_data["activeLocation"]
    assert session["versionId"] == user_data["versionId"]
    assert session["appStatus"] == user_data["appStatus"]
    assert session["whitelabelDomain"] == user_data["whitelabelDetails"]["domain"]
    assert session["logoUrl"] == user_data["whitelabelDetails"]["logoUrl"]
