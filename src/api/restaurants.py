from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.restaurant import get_restaurants, create_restaurant, get_restaurant_by_id, delete_restaurant
from src.schemas.restaurant import Restaurant, RestaurantCreate

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[Restaurant])
def read_restaurants(db: Session = Depends(get_db)):
    restaurants = get_restaurants(db)
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")
    return restaurants

@router.post("/", response_model=Restaurant)
def create_new_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    return create_restaurant(db, restaurant)
