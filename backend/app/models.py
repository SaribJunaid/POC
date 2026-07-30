from typing import Optional

from pydantic import BaseModel, Field


class DecryptRequest(BaseModel):
    key: str = Field(..., description="Encrypted SSO payload returned by GHL")


class DecryptResponse(BaseModel):
    token_type: str = Field(default="Bearer")
    access_token: str
    expires_in: int


class SessionUser(BaseModel):
    userId: Optional[str] = None
    companyId: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None
    email: Optional[str] = None
    userName: Optional[str] = None
    isAgencyOwner: Optional[bool] = None
    activeLocation: Optional[str] = None
    versionId: Optional[str] = None
    appStatus: Optional[str] = None
    whitelabelDomain: Optional[str] = None
    logoUrl: Optional[str] = None

