from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.user import (
    get_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)
from src.schemas.user import User, UserCreate

# Initialize router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read all users
@router.get("/", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Read user by ID
@router.get("/{user_id}", response_model=User)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Create a new user
@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

# Update an existing user by ID
@router.put("/{user_id}", response_model=User)
def update_user_by_id(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Delete a user by ID
@router.delete("/{user_id}", response_model=User)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
