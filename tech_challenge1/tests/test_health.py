from fastapi.testclient import TestClient
from tech_challenge1.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200