import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


def env_value(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return value if value not in (None, "") else default


class Settings:
    GHL_API_TOKEN: str = env_value("GHL_API_TOKEN")
    GHL_SHARED_SECRET: str = env_value("GHL_SHARED_SECRET")
    GHL_API_BASE_URL: str = env_value("GHL_API_BASE_URL", "https://services.leadconnectorhq.com")
    JWT_SECRET: str = env_value("JWT_SECRET", "change-me-in-production")
    JWT_ALGORITHM: str = env_value("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(env_value("JWT_EXPIRE_MINUTES", "60"))
    FRONTEND_URL: str = env_value("FRONTEND_URL", "http://localhost:5173")

    @classmethod
    def allowed_origins(cls) -> List[str]:
        origins = [cls.FRONTEND_URL, "http://localhost:5173", "https://localhost:5173"]
        extra_origins = os.getenv("ALLOWED_ORIGINS", "")
        if extra_origins:
            origins.extend([item.strip() for item in extra_origins.split(",") if item.strip()])
        return list(dict.fromkeys(origins))


settings = Settings()
