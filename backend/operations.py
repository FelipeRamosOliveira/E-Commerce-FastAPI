from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=400, detail="Username already registered")

    return db_user

def get_user(db: Session, username: str):
    """
    Retrieve a user by username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())

    try:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Product already exists")

    return db_product

# def get_products(db: Session):
#     return db.query(models.Product).all()

def get_products(db: Session):
    try:
        products = db.query(models.Product).all()
        logging.info(f"Found {len(products)} products.")
        return products
    except Exception as e:
        logging.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(user_id=order.user_id, products=str(order.products))

    try:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    except Exception as e:  # Catch other exceptions, such as IntegrityError
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating order: " + str(e))

    return db_order
