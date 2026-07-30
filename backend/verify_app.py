from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
print(client.get('/health').json())
