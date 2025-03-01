from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from jose.exceptions import JWTError
from app.core.config import get_settings
from app.schemas.user import UserFromAuth0
import requests

app = FastAPI()
security = HTTPBearer()

# Configuración de Auth0
settings = get_settings()
AUTH0_DOMAIN = settings.AUTH0_DOMAIN
AUTH0_AUDIENCE = settings.AUTH0_AUDIENCE
ALGORITHMS = settings.AUTH0_ALGORITHMS

# Cache para las claves JWKS
jwks_cache = None


def get_jwks():
    global jwks_cache
    if jwks_cache is None:
        jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
        response = requests.get(jwks_url)
        jwks_cache = response.json()
    return jwks_cache


def get_signing_key(token):
    jwks = get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: encabezado no verificable"
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Clave de firma no encontrada"
    )


async def verify_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        signing_key = get_signing_key(token)
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=ALGORITHMS,
            audience=AUTH0_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}"
        )


async def get_current_user(
    payload: dict = Depends(verify_token)
) -> UserFromAuth0:
    """
    Dependencia para obtener el usuario actual basado en el token JWT
    """
    try:
        # Campo "sub" contiene el ID del user en Auth0 (ej: "auth0|123456789")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Información de usuario no válida en el token"
            )

        # Extraer información adicional del token
        email = payload.get("email", "email@noemail.com")
        name = payload.get("name", "name")

        # Si usas permisos en Auth0, pueden estar en el claim "permissions"
        permissions = payload.get("permissions", [])

        return UserFromAuth0(
            user_id=user_id,
            email=email,
            name=name,
            username=name,
            permissions=permissions
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No se pudo obtener el usuario: {str(e)}"
        )
