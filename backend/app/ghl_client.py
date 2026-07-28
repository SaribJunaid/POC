import logging
from typing import Any, Dict, List, Optional

import requests

from .config import settings

logger = logging.getLogger("ghl_client")


class GHLAPIError(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class GHLClient:
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: int = 10):
        self.base_url = (base_url or settings.GHL_API_BASE_URL).rstrip("/")
        self.token = token or settings.GHL_API_TOKEN
        self.timeout = timeout
        self.session = requests.Session()

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Version": "v3",
        }
        return headers

    def _request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if not self.token:
            raise GHLAPIError("GHL API token is not configured.", status_code=401)

        url = f"{self.base_url}{path}"
        try:
            logger.info("Calling GHL endpoint %s", url)
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=self._headers(),
                timeout=self.timeout,
            )
            logger.info("GHL response status: %s", response.status_code)
        except requests.RequestException as exc:
            logger.exception("GHL request failed")
            raise GHLAPIError("GHL API is unavailable at the moment.", status_code=502) from exc

        if response.status_code == 401:
            raise GHLAPIError("GHL authentication failed.", status_code=401)
        if response.status_code == 403:
            raise GHLAPIError("GHL permission denied.", status_code=403)
        if response.status_code == 404:
            raise GHLAPIError("GHL resource was not found.", status_code=404)
        if response.status_code == 422:
            raise GHLAPIError("Invalid GHL request.", status_code=422)
        if response.status_code == 429:
            raise GHLAPIError("GHL rate limit exceeded.", status_code=429)
        if response.status_code >= 500:
            raise GHLAPIError("GHL API service error.", status_code=502)
        if response.status_code >= 400:
            raise GHLAPIError("GHL request failed.", status_code=response.status_code)

        try:
            payload = response.json()
        except ValueError as exc:
            raise GHLAPIError("Invalid JSON response from GHL.", status_code=502) from exc

        return payload

    def get_location(self, location_id: str) -> Dict[str, Any]:
        payload = self._request("GET", f"/locations/{location_id}")
        location = payload.get("location") or payload
        if not location:
            raise GHLAPIError("Location not found.", status_code=404)
        return {
            "id": location.get("id"),
            "name": location.get("name"),
            "companyId": location.get("companyId"),
            "brandId": location.get("brandId"),
        }

    def search_users(self, company_id: str) -> List[Dict[str, Any]]:
        payload = self._request("GET", "/users/search", params={"companyId": company_id})
        users = payload.get("users") or []
        if not isinstance(users, list):
            raise GHLAPIError("Invalid user list returned by GHL.", status_code=502)
        return users

    def search_user_by_email(self, company_id: str, email: str) -> Optional[Dict[str, Any]]:
        users = self.search_users(company_id)
        for user in users:
            if str(user.get("email") or "").strip().lower() == email.strip().lower():
                return user
        return None

    def get_user_by_id(self, company_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        users = self.search_users(company_id)
        for user in users:
            if str(user.get("id") or "").strip() == user_id.strip():
                return user
        return None
