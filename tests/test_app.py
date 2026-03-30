from fastapi.testclient import TestClient

from app.main import app


def test_root_returns_html():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Disney Bot" in response.text


def test_api_status():
    client = TestClient(app)
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["status"] == "idle"
