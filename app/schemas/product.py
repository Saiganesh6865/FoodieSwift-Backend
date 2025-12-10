from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category: str
    rating: float = 4.5

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    
    class Config:
        from_attributes = True
