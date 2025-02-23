from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users():
    """read users controller"""
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    """read current user controller"""
    return {"username": "fakecurrentuser"}


@router.get("/{username}")
async def read_user(username: str):
    """read user controller"""
    return {"username": username}
