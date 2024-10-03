# backend/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Column, Integer, Float, String  
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    orders = relationship("Order", back_populates="owner")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    products = Column(String)  # Simplified for demonstration
    owner = relationship("User", back_populates="orders")

