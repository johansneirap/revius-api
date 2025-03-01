import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy.exc import DatabaseError
from app.main import app
from app.core.config import get_settings
from app.main import get_healthcheck, get_db

client = TestClient(app)
settings = get_settings()
BASE_PATH = settings.GLOBAL_API_PREFIX


class MockDBSession:
    def __init__(self, working=True):
        self.working = working

    def execute(self, query):
        if not self.working:
            raise DatabaseError("Database connection error", None, None)
        return "Success"

    def close(self):
        pass


@pytest.fixture
def db_working():
    return MockDBSession(working=True)


@pytest.fixture
def db_error():
    return MockDBSession(working=False)


@pytest.fixture
def override_get_db(monkeypatch, db_working):
    def mock_get_db():
        return db_working

    monkeypatch.setattr("your_app.get_db", mock_get_db)
    return mock_get_db


def test_read_root():
    response = client.get(BASE_PATH)
    msg = f"Hello from {settings.PROJECT_NAME} {settings.VERSION}"
    assert response.status_code == 200
    assert response.json() == {"message": msg}


def test_get_version():
    response = client.get(f"{BASE_PATH}/version")
    assert response.status_code == 200
    assert "version" in response.json()


@pytest.mark.asyncio
async def test_healthcheck_db_connected(monkeypatch, db_working):
    result = await get_healthcheck(db=db_working)

    assert result["status"] == "ok"
    assert result["database"] == "connected"
    assert result["api"] == "running"

# Test para base de datos desconectada


@pytest.mark.asyncio
async def test_healthcheck_db_error(monkeypatch, db_error):
    result = await get_healthcheck(db=db_error)

    assert result["status"] == "error"
    assert result["database"] == "disconnected"
    assert "error" in result


@pytest.mark.asyncio
async def test_healthcheck_with_dependency(monkeypatch):
    db_mock = MockDBSession(working=True)

    async def mock_get_db():
        return db_mock

    monkeypatch.setattr("app.main.get_db", Depends(lambda: mock_get_db))
    db = await mock_get_db()
    result = await get_healthcheck(db)

    assert result["status"] == "ok"
    assert result["database"] == "connected"


def test_healthcheck_endpoint(monkeypatch):
    def mock_get_db():
        return MockDBSession(working=True)

    app.dependency_overrides[get_db] = mock_get_db

    response = client.get("api/v1/healthcheck")
    data = response.json()

    assert response.status_code == 200
    assert data["status"] == "ok"
    assert data["database"] == "connected"
    app.dependency_overrides.clear()
