from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from .relationships import product_store


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    current_price = Column(Float)
    average_rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    reviews = relationship("Review", back_populates="product")
    price_history = relationship("PriceHistory", back_populates="product")
    stores = relationship("Store", secondary=product_store,
                          back_populates="products")


class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    website = Column(String)

    # Relaciones
    products = relationship(
        "Product", secondary=product_store, back_populates="stores")


class PriceHistory(Base):
    __tablename__ = 'price_history'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    price = Column(Float)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    product = relationship("Product", back_populates="price_history")
