from fastapi import APIRouter

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/")
async def read_favorites():
    """read favorites controller"""
    return [{"favorite": "favorite 1"}, {"favorite": "favorite 2"}]
