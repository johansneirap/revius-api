from fastapi import FastAPI

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
    return {"message": "Hello from Revius API"}
