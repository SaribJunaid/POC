# GoHighLevel Custom Page SSO App

This repository contains a React + FastAPI implementation of the official GoHighLevel Marketplace Custom Page SSO flow. Authentication is based only on the encrypted SSO payload returned by GHL through `postMessage`; the frontend never decrypts that payload and never authenticates from URL parameters.

## Architecture
- Frontend: React + Vite + JavaScript
- Backend: FastAPI + Python
- Auth flow: frontend requests `REQUEST_USER_DATA`, posts the encrypted payload to FastAPI, receives a JWT, stores it in `sessionStorage`, and fetches the current session.

## Project Structure
```text
backend/
  app/
    main.py
    config.py
    crypto.py
    models.py
    routes/sso.py
    services/jwt_service.py
    services/sso_service.py
frontend/
  src/
    pages/SSOPage.jsx
    pages/Dashboard.jsx
    services/ssoService.js
    hooks/useSession.js
    components/Loading.jsx
    components/ProtectedRoute.jsx
```

## Prerequisites
- Python 3.10+
- Node.js 18+
- A GHL Marketplace app Custom Page with a generated Shared Secret

## Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Update `.env` with your real values:
```env
GHL_SHARED_SECRET=your_ghl_shared_secret
JWT_SECRET=generate_a_strong_random_value
JWT_EXPIRE_MINUTES=60
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,https://localhost:5173
```

For production, this app is configured for:
```env
FRONTEND_URL=https://poc-jade-sigma.vercel.app/
ALLOWED_ORIGINS=https://poc-jade-sigma.vercel.app,https://poc-jade-sigma.vercel.app/
```

Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup
```bash

npm install
npm run dev
```

## Testing the APIs
### Health
```bash
curl http://localhost:8000/health
```

### Decrypt SSO payload
```bash
curl -X POST http://localhost:8000/sso/decrypt \
  -H "Content-Type: application/json" \
  -d '{"key":"ENCRYPTED_GHL_PAYLOAD"}'
```

### Current session
```bash
curl http://localhost:8000/sso/session \
  -H "Authorization: Bearer JWT_FROM_DECRYPT_RESPONSE"
```

## GHL Custom Page Configuration
Point the GHL Marketplace Custom Page iframe to the frontend app root. The root route requests the encrypted SSO payload from the parent GHL window, validates it through the backend, and redirects to the dashboard after the JWT session is established.

## Security Notes
- The GHL shared secret is stored only on the backend.
- The frontend never decrypts the SSO payload.
- JWTs are stored in `sessionStorage`, not `localStorage`.
- Use HTTPS in production.
