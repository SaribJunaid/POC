# GoHighLevel Custom Menu Link Authentication POC

This repository contains a minimal but production-oriented proof of concept for opening an external web application from a GoHighLevel custom menu link, discovering the current GHL context, and authorizing the current user via the GHL API using a backend-only Private Integration Token.

## Architecture
- Frontend: React + Vite + JavaScript
- Backend: FastAPI + Python
- Communication: frontend calls the backend over HTTP, and the backend calls the GHL API using a private token stored only on the backend.

## Project Structure
```text
ghl-auth-poc/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── ghl_client.py
│   │   ├── auth.py
│   │   ├── schemas.py
│   │   └── context.py
│   ├── .env.example
│   ├── .gitignore
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoadingScreen.jsx
│   │   │   ├── AccessDenied.jsx
│   │   │   ├── Authorized.jsx
│   │   │   └── DebugPanel.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── utils/
│   │   │   └── ghlContext.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── .env.example
│   ├── .gitignore
│   ├── package.json
│   └── README.md
├── .gitignore
└── README.md
```

## Prerequisites
- Python 3.10+
- Node.js 18+
- A valid GHL Private Integration Token

## Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Update `.env` with your real values:
```env
GHL_API_TOKEN=your_private_integration_token
GHL_API_BASE_URL=https://services.leadconnectorhq.com
FRONTEND_URL=http://localhost:5173
ALLOWED_ORIGINS=http://localhost:5173,https://localhost:5173
```

Run the backend:
```bash
uvicorn app.main:app --reload --port 8000
```

## Frontend Setup
```bash
cd frontend
npm install
copy .env.example .env
```

Run the frontend:
```bash
npm run dev
```

## Testing the APIs
### Health
```bash
curl http://localhost:8000/health
```

### Location context
```bash
curl "http://localhost:8000/api/ghl/context?location_id=LOCATION_ID"
```

### Authorization validation
```bash
curl -X POST http://localhost:8000/api/auth/validate \
  -H "Content-Type: application/json" \
  -d '{"location_id":"LOCATION_ID","user_id":"USER_ID","email":"user@example.com"}'
```

## GHL Custom Menu Link Configuration
Use a custom menu link that opens your frontend app with a URL such as:
```text
https://YOUR_DOMAIN.com/?locationId={{location.id}}
```

If GHL provides additional parameters, the frontend will detect them without breaking.

## Testing Different Users
The example users below are for validation only. The app uses live GHL API responses rather than hardcoded values.

- Muhammad Kashir (`kashir@gmail.com`) → expected DENIED (role: user)
- Muhammad Usman (`usman@gmail.com`) → expected AUTHORIZED (role: admin)
- Sarib Junaid (`sarib.irenic@gmail.com`) → expected AUTHORIZED (agency owner)

## Authorization Logic
The backend checks:
1. The requested location exists.
2. The user can be found in the GHL account for the matching company.
3. The user belongs to the requested location.
4. The user is either an admin or an agency owner.

## Security Notes
- The GHL private token is stored only on the backend.
- The frontend never receives the token.
- The app avoids cross-origin parent window access and uses only safe browser mechanisms.
- Use HTTPS for deployment.

## Known Limitations
- This is a proof of concept, not a full identity or permission platform.
- The app depends on what the GHL environment exposes through the URL, iframe context, or postMessage.
- Exact endpoint behavior may vary slightly depending on the tenant/account configuration.
