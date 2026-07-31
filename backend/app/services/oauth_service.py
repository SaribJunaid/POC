import requests
import datetime
from typing import Dict, Any
from urllib.parse import urlencode

from ..config import settings


class OAuthService:
    """Service handling GoHighLevel OAuth token exchange and refresh.

    It stores installation information in a JSON file (data/installations.json).
    """

    TOKEN_ENDPOINT = f"{settings.GHL_API_BASE_URL}/oauth/token"
    INSTALLATION_FILE = "c:/Users/PMLS/Desktop/POC/backend/data/installations.json"

    def __init__(self):
        # Ensure the data directory exists
        import os
        os.makedirs(os.path.dirname(self.INSTALLATION_FILE), exist_ok=True)
        # Initialize file if missing
        if not os.path.isfile(self.INSTALLATION_FILE):
            with open(self.INSTALLATION_FILE, "w", encoding="utf-8") as f:
                f.write("[]")

    # ---------------------------------------------------------------------
    # Token exchange (authorization_code)
    # ---------------------------------------------------------------------
    def exchange_code(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange an authorization code for access/refresh tokens.

        Returns the full token response JSON.
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": settings.GHL_API_TOKEN,  # Using provided token as client_id
            "client_secret": settings.GHL_SHARED_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.TOKEN_ENDPOINT, data=urlencode(payload), headers=headers)
        response.raise_for_status()
        token_data = response.json()
        return token_data

    # ---------------------------------------------------------------------
    # Refresh token
    # ---------------------------------------------------------------------
    def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": settings.GHL_API_TOKEN,
            "client_secret": settings.GHL_SHARED_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.TOKEN_ENDPOINT, data=urlencode(payload), headers=headers)
        response.raise_for_status()
        return response.json()

    # ---------------------------------------------------------------------
    # Installation persistence (JSON file)
    # ---------------------------------------------------------------------
    def _load_installations(self) -> list:
        import json
        with open(self.INSTALLATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_installations(self, data: list) -> None:
        import json
        with open(self.INSTALLATION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def save_installation(self, installation: dict) -> None:
        """Append a new installation record.

        The record should contain at least:
        - access_token
        - refresh_token
        - location_id
        - company_id
        - user_id
        - installation_timestamp
        """
        installs = self._load_installations()
        installs.append(installation)
        self._save_installations(installs)

    def get_latest_installation(self) -> dict | None:
        installs = self._load_installations()
        return installs[-1] if installs else None
