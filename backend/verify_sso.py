from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
print('health', client.get('/health').status_code)
print('session', client.get('/sso/session').status_code)
