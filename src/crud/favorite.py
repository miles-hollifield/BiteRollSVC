from sqlalchemy.orm import Session
from src.models.favorite import Favorite
from src.schemas.favorite import FavoriteCreate

# Retrieve all favorites
def get_favorites(db: Session):
    return db.query(Favorite).all()

# Retrieve a favorite by ID
def get_favorite_by_id(db: Session, favorite_id: int):
    return db.query(Favorite).filter(Favorite.favorite_id == favorite_id).first()

# Create a new favorite
def create_favorite(db: Session, favorite_data: FavoriteCreate):
    db_favorite = Favorite(
        user_id=favorite_data.user_id,
        restaurant_id=favorite_data.restaurant_id,
    )
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

# Update an existing favorite by ID
def update_favorite(db: Session, favorite_id: int, favorite_data: FavoriteCreate):
    db_favorite = get_favorite_by_id(db, favorite_id)
    if db_favorite:
        db_favorite.user_id = favorite_data.user_id
        db_favorite.restaurant_id = favorite_data.restaurant_id
        db.commit()
        db.refresh(db_favorite)
    return db_favorite

# Delete a favorite by ID
def delete_favorite(db: Session, favorite_id: int):
    db_favorite = get_favorite_by_id(db, favorite_id)
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return db_favorite
