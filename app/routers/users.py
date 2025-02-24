from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.security import get_current_user
from ..core.dependencies import get_current_admin_user
from ..database import get_db
from ..schemas.user import UserCreate, User, UserUpdate
from ..models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def read_user_me(
    current_user: UserModel = Depends(get_current_user)
):
    """Obtener información del usuario actual"""
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar información del usuario actual"""
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios (solo admin)"""
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users
