# Backend

## Overview
This FastAPI service handles GoHighLevel Custom Page SSO. The frontend sends the encrypted GHL SSO payload to the backend, the backend decrypts it with `GHL_SHARED_SECRET`, and returns a short-lived JWT.

## Setup
1. Create and activate a virtual environment:
   - Windows: `venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure `.env`:

```env
GHL_SHARED_SECRET=
JWT_SECRET=
JWT_EXPIRE_MINUTES=60
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,https://localhost:5173
```

Production frontend:
```env
FRONTEND_URL=https://poc-jade-sigma.vercel.app/
ALLOWED_ORIGINS=https://poc-jade-sigma.vercel.app,https://poc-jade-sigma.vercel.app/
```

## Run
```bash
uvicorn app.main:app --reload --port 8000
```

## Endpoints
- `GET /health`
- `POST /sso/decrypt`
- `GET /sso/session`
- `POST /logout`
