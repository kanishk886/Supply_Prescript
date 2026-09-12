import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_roi_endpoint():
    response = client.get("/api/roi")
    assert response.status_code == 200
    assert "roi_percentage" in response.json()
