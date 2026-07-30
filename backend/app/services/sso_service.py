import logging
from typing import Any, Dict

from app.config import settings
from app.crypto import decrypt_sso_payload
from app.services.jwt_service import JWTService

logger = logging.getLogger("ghl_sso")


class SSOService:
    def __init__(self, jwt_service: JWTService | None = None) -> None:
        self.jwt_service = jwt_service or JWTService()
        self.shared_secret = settings.GHL_SHARED_SECRET

    def authenticate(self, encrypted_payload: str) -> Dict[str, Any]:
        if not encrypted_payload:
            raise ValueError("Encrypted payload is required")
        if not self.shared_secret:
            raise ValueError("GHL_SHARED_SECRET is not configured")

        user_data = decrypt_sso_payload(encrypted_payload, self.shared_secret)
        self._validate_user_data(user_data)
        token = self.jwt_service.create_token(user_data)
        logger.info("Created SSO session for user %s", user_data.get("userId"))
        return {
            "token_type": "Bearer",
            "access_token": token,
            "expires_in": self.jwt_service.expire_minutes * 60,
        }

    def build_session_payload(self, token_payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "userId": token_payload.get("sub"),
            "companyId": token_payload.get("company_id"),
            "role": token_payload.get("role"),
            "type": token_payload.get("type"),
            "email": token_payload.get("email"),
            "userName": token_payload.get("user_name"),
            "isAgencyOwner": token_payload.get("is_agency_owner"),
            "activeLocation": token_payload.get("active_location"),
            "versionId": token_payload.get("version_id"),
            "appStatus": token_payload.get("app_status"),
            "whitelabelDomain": token_payload.get("whitelabel_domain"),
            "logoUrl": token_payload.get("logo_url"),
        }

    def _validate_user_data(self, user_data: Dict[str, Any]) -> None:
        required_fields = ("userId", "companyId", "role", "type", "email", "userName", "isAgencyOwner")
        missing = [field for field in required_fields if user_data.get(field) in (None, "")]
        if missing:
            raise ValueError(f"Decrypted SSO payload is missing required fields: {', '.join(missing)}")
