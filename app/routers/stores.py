from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.security import get_current_user
from ..core.dependencies import get_current_admin_user
from ..database import get_db
from ..schemas.product import StoreCreate, Store
from ..models.product import Store as StoreModel
from ..models.user import User as UserModel

router = APIRouter(
    prefix="/stores",
    tags=["stores"]
)

@router.post("/", response_model=Store)
async def create_store(
    store: StoreCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Crear nueva tienda (solo admin)"""
    db_store = StoreModel(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

@router.get("/", response_model=List[Store])
async def read_stores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar todas las tiendas"""
    stores = db.query(StoreModel).offset(skip).limit(limit).all()
    return stores