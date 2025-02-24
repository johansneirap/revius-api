from fastapi import FastAPI
from app.routers import comments, favorites, products, reviews, stores, users
from app.core.config import get_settings

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
async def get_healthcheck():
    """Endpoint to get the healthcheck of the application"""
    return {"status": "ok"}
