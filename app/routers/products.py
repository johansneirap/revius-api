from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
async def read_products():
    """read products controller"""
    return [{"product": "product 1"}, {"product": "product 2"}]
