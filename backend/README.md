# Backend

## Overview
This FastAPI service exposes the GHL authorization proof-of-concept endpoints.

## Setup
1. Create and activate a virtual environment:
   - Windows: `venv\\Scripts\\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your GHL Private Integration Token.

## Run
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints
- `GET /health`
- `GET /api/ghl/context?location_id=LOCATION_ID`
- `POST /api/auth/validate`
- `GET /api/config`
