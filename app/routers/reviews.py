from fastapi import APIRouter

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/")
async def read_reviews():
    """read reviews controller"""
    return [{"review": "review 1"}, {"review": "review 2"}]
