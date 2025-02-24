from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

product_store = Table(
    'product_store',
    Base.metadata,
    Column('product_id', Integer, ForeignKey('products.id')),
    Column('store_id', Integer, ForeignKey('stores.id'))
)
