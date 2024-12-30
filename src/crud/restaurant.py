from sqlalchemy.orm import Session
from src.models.restaurant import Restaurant
from src.schemas.restaurant import RestaurantCreate

def get_restaurants(db: Session):
    """Retrieve all restaurants from the database."""
    return db.query(Restaurant).all()

def get_restaurant_by_id(db: Session, restaurant_id: int):
    """Retrieve a single restaurant by ID."""
    return db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()

def get_restaurant_by_name(db: Session, name: str):
    """Retrieve restaurants by their name."""
    return db.query(Restaurant).filter(Restaurant.restaurant_name.ilike(f"%{name}%")).all()

def create_restaurant(db: Session, restaurant: RestaurantCreate):
    """Create a new restaurant."""
    db_restaurant = Restaurant(
        restaurant_name=restaurant.restaurant_name,
        restaurant_cuisine=restaurant.restaurant_cuisine,
        restaurant_website=restaurant.restaurant_website,
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def delete_restaurant(db: Session, restaurant_id: int):
    """Delete a restaurant by ID."""
    db_restaurant = get_restaurant_by_id(db, restaurant_id)
    if db_restaurant:
        db.delete(db_restaurant)
        db.commit()
    return db_restaurant
