from typing import Any, Dict, Optional

from .ghl_client import GHLAPIError, GHLClient


class AuthorizationService:
    def __init__(self, client: Optional[GHLClient] = None):
        self.client = client or GHLClient()

    def authorize(self, location_id: str, user_id: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
        if not location_id:
            raise ValueError("location_id is required")
        if not user_id and not email:
            raise ValueError("Either user_id or email must be provided")

        location = self.client.get_location(location_id)
        company_id = location.get("companyId")
        if not company_id:
            raise GHLAPIError("Location company ID is missing.", status_code=404)

        users = self.client.search_users(company_id)
        current_user = None

        if user_id:
            current_user = self.client.get_user_by_id(company_id, user_id)
        if not current_user and email:
            current_user = self.client.search_user_by_email(company_id, email)

        if not current_user:
            return {
                "authorized": False,
                "reason": "User could not be found in the GHL account",
                "location": {
                    "id": location.get("id"),
                    "name": location.get("name"),
                    "companyId": company_id,
                },
                "user": None,
            }

        roles = current_user.get("roles") or {}
        location_ids = roles.get("locationIds") or []
        if isinstance(location_ids, str):
            location_ids = [location_ids]
        if location_id not in location_ids:
            return {
                "authorized": False,
                "reason": "User does not belong to the requested location",
                "location": {
                    "id": location.get("id"),
                    "name": location.get("name"),
                    "companyId": company_id,
                },
                "user": {
                    "id": current_user.get("id"),
                    "name": current_user.get("name"),
                    "email": current_user.get("email"),
                    "role": roles.get("role"),
                    "isAgencyOwner": bool(current_user.get("isAgencyOwner")),
                },
            }

        role = roles.get("role") or "user"
        is_agency_owner = bool(current_user.get("isAgencyOwner"))
        authorized = is_agency_owner or role == "admin"

        return {
            "authorized": authorized,
            "reason": "User is authorized" if authorized else "User is not authorized for this application",
            "location": {
                "id": location.get("id"),
                "name": location.get("name"),
                "companyId": company_id,
            },
            "user": {
                "id": current_user.get("id"),
                "name": current_user.get("name"),
                "email": current_user.get("email"),
                "role": role,
                "isAgencyOwner": is_agency_owner,
            },
        }
