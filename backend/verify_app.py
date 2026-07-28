from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
print(client.get('/health').json())
try:
    resp = client.get('/api/ghl/context?location_id=test')
    print(resp.status_code)
    print(resp.text)
except Exception as exc:
    print(type(exc).__name__, exc)
