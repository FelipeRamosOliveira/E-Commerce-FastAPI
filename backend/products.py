from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Product
from ..schemas import ProductCreate, ProductOut
from ..users import get_current_admin

router = APIRouter()

@router.post("/products", response_model=ProductOut, dependencies=[Depends(get_current_admin)])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, description=product.description, price=product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/products", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
