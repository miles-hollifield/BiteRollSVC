from sqlalchemy.orm import Session
from src.models.set import Set
from src.schemas.set import SetCreate

# Retrieve all sets
def get_sets(db: Session):
    return db.query(Set).all()

# Retrieve a set by ID
def get_set_by_id(db: Session, set_id: int):
    return db.query(Set).filter(Set.set_id == set_id).first()

# Create a new set
def create_set(db: Session, set_data: SetCreate):
    db_set = Set(
        set_name=set_data.set_name,
        user_id=set_data.user_id
    )
    db.add(db_set)
    db.commit()
    db.refresh(db_set)
    return db_set

# Update a set by ID
def update_set(db: Session, set_id: int, set_data: SetCreate):
    db_set = get_set_by_id(db, set_id)
    if db_set:
        db_set.set_name = set_data.set_name
        db_set.user_id = set_data.user_id
        db.commit()
        db.refresh(db_set)
    return db_set

# Delete a set by ID
def delete_set(db: Session, set_id: int):
    db_set = get_set_by_id(db, set_id)
    if db_set:
        db.delete(db_set)
        db.commit()
    return db_set
