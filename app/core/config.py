import os
from pydantic import BaseModel, ConfigDict
from typing import Optional
from functools import lru_cache
from app.version import VERSION


class Settings(BaseModel):
    PROJECT_NAME: str = "Review API"
    VERSION: str = VERSION
    GLOBAL_API_PREFIX: str = "/api/v1"

    # PostgreSQL
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
    DB_NAME: str = os.getenv("DB_NAME", "reviewdb")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    # Auth0
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "my-domain.auth0.com")
    AUTH0_AUDIENCE: str = os.getenv("AUTH0_AUDIENCE", "your-api-identifier")
    AUTH0_ALGORITHMS: list = ["RS256"]

    # AWS S3 (para almacenamiento de imágenes)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_BUCKET_NAME: Optional[str] = None

    model_config = ConfigDict(env_file=".env", case_sensitive=True)


@lru_cache()
def get_settings() -> Settings:
    """Retorna una instancia cacheada de la aplicación"""
    return Settings()
