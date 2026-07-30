from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt

from app.config import settings


class JWTService:
    def __init__(self, secret: str | None = None, algorithm: str | None = None, expire_minutes: int | None = None) -> None:
        self.secret = secret or settings.JWT_SECRET
        self.algorithm = algorithm or settings.JWT_ALGORITHM
        self.expire_minutes = expire_minutes or settings.JWT_EXPIRE_MINUTES

    def create_token(self, user_data: Dict[str, Any]) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        whitelabel_details = user_data.get("whitelabelDetails") or {}
        payload = {
            "sub": user_data.get("userId"),
            "company_id": user_data.get("companyId"),
            "role": user_data.get("role"),
            "type": user_data.get("type"),
            "email": user_data.get("email"),
            "user_name": user_data.get("userName"),
            "is_agency_owner": user_data.get("isAgencyOwner"),
            "active_location": user_data.get("activeLocation"),
            "version_id": user_data.get("versionId"),
            "app_status": user_data.get("appStatus"),
            "whitelabel_domain": whitelabel_details.get("domain"),
            "logo_url": whitelabel_details.get("logoUrl"),
            "exp": expires_at,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except JWTError as exc:
            raise ValueError("Invalid or expired token") from exc
