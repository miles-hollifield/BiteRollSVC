from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.set import (
    get_sets,
    get_set_by_id,
    create_set,
    update_set,
    delete_set
)
from src.schemas.set import Set, SetCreate

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read all sets
@router.get("/", response_model=list[Set])
def read_sets(db: Session = Depends(get_db)):
    sets = get_sets(db)
    if not sets:
        raise HTTPException(status_code=404, detail="No sets found")
    return sets

# Read a set by ID
@router.get("/{set_id}", response_model=Set)
def read_set_by_id(set_id: int, db: Session = Depends(get_db)):
    db_set = get_set_by_id(db, set_id)
    if not db_set:
        raise HTTPException(status_code=404, detail="Set not found")
    return db_set

# Create a new set
@router.post("/", response_model=Set)
def create_new_set(set_data: SetCreate, db: Session = Depends(get_db)):
    return create_set(db, set_data)

# Update a set by ID
@router.put("/{set_id}", response_model=Set)
def update_set_by_id(set_id: int, set_data: SetCreate, db: Session = Depends(get_db)):
    db_set = update_set(db, set_id, set_data)
    if not db_set:
        raise HTTPException(status_code=404, detail="Set not found")
    return db_set

# Delete a set by ID
@router.delete("/{set_id}", response_model=Set)
def delete_set_by_id(set_id: int, db: Session = Depends(get_db)):
    db_set = delete_set(db, set_id)
    if not db_set:
        raise HTTPException(status_code=404, detail="Set not found")
    return db_set
