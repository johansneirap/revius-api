from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.dependencies import get_current_admin_user
from ..database import get_db
from ..schemas.product import ProductCreate, Product, PriceHistory
from ..models.user import User as UserModel
from ..models.product import (
    Product as ProductModel,
    PriceHistory as PriceHistoryModel,
    Store
)

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_admin_user)
):
    """Crear nuevo producto (solo admin)"""
    db_product = ProductModel(**product.dict(exclude={'store_ids'}))

    # Agregar tiendas al producto
    if product.store_ids:
        stores = db.query(Store).filter(Store.id.in_(product.store_ids)).all()
        db_product.stores = stores

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=List[Product])
async def read_products(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    min_rating: Optional[float] = None,
    store_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar productos con filtros opcionales"""
    query = db.query(ProductModel)

    if search:
        query = query.filter(ProductModel.name.ilike(f"%{search}%"))
    if min_rating:
        query = query.filter(ProductModel.average_rating >= min_rating)
    if store_id:
        query = query.filter(ProductModel.stores.any(id=store_id))

    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=Product)
async def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Obtener un producto específico"""
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{product_id}/price-history", response_model=List[PriceHistory])
async def read_product_price_history(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Obtener historial de precios de un producto"""
    history = db.query(PriceHistoryModel)\
        .filter(PriceHistoryModel.product_id == product_id)\
        .order_by(PriceHistoryModel.recorded_at.desc())\
        .all()
    return history
