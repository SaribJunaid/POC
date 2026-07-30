import logging
from typing import Annotated, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models import DecryptRequest, DecryptResponse, SessionUser
from app.services.jwt_service import JWTService
from app.services.sso_service import SSOService

logger = logging.getLogger("ghl_sso")
router = APIRouter(prefix="", tags=["sso"])
security = HTTPBearer(auto_error=False)

jwt_service = JWTService()
sso_service = SSOService(jwt_service=jwt_service)


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/sso/decrypt", response_model=DecryptResponse)
def decrypt_sso(payload: DecryptRequest) -> DecryptResponse:
    try:
        response = sso_service.authenticate(payload.key)
        return DecryptResponse(**response)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("SSO decryption failed")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="SSO validation failed") from exc


@router.get("/sso/session", response_model=SessionUser)
def get_session(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(security)] = None) -> SessionUser:
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    try:
        token_payload = jwt_service.decode_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    return SessionUser(**sso_service.build_session_payload(token_payload))


@router.post("/logout")
def logout() -> Dict[str, str]:
    return {"status": "ok"}
