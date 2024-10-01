from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./sales.db"  # SQLite database file
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # Database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory
Base = declarative_base()  # Base class for declarative class definitions

# Sales model definition
class Sale(Base):
    __tablename__ = "sales"  # Table name in the database

    # Columns in the sales table
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    item = Column(String, index=True)  # Item name
    unit_price = Column(Integer)  # Price of the item
    quantity = Column(Integer)  # Quantity of the item

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app instance
app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session for route use
    finally:
        db.close()  # Close session

@app.get("/")  # Redirect root URL to documentation
def home():
    return RedirectResponse(url="/docs")

@app.get("/sales")  # Get total sales count
def get_sales_count(db: Session = Depends(get_db)):
    count = db.query(Sale).count()  # Count sales in the database
    return {"Sales": count}

@app.get("/sales/{sale_id}")  # Get sale by ID
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()  # Find sale by ID
    if sale:
        return {
            "id": sale.id,
            "item": sale.item,
            "unit_price": sale.unit_price,
            "quantity": sale.quantity,
        }
    else:
        raise HTTPException(status_code=404, detail="Sale ID does not exist")  # 404 if not found

# Pydantic model for creating new sales
class SaleCreate(BaseModel):
    item: str  # Item name
    unit_price: int  # Price per unit
    quantity: int  # Quantity available

@app.post("/sales", response_model=SaleCreate)  # Create a new sale
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    new_sale = Sale(item=sale.item, unit_price=sale.unit_price, quantity=sale.quantity)  # Create new sale instance
    db.add(new_sale)  # Add to session
    db.commit()  # Commit to database
    db.refresh(new_sale)  # Refresh to get updated data
    return new_sale  # Return created sale

@app.on_event("startup")  # Populate mock data on startup
def startup():
    db = SessionLocal()  # Create a new session
    if db.query(Sale).count() == 0:  # Check if database is empty
        mock_sales = [  # Mock sales data
            {"item": "can", "unit_price": 4, "quantity": 5},
            {"item": "2L bottle", "unit_price": 15, "quantity": 5},
            {"item": "750ml bottle", "unit_price": 10, "quantity": 5},
            {"item": "mini can", "unit_price": 2, "quantity": 5},
        ]
        for sale_data in mock_sales:
            sale = Sale(**sale_data)  # Create sale instance
            db.add(sale)  # Add to session
        db.commit()  # Commit mock data
