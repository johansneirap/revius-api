from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
from ..models.user import User
from sqlalchemy.orm import Session
from .config import get_settings
from ..database import get_db
import jwt
from functools import lru_cache

settings = get_settings()
security = HTTPBearer()

@lru_cache()
def get_auth0_public_key():
    """Obtiene la clave pública de Auth0 para verificar tokens"""
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    return jwt.PyJWKClient(jwks_url)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Valida el token JWT y retorna el usuario actual
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        jwks_client = get_auth0_public_key()
        signing_key = jwks_client.get_signing_key_from_jwt(credentials.credentials)
        
        payload = jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=settings.AUTH0_ALGORITHMS,
            audience=settings.AUTH0_AUDIENCE,
            issuer=f"https://{settings.AUTH0_DOMAIN}/"
        )
        
        user = db.query(User).filter(User.auth0_id == payload["sub"]).first()
        if not user:
            raise credentials_exception
        
        return user
        
    except JWTError:
        raise credentials_exception