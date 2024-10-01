from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Cart, Product, Order
from ..users import get_current_user

router = APIRouter()

@router.post("/cart/add")
def add_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    cart_item = Cart(user_id=user.id, product_id=product.id, quantity=quantity)
    db.add(cart_item)
    db.commit()
    return {"message": "Item added to cart"}

@router.post("/cart/order")
def place_order(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart_items = db.query(Cart).filter(Cart.user_id == user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = sum(item.quantity * item.product.price for item in cart_items)
    new_order = Order(user_id=user.id, total_price=total_price, status="Placed")
    db.add(new_order)
    db.commit()

    # Clear cart
    db.query(Cart).filter(Cart.user_id == user.id).delete()
    db.commit()
    return {"message": "Order placed successfully"}