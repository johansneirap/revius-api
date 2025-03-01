from fastapi import FastAPI, Depends
from app.routers import comments, favorites, products, reviews, stores, users
from app.core.config import get_settings
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

app = FastAPI()
settings = get_settings()

app.router.prefix = settings.GLOBAL_API_PREFIX
app.include_router(users.router)
app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(comments.router)
app.include_router(stores.router)
app.include_router(favorites.router)


@app.get("/")
async def root():
    """read root function"""
    msg = f"Hello from {settings.PROJECT_NAME} {settings.VERSION}"
    return {"message": msg}


@app.get("/version")
async def get_version():
    """Endpoint to get the version of the application"""
    return {"version": settings.VERSION}


@app.get("/healthcheck")
async def get_healthcheck(db: Session = Depends(get_db)):
    """Endpoint to get the healthcheck of the application"""
    try:
        # Intentar ejecutar una query simple para verificar la base de datos
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "api": "running"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}
