import logging
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .auth import AuthorizationService
from .config import settings
from .context import ContextService
from .ghl_client import GHLAPIError
from .schemas import AuthResponse, ConfigResponse, ContextResponse, ValidateRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ghl_auth_poc")

app = FastAPI(title="GHL Auth POC", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

context_service = ContextService()
authorization_service = AuthorizationService()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/api/ghl/context", response_model=ContextResponse)
def get_context(location_id: str) -> ContextResponse:
    try:
        context = context_service.get_context(location_id)
        return ContextResponse(**context)
    except HTTPException:
        raise
    except GHLAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except Exception as exc:
        logger.exception("Location lookup failed")
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.post("/api/auth/validate", response_model=AuthResponse)
def validate_authorization(payload: ValidateRequest) -> AuthResponse:
    try:
        user_id, email = payload.get_identity()
        if not user_id and not email:
            raise HTTPException(status_code=422, detail="Either user_id or email must be provided")
        result = authorization_service.authorize(payload.location_id, user_id=user_id, email=email)
        return AuthResponse(**result)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GHLAPIError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except Exception as exc:
        logger.exception("Authorization failed")
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.get("/api/config", response_model=ConfigResponse)
def get_config() -> ConfigResponse:
    return ConfigResponse(
        frontendUrl=settings.FRONTEND_URL,
        apiBaseUrl=settings.GHL_API_BASE_URL,
        trustedOrigins=settings.allowed_origins(),
    )
