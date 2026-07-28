from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ValidateRequest(BaseModel):
    location_id: str = Field(..., min_length=1)
    user_id: Optional[str] = None
    email: Optional[str] = None

    model_config = {"extra": "forbid"}

    def get_identity(self) -> tuple[Optional[str], Optional[str]]:
        return self.user_id, self.email


class ContextResponse(BaseModel):
    locationId: Optional[str] = None
    locationName: Optional[str] = None
    companyId: Optional[str] = None


class AuthUserResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    isAgencyOwner: bool = False


class AuthResponse(BaseModel):
    authorized: bool
    reason: str
    location: Dict[str, Optional[str]]
    user: Optional[AuthUserResponse] = None


class ConfigResponse(BaseModel):
    frontendUrl: str
    apiBaseUrl: str
    trustedOrigins: List[str]
