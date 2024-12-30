from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.set_entry import (
    get_set_entries,
    get_set_entry_by_id,
    create_set_entry,
    update_set_entry,
    delete_set_entry
)
from src.schemas.set_entry import SetEntry, SetEntryCreate

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read all set entries
@router.get("/", response_model=list[SetEntry])
def read_set_entries(db: Session = Depends(get_db)):
    set_entries = get_set_entries(db)
    if not set_entries:
        raise HTTPException(status_code=404, detail="No set entries found")
    return set_entries

# Read a set entry by ID
@router.get("/{set_entry_id}", response_model=SetEntry)
def read_set_entry_by_id(set_entry_id: int, db: Session = Depends(get_db)):
    db_set_entry = get_set_entry_by_id(db, set_entry_id)
    if not db_set_entry:
        raise HTTPException(status_code=404, detail="Set entry not found")
    return db_set_entry

# Create a new set entry
@router.post("/", response_model=SetEntry)
def create_new_set_entry(set_entry: SetEntryCreate, db: Session = Depends(get_db)):
    return create_set_entry(db, set_entry)

# Update a set entry by ID
@router.put("/{set_entry_id}", response_model=SetEntry)
def update_set_entry_by_id(set_entry_id: int, set_entry: SetEntryCreate, db: Session = Depends(get_db)):
    db_set_entry = update_set_entry(db, set_entry_id, set_entry)
    if not db_set_entry:
        raise HTTPException(status_code=404, detail="Set entry not found")
    return db_set_entry

# Delete a set entry by ID
@router.delete("/{set_entry_id}", response_model=SetEntry)
def delete_set_entry_by_id(set_entry_id: int, db: Session = Depends(get_db)):
    db_set_entry = delete_set_entry(db, set_entry_id)
    if not db_set_entry:
        raise HTTPException(status_code=404, detail="Set entry not found")
    return db_set_entry
