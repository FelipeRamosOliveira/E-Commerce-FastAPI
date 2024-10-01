from pydantic import BaseModel

# Pydantic model for creating a new sale
class SaleCreate(BaseModel):
    item: str
    unit_price: int
    quantity: int

    class Config:
        orm_mode = True
    