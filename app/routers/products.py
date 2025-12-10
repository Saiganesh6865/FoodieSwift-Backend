from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductOut, ProductCreate

router = APIRouter(prefix='/products', tags=['products'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@router.post('/seed', status_code=201)
def seed_products(db: Session = Depends(get_db)):
    # Clear existing
    db.query(Product).delete()
    
    sample_products = [
        {
            "name": "Spicy Chicken Burger",
            "description": "Juicy chicken patty with spicy mayo and fresh lettuce.",
            "price": 149.0,
            "category": "Burger",
            "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=60",
            "rating": 4.8
        },
        {
            "name": "Margherita Pizza",
            "description": "Classic delight with 100% real mozzarella cheese.",
            "price": 299.0,
            "category": "Pizza",
            "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&auto=format&fit=crop&q=60",
            "rating": 4.5
        },
        {
            "name": "Veggie Taco",
            "description": "Loaded with fresh veggies and tangy sauce.",
            "price": 99.0,
            "category": "Mexican",
            "image_url": "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=500&auto=format&fit=crop&q=60",
            "rating": 4.3
        },
        {
            "name": "Fresh Sushi Platter",
            "description": "Assorted sushi rolls with wasabi and soy sauce.",
            "price": 599.0,
            "category": "Asian",
            "image_url": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&auto=format&fit=crop&q=60",
            "rating": 4.9
        },
        {
            "name": "Chocolate Lava Cake",
            "description": "Gooey molten chocolate center.",
            "price": 120.0,
            "category": "Dessert",
            "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476d?w=500&auto=format&fit=crop&q=60",
            "rating": 4.7
        },
         {
            "name": "Iced Coffee",
            "description": "Cold brewed coffee with milk and ice.",
            "price": 150.0,
            "category": "Drinks",
            "image_url": "https://images.unsplash.com/photo-1517701604599-bb29b5c73553?w=500&auto=format&fit=crop&q=60",
            "rating": 4.6
        }
    ]
    
    for p_data in sample_products:
        db.add(Product(**p_data))
        
    db.commit()
    return {"message": "Products seeded successfully"}
