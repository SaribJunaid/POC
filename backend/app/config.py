import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    GHL_API_TOKEN: str | None = os.getenv("GHL_API_TOKEN")
    GHL_API_BASE_URL: str = os.getenv("GHL_API_BASE_URL", "https://services.leadconnectorhq.com")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    @classmethod
    def allowed_origins(cls) -> List[str]:
        origins = [cls.FRONTEND_URL, "http://localhost:5173", "https://localhost:5173"]
        extra_origins = os.getenv("ALLOWED_ORIGINS", "")
        if extra_origins:
            origins.extend([item.strip() for item in extra_origins.split(",") if item.strip()])
        return list(dict.fromkeys(origins))


settings = Settings()
