from sqlalchemy.orm import Session
from fastapi import HTTPException
from .models import Sale
from .schemas import SaleCreate

# Get the total number of sales
def get_sales_count(db: Session):
    return {"Sales": db.query(Sale).count()}

# Get a sale by its ID
def get_sale_by_id(sale_id: int, db: Session):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale:
        return {
            "id": sale.id,
            "item": sale.item,
            "unit_price": sale.unit_price,
            "quantity": sale.quantity,
        }
    raise HTTPException(status_code=404, detail="Sale ID does not exist")

# Create a new sale
def create_new_sale(sale: SaleCreate, db: Session):
    new_sale = Sale(item=sale.item, unit_price=sale.unit_price, quantity=sale.quantity)
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

def oi():
    return "oi"