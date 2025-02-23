from fastapi import FastAPI
from app.version import VERSION
from app.constants.api_properties import GLOBAL_PREFIX
from app.routers import comments, favorites, products, reviews, stores, users

app = FastAPI()

app.router.prefix = GLOBAL_PREFIX
app.include_router(users.router)
app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(comments.router)
app.include_router(stores.router)
app.include_router(favorites.router)


@app.get("/")
async def root():
    """read root function"""
    return {"message": f"Hello from Revius API {VERSION}"}

@app.get("/version")
async def get_version():
    """Endpoint to get the version of the application"""
    return {"version": VERSION}

@app.get("/healthcheck")
async def get_healthcheck():
    """Endpoint to get the healthcheck of the application"""
    return {"status": "ok"}
