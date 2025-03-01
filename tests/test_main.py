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


# Mock para la sesión de base de datos
class MockDBSession:
    def __init__(self, working=True):
        self.working = working

    def execute(self, query):
        if not self.working:
            raise DatabaseError("Database connection error", None, None)
        return "Success"

    def close(self):
        pass

# Fixtures para simular diferentes estados de la base de datos


@pytest.fixture
def db_working():
    return MockDBSession(working=True)


@pytest.fixture
def db_error():
    return MockDBSession(working=False)

# Mock para get_db


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


def test_get_healthcheck():
    response = client.get(f"{BASE_PATH}/healthcheck")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "database": "connected",
        "api": "running"
    }


@pytest.mark.asyncio
async def test_healthcheck_db_connected(monkeypatch, db_working):
    # Simular directamente la inyección de dependencia
    result = await get_healthcheck(db=db_working)

    assert result["status"] == "ok"
    assert result["database"] == "connected"
    assert result["api"] == "running"

# Test para base de datos desconectada


@pytest.mark.asyncio
async def test_healthcheck_db_error(monkeypatch, db_error):
    # Simular directamente la inyección de dependencia
    result = await get_healthcheck(db=db_error)

    assert result["status"] == "error"
    assert result["database"] == "disconnected"
    assert "error" in result

# Test de integración usando la dependencia


@pytest.mark.asyncio
async def test_healthcheck_with_dependency(monkeypatch):
    # Mock del objeto de sesión
    db_mock = MockDBSession(working=True)

    # Mock de la función get_db
    async def mock_get_db():
        return db_mock

    # Aplicar el mock
    monkeypatch.setattr("app.main.get_db", Depends(lambda: mock_get_db))

    # Para una prueba más completa, deberías usar TestClient de FastAPI
    # Pero podemos simular manualmente el comportamiento:
    db = await mock_get_db()
    result = await get_healthcheck(db)

    assert result["status"] == "ok"
    assert result["database"] == "connected"

# Test más completo usando TestClient (recomendado)


def test_healthcheck_endpoint(monkeypatch):
    # Mock de la función get_db
    def mock_get_db():
        return MockDBSession(working=True)

    # Aplicar el mock
    app.dependency_overrides[get_db] = mock_get_db

    # Realizar solicitud
    response = client.get("api/v1/healthcheck")

    # Verificar respuesta
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"

    # Limpiar después de la prueba
    app.dependency_overrides.clear()
