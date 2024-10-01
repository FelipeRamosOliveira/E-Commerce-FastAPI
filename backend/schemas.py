from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int

class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user_id: int
    products: List[int]  # List of product IDs
