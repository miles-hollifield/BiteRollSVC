from sqlalchemy.orm import Session
from src.models.restaurant import Restaurant
from src.schemas.restaurant import RestaurantCreate

# Retrieve all restaurants
def get_restaurants(db: Session):
    return db.query(Restaurant).all()

# Retrieve a restaurant by ID
def get_restaurant_by_id(db: Session, restaurant_id: int):
    return db.query(Restaurant).filter(Restaurant.restaurant_id == restaurant_id).first()

# Create a new restaurant
def create_restaurant(db: Session, restaurant: RestaurantCreate):
    db_restaurant = Restaurant(
        restaurant_name=restaurant.restaurant_name,
        restaurant_cuisine=restaurant.restaurant_cuisine,
        restaurant_website=restaurant.restaurant_website
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

# Update an existing restaurant by ID
def update_restaurant(db: Session, restaurant_id: int, restaurant: RestaurantCreate):
    db_restaurant = get_restaurant_by_id(db, restaurant_id)
    if db_restaurant:
        db_restaurant.restaurant_name = restaurant.restaurant_name
        db_restaurant.restaurant_cuisine = restaurant.restaurant_cuisine
        db_restaurant.restaurant_website = restaurant.restaurant_website
        db.commit()
        db.refresh(db_restaurant)
    return db_restaurant

# Delete a restaurant by ID
def delete_restaurant(db: Session, restaurant_id: int):
    db_restaurant = get_restaurant_by_id(db, restaurant_id)
    if db_restaurant:
        db.delete(db_restaurant)
        db.commit()
    return db_restaurant
