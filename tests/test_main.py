from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
client = TestClient(app)

settings = get_settings()


def test_read_root():
    response = client.get("/api/v1/")
    msg = f"Hello from {settings.PROJECT_NAME} {settings.VERSION}"
    assert response.status_code == 200
    assert response.json() == {"message": msg}


def test_get_version():
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_get_healthcheck():
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
