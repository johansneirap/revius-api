import pytest
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, Depends
from jose import jwt
from jose.exceptions import JWTError
from app.core.security import (
    get_jwks, get_signing_key,
    get_current_user)
from app.core.config import get_settings

settings = get_settings()
AUTH0_DOMAIN = settings.AUTH0_DOMAIN
AUTH0_AUDIENCE = settings.AUTH0_AUDIENCE
ALGORITHMS = settings.AUTH0_ALGORITHMS


@pytest.fixture
def token():
    # Generate a mock token for testing
    payload = {
        "sub": "auth0|123456789",
        "email": "test@example.com",
        "name": "Test User",
        "permissions": ["read:messages"]
    }
    token = jwt.encode(payload, "secret", algorithm=ALGORITHMS[0])
    return token


@pytest.fixture
def credentials(token):
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


def test_get_jwks(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"keys": [{"kid": "test_kid"}]}
    mocker.patch("requests.get", return_value=mock_response)

    jwks = get_jwks()
    assert jwks == {"keys": [{"kid": "test_kid"}]}

# Mock para get_jwks


@pytest.fixture
def mock_jwks(monkeypatch):
    mock_data = {
        "keys": [
            {
                "kid": "test-key-1",
                "kty": "RSA",
                "use": "sig",
                "n": "sample-n-value",
                "e": "AQAB"
            },
            {
                "kid": "test-key-2",
                "kty": "RSA",
                "use": "sig",
                "n": "another-n-value",
                "e": "AQAB"
            }
        ]
    }

    def mock_get_jwks():
        return mock_data

    monkeypatch.setattr("app.core.security.get_jwks", mock_get_jwks)
    return mock_data

# Test válido: token con kid coincidente


@pytest.mark.parametrize("kid", ["test-key-1", "test-key-2"])
def test_get_signing_key_valid(monkeypatch, mock_jwks, kid):
    # Crear un token ficticio
    token = "header.payload.signature"

    # Mock para jwt.get_unverified_header
    def mock_get_unverified_header(token):
        return {"kid": kid}

    monkeypatch.setattr(jwt, "get_unverified_header",
                        mock_get_unverified_header)

    # Llamar a la función
    key = get_signing_key(token)

    # Verificar el resultado
    assert key["kid"] == kid
    assert key["kty"] == "RSA"
    assert key["use"] == "sig"
    assert "n" in key
    assert "e" in key

# Test inválido: encabezado no verificable


def test_get_signing_key_invalid_header(monkeypatch, mock_jwks):
    token = "invalid.token"

    # Mock para jwt.get_unverified_header que lanza excepción
    def mock_get_unverified_header_error(token):
        raise JWTError("Invalid token")

    monkeypatch.setattr(jwt, "get_unverified_header",
                        mock_get_unverified_header_error)

    # Verificar que se lanza la excepción HTTP correcta
    with pytest.raises(HTTPException) as exc_info:
        get_signing_key(token)

    # Verificar el código de estado y el detalle
    assert exc_info.value.status_code == 401
    assert "encabezado no verificable" in exc_info.value.detail

# Test inválido: kid no encontrado


def test_get_signing_key_kid_not_found(monkeypatch, mock_jwks):
    token = "header.payload.signature"

    # Mock para jwt.get_unverified_header
    def mock_get_unverified_header(token):
        return {"kid": "non-existent-kid"}

    monkeypatch.setattr(jwt, "get_unverified_header",
                        mock_get_unverified_header)

    # Verificar que se lanza la excepción HTTP correcta
    with pytest.raises(HTTPException) as exc_info:
        get_signing_key(token)

    # Verificar el código de estado y el detalle
    assert exc_info.value.status_code == 401
    assert "Clave de firma no encontrada" in exc_info.value.detail


# @pytest.mark.asyncio
# async def test_get_current_user(mocker, credentials):
#     mocker.patch("app.core.security.verify_token", return_value={
#         "sub": "auth0|123456789",
#         "email": "test@example.com",
#         "name": "Test User",
#         "permissions": ["read:messages"]
#     })
#     user = await get_current_user()
#     assert user == UserFromAuth0(
#         user_id="auth0|123456789",
#         email="test@example.com",
#         name="Test User",
#         username="Test User",
#         permissions=["read:messages"]
#     )


# Fixtures para los payloads de prueba
@pytest.fixture
def valid_payload():
    return {
        "sub": "auth0|123456789",
        "email": "test@example.com",
        "name": "Test User",
        "permissions": ["read:items", "write:items"]
    }


@pytest.fixture
def payload_no_sub():
    return {
        "email": "test@example.com",
        "name": "Test User",
        "permissions": ["read:items"]
    }


@pytest.fixture
def payload_minimal():
    return {
        "sub": "auth0|987654321"
    }

# Mock para verify_token


@pytest.fixture
def mock_verify_token(monkeypatch, valid_payload):
    async def mock_verify_token_func():
        return valid_payload

    monkeypatch.setattr("your_auth_module.verify_token",
                        Depends(lambda: mock_verify_token_func))
    return mock_verify_token_func

# Test caso válido con payload completo


@pytest.mark.asyncio
async def test_get_current_user_valid(monkeypatch, valid_payload):
    # Prueba directamente con el payload sin usar Depends
    user = await get_current_user(valid_payload)

    # Verificar que el objeto usuario se creó correctamente
    assert user.user_id == "auth0|123456789"
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.username == "Test User"
    assert "read:items" in user.permissions
    assert "write:items" in user.permissions

# Test caso con payload mínimo (solo sub)


@pytest.mark.asyncio
async def test_get_current_user_minimal(monkeypatch, payload_minimal):
    user = await get_current_user(payload_minimal)

    # Verificar valores por defecto
    assert user.user_id == "auth0|987654321"
    assert user.email == "email@noemail.com"  # valor por defecto
    assert user.name == "name"  # valor por defecto
    assert user.username == "name"
    assert user.permissions == []

# Test caso sin 'sub' en el payload


@pytest.mark.asyncio
async def test_get_current_user_no_sub(monkeypatch, payload_no_sub):
    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(payload_no_sub)

    # Verificar excepción
    assert exc_info.value.status_code == 401
    assert "Información de usuario no válida" in exc_info.value.detail

# Test caso excepción general


@pytest.mark.asyncio
async def test_get_current_user_exception(monkeypatch):
    # Crear un payload que cause una excepción
    broken_payload = {"sub": None}

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(broken_payload)

    # Verificar excepción
    assert exc_info.value.status_code == 401
    assert "No se pudo obtener el usuario" in exc_info.value.detail

# Test integración con verify_token (opcional)


@pytest.mark.asyncio
async def test_get_current_user_with_depends(monkeypatch, valid_payload):
    # Este test es más complejo porque necesita simular Depends
    # Para una implementación real, deberías usar FastAPI TestClient

    # Mock para simular Depends(verify_token)
    async def mock_depends():
        return valid_payload

    # Llamada a la función
    user = await get_current_user(await mock_depends())

    # Verificaciones
    assert user.user_id == "auth0|123456789"
    assert "read:items" in user.permissions
