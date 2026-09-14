from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_decisions():
    response = client.get("/api/decisions/")
    # Could be empty initially or return 401 if auth is enforced heavily, 
    # but based on current routing it should return 200 list or 401.
    assert response.status_code in [200, 401]

