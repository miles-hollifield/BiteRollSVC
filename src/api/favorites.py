from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.favorite import (
    get_favorites,
    get_favorite_by_id,
    create_favorite,
    delete_favorite
)
from src.schemas.favorite import Favorite, FavoriteCreate
from src.api.users import get_current_user  # Reuse get_current_user from users.py

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all favorites for the logged-in user
@router.get("/", response_model=list[Favorite])
def read_favorites(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    favorites = get_favorites(db, current_user.user_id)
    if not favorites:
        raise HTTPException(status_code=404, detail="No favorites found for the user")
    return favorites

# Create a new favorite for the logged-in user
@router.post("/", response_model=Favorite)
def create_new_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    print("Raw payload received:", favorite)  # Raw favorite object
    print(f"Current user ID: {current_user.user_id}")  # Debug user ID

    # Ensure the restaurant_id is present
    if not favorite.restaurant_id:
        raise HTTPException(status_code=422, detail="Invalid restaurant_id")

    return create_favorite(db, favorite, current_user.user_id)


# Delete a favorite by ID
@router.delete("/{favorite_id}", response_model=Favorite)
def delete_favorite_by_id(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_favorite = get_favorite_by_id(db, favorite_id)
    # Check if the favorite exists and belongs to the current user
    if not db_favorite or db_favorite.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return delete_favorite(db, favorite_id)
