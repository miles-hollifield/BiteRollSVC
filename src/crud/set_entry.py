from sqlalchemy.orm import Session
from src.models.set_entry import SetEntry
from src.schemas.set_entry import SetEntryCreate

# Retrieve all set entries
def get_set_entries(db: Session):
    return db.query(SetEntry).all()

# Retrieve a set entry by ID
def get_set_entry_by_id(db: Session, set_entry_id: int):
    return db.query(SetEntry).filter(SetEntry.set_entry_id == set_entry_id).first()

# Create a new set entry
def create_set_entry(db: Session, set_entry_data: SetEntryCreate):
    db_set_entry = SetEntry(
        set_id=set_entry_data.set_id,
        restaurant_id=set_entry_data.restaurant_id,
    )
    db.add(db_set_entry)
    db.commit()
    db.refresh(db_set_entry)
    return db_set_entry

# Update a set entry by ID
def update_set_entry(db: Session, set_entry_id: int, set_entry_data: SetEntryCreate):
    db_set_entry = get_set_entry_by_id(db, set_entry_id)
    if db_set_entry:
        db_set_entry.set_id = set_entry_data.set_id
        db_set_entry.restaurant_id = set_entry_data.restaurant_id
        db.commit()
        db.refresh(db_set_entry)
    return db_set_entry

# Delete a set entry by ID
def delete_set_entry(db: Session, set_entry_id: int):
    db_set_entry = get_set_entry_by_id(db, set_entry_id)
    if db_set_entry:
        db.delete(db_set_entry)
        db.commit()
    return db_set_entry
