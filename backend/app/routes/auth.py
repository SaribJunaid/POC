import datetime
from fastapi import APIRouter, Request, Response, HTTPException, status
from fastapi.responses import RedirectResponse
import urllib.parse

from app.services.oauth_service import OAuthService
from app.services.jwt_service import JWTService
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth_service = OAuthService()
jwt_service = JWTService()

@router.get("/callback")
def oauth_callback(request: Request) -> Response:
    """OAuth2 Authorization Code callback.

    Handles the ``code`` parameter from GoHighLevel, exchanges it for tokens,
    creates our own JWT and redirects back to the SPA with the JWT in the
    query string.
    """
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing code parameter")
    # Build the redirect URI that GHL used (our own endpoint)
    redirect_uri = str(request.url_for('oauth_callback'))
    # Exchange the authorization code for GHL tokens
    token_response = oauth_service.exchange_code(code=code, redirect_uri=redirect_uri)
    # Extract fields we need – keys follow GHL docs (adjust if needed)
    access_token = token_response.get("access_token")
    refresh_token = token_response.get("refresh_token")
    location_id = token_response.get("location_id")
    company_id = token_response.get("company_id")
    user_id = token_response.get("user_id")

    # Build a payload compatible with existing SSOService expectations
    user_data = {
        "userId": user_id,
        "companyId": company_id,
        "role": token_response.get("role", "user"),
        "type": token_response.get("type", ""),
        "email": token_response.get("email", ""),
        "userName": token_response.get("user_name", ""),
        "isAgencyOwner": token_response.get("is_agency_owner", False),
        "activeLocation": location_id,
        "versionId": token_response.get("version_id", ""),
        "appStatus": token_response.get("app_status", ""),
        "whitelabelDetails": {
            "domain": token_response.get("whitelabel_domain", ""),
            "logoUrl": token_response.get("logo_url", ""),
        },
    }
    # Create our own JWT for the SPA
    our_jwt = jwt_service.create_token(user_data)

    # Persist installation (never expose secret tokens to the frontend)
    installation_record = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "location_id": location_id,
        "company_id": company_id,
        "user_id": user_id,
        "installation_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    oauth_service.save_installation(installation_record)

    # Redirect back to the SPA login page with the JWT in the query string
    redirect_url = f"{settings.FRONTEND_URL}/login?token={urllib.parse.quote_plus(our_jwt)}"
    return RedirectResponse(url=redirect_url)

@router.get("/me")
def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt_service.decode_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    return {"user": payload}

@router.post("/logout")
def logout():
    # No server‑side session state – client simply discards JWT
    return {"status": "logged_out"}

@router.post("/refresh")
def refresh_token():
    latest = oauth_service.get_latest_installation()
    if not latest:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No installation found")
    refresh_tok = latest.get("refresh_token")
    if not refresh_tok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No refresh token stored")
    token_response = oauth_service.refresh_access_token(refresh_tok)
    # Re‑use the same shape as before for JWT payload
    user_data = {
        "userId": token_response.get("user_id"),
        "companyId": token_response.get("company_id"),
        "role": token_response.get("role", "user"),
        "type": token_response.get("type", ""),
        "email": token_response.get("email", ""),
        "userName": token_response.get("user_name", ""),
        "isAgencyOwner": token_response.get("is_agency_owner", False),
        "activeLocation": token_response.get("location_id"),
        "versionId": token_response.get("version_id", ""),
        "appStatus": token_response.get("app_status", ""),
        "whitelabelDetails": {
            "domain": token_response.get("whitelabel_domain", ""),
            "logoUrl": token_response.get("logo_url", ""),
        },
    }
    new_jwt = jwt_service.create_token(user_data)
    # Update stored installation with fresh tokens and timestamp
    latest["access_token"] = token_response.get("access_token")
    latest["refresh_token"] = token_response.get("refresh_token")
    latest["installation_timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    # Overwrite the entire installations file with the updated list
    oauth_service._save_installations(oauth_service._load_installations())
    return {"token": new_jwt}
