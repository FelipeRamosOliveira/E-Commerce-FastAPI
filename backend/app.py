import warnings
warnings.filterwarnings("ignore")
#
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Sale, Base
from .schemas import SaleCreate
from .crud import get_sales_count, get_sale_by_id, create_new_sale

# Initialize the FastAPI app
app = FastAPI()

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Redirect root URL to documentation
@app.get("/")
def home():
    return RedirectResponse(url="/docs")

# Route to get total sales count
@app.get("/sales")
def sales_count(db: Session = Depends(get_db)):
    return get_sales_count(db)

# Route to get a sale by ID
@app.get("/sales/{sale_id}")
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    return get_sale_by_id(sale_id, db)

# Route to create a new sale
@app.post("/sales", response_model=SaleCreate)
def new_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    return create_new_sale(sale, db)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    if db.query(Sale).count() == 0:
        # Populate mock data if the table is empty
        mock_sales = [
            {"item": "can", "unit_price": 4, "quantity": 5},
            {"item": "2L bottle", "unit_price": 15, "quantity": 5},
            {"item": "750ml bottle", "unit_price": 10, "quantity": 5},
            {"item": "mini can", "unit_price": 2, "quantity": 5},
        ]
        for sale_data in mock_sales:
            sale = Sale(**sale_data)
            db.add(sale)
        db.commit()
