import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import sso, auth

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ghl_sso_app")

app = FastAPI(title="GHL Custom Pages SSO", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sso.router)
app.include_router(auth.router)
