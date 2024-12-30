from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.favorite import (
    get_favorites,
    get_favorite_by_id,
    create_favorite,
    update_favorite,
    delete_favorite
)
from src.schemas.favorite import Favorite, FavoriteCreate

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read all favorites
@router.get("/", response_model=list[Favorite])
def read_favorites(db: Session = Depends(get_db)):
    favorites = get_favorites(db)
    if not favorites:
        raise HTTPException(status_code=404, detail="No favorites found")
    return favorites

# Read a favorite by ID
@router.get("/{favorite_id}", response_model=Favorite)
def read_favorite_by_id(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = get_favorite_by_id(db, favorite_id)
    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return db_favorite

# Create a new favorite
@router.post("/", response_model=Favorite)
def create_new_favorite(favorite: FavoriteCreate, db: Session = Depends(get_db)):
    return create_favorite(db, favorite)

# Update a favorite by ID
@router.put("/{favorite_id}", response_model=Favorite)
def update_favorite_by_id(favorite_id: int, favorite: FavoriteCreate, db: Session = Depends(get_db)):
    db_favorite = update_favorite(db, favorite_id, favorite)
    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return db_favorite

# Delete a favorite by ID
@router.delete("/{favorite_id}", response_model=Favorite)
def delete_favorite_by_id(favorite_id: int, db: Session = Depends(get_db)):
    db_favorite = delete_favorite(db, favorite_id)
    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return db_favorite
