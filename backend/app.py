import warnings
warnings.filterwarnings("ignore")

# FastAPI and dependencies
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import logging
from sqlalchemy import func

# Local modules
from .auth import hash_password
from .database import SessionLocal, engine
from .models import Base, Product, User
from .logging import setup_logging
from .schemas import UserSchema, UserCreate, ProductSchema
from .operations import create_user, get_user, get_products

# Initialize the FastAPI app
app = FastAPI()

# Setup logging configuration
setup_logging()
logging.basicConfig(level=logging.INFO)

# Middleware for logging requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return RedirectResponse(url="/docs")

@app.post("/users/", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

@app.get("/products/", response_model=List[ProductSchema])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)

# Carrinho como lista para armazenar os produtos adicionados
cart = []

@app.post("/add-to-cart/")
def add_to_cart(product_name: str, db: Session = Depends(get_db)):
    """
    Adiciona um produto ao carrinho com base no nome do produto.
    """
    # Normaliza o nome do produto para remoção de acentos
    normalized_product_name = product_name.lower()

    # Busca o produto no banco de dados, ignorando maiúsculas/minúsculas e acentos
    product = db.query(Product).filter(func.lower(Product.name) == normalized_product_name).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Adiciona o produto ao carrinho
    cart.append(product)
    return {"message": f"{product_name} added to cart", "cart_size": len(cart)}

@app.get("/cart/")
def view_cart(name: str = "Customer"):
    """
    Exibe o conteúdo do carrinho e o total de preços.
    """
    total_price = sum(product.price for product in cart)
    cart_items = [{"name": product.name, "price": product.price} for product in cart]

    # Frase bacana
    return {
        "message": f"Thank you for shopping with us, {name}! Here's your cart:",
        "cart": cart_items,
        "total_price": total_price
    }

@app.on_event("startup")
def startup():
    db = SessionLocal()
    existing_products = {product.name for product in db.query(Product).all()}
    mock_products = [
        {"name": "Skol", "description": "Light beer", "price": 1.5},
        {"name": "Brahma", "description": "Premium lager", "price": 1.8},
        {"name": "Antarctica", "description": "Pale lager", "price": 1.6},
        {"name": "Guaraná Antarctica", "description": "Soft drink", "price": 1.2},
        {"name": "Beck's", "description": "German pilsner beer", "price": 2},
        {"name": "Ambev Beer", "description": "Refreshing beer from Ambev", "price": 10},
    ]
    for product_data in mock_products:
        if product_data["name"] not in existing_products:
            product = Product(**product_data)
            db.add(product)
    db.commit()
    db.close()

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
