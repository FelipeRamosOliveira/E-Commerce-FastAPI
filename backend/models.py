from sqlalchemy import Column, Integer, String
from .database import Base

# Sale model that maps to the 'sales' table in the database
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    unit_price = Column(Integer)
    quantity = Column(Integer)