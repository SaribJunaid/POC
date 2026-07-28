from typing import Any, Dict, Optional

from .auth import AuthorizationService
from .config import settings
from .ghl_client import GHLAPIError, GHLClient


class ContextService:
    def __init__(self, client: Optional[GHLClient] = None):
        self.client = client or GHLClient()
        self.auth_service = AuthorizationService(self.client)

    def get_context(self, location_id: str) -> Dict[str, Any]:
        location = self.client.get_location(location_id)
        return {
            "locationId": location.get("id"),
            "locationName": location.get("name"),
            "companyId": location.get("companyId"),
        }
