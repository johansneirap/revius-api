from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal

class StoreBase(BaseModel):
    name: str
    website: str

class Store(StoreBase):
    id: int
    
    class Config:
        from_attributes = True

class StoreCreate(StoreBase):
    pass

class ProductBase(BaseModel):
    name: str
    description: str
    current_price: Decimal

class ProductCreate(ProductBase):
    store_ids: List[int]

class Product(ProductBase):
    id: int
    average_rating: float
    review_count: int
    created_at: datetime
    stores: List[Store]
    
    class Config:
        from_attributes = True

class PriceHistoryBase(BaseModel):
    price: Decimal
    recorded_at: datetime

class PriceHistory(PriceHistoryBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True
