from fastapi.testclient import TestClient
from fleetpulse.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_anomalies_endpoint():
    response = client.get("/anomalies?limit=5")
    assert response.status_code == 200
    assert len(response.json()) <= 5
