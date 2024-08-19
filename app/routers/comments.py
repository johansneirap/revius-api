from fastapi import APIRouter

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/")
async def read_comments():
    """read comments controller"""
    return [{"comment": "comment 1"}, {"comment": "comment 2"}]
