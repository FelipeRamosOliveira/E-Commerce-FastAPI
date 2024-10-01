import warnings
warnings.filterwarnings("ignore")

# FastAPI and dependencies
from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

# Local modules
import logging
from .auth import hash_password
from .database import SessionLocal, engine
from .models import Base, Product, User
from .logging import setup_logging
from .schemas import UserSchema, UserCreate, ProductSchema, ProductCreate, OrderCreate
from .operations import (
    create_user,
    get_user,
    create_product,
    get_products,
    create_order
)

# Initialize the FastAPI app
app = FastAPI()

# Setup logging configuration
setup_logging()
logging.basicConfig(level=logging.INFO)

# Middleware for logging requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log incoming requests and outgoing responses.
    """
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    """
    Provide a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redirect root URL to documentation
@app.get("/")
def home():
    """
    Redirect to FastAPI documentation.
    """
    return RedirectResponse(url="/docs")

# User management routes
@app.post("/users/", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

# Product management routes
@app.post("/products/", response_model=ProductSchema)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Add a new product.
    """
    return create_product(db=db, product=product)

@app.get("/products/", response_model=List[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    """
    List all products.
    """
    return get_products(db=db)

# Order management route
@app.post("/orders/", response_model=OrderCreate)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Place a new order.
    """
    return create_order(db=db, order=order)

# Startup event to populate mock data
@app.on_event("startup")
def startup():
    """
    Populate mock products and users data if tables are empty.
    """
    db = SessionLocal()

    # Populate mock products data if the products table is empty
    if db.query(Product).count() == 0:
        mock_products = [
            {"name": "Skol", "description": "Light beer", "price": 1.5},
            {"name": "Brahma", "description": "Premium lager", "price": 1.8},
            {"name": "Antarctica", "description": "Pale lager", "price": 1.6},
            {"name": "Guaraná Antarctica", "description": "Soft drink", "price": 1.2},
            {"name": "Beck's", "description": "German pilsner beer", "price": 2.0},
        ]
        for product_data in mock_products:
            product = Product(**product_data)
            db.add(product)
        db.commit()
    
    # Populate mock users data if the users table is empty
    if db.query(User).count() == 0:
        mock_users = [
            {"username": "user1", "hashed_password": hash_password("hashedpassword1")},
            {"username": "user2", "hashed_password": hash_password("hashedpassword2")},
            {"username": "admin", "hashed_password": hash_password("hashedadminpassword")},
        ]
        for user_data in mock_users:
            user = User(**user_data)
            db.add(user)
        db.commit()
