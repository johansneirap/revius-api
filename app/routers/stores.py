from fastapi import APIRouter

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("/")
async def read_stores():
    """read stores controller"""
    return [{"store": "Store 1"}, {"store": "Store 2"}]
