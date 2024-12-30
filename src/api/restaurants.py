from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.restaurant import (
    get_restaurants,
    get_restaurant_by_id,
    create_restaurant,
    update_restaurant,
    delete_restaurant
)
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

# Read all restaurants
@router.get("/", response_model=list[Restaurant])
def read_restaurants(db: Session = Depends(get_db)):
    restaurants = get_restaurants(db)
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")
    return restaurants

# Read a restaurant by ID
@router.get("/{restaurant_id}", response_model=Restaurant)
def read_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = get_restaurant_by_id(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

# Create a new restaurant
@router.post("/", response_model=Restaurant)
def create_new_restaurant(restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    return create_restaurant(db, restaurant)

# Update a restaurant by ID
@router.put("/{restaurant_id}", response_model=Restaurant)
def update_restaurant_by_id(restaurant_id: int, restaurant: RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = update_restaurant(db, restaurant_id, restaurant)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant

# Delete a restaurant by ID
@router.delete("/{restaurant_id}", response_model=Restaurant)
def delete_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    db_restaurant = delete_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return db_restaurant
