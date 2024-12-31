from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.user import User  # Correct SQLAlchemy model
from src.crud.user import (
    get_users,
    get_user_by_id,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
)
from src.schemas.user import UserCreate, UserRegister, UserLogin, UserResponse
from src.utils.auth import verify_password, create_access_token, hash_password
from datetime import timedelta
import bcrypt

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
@router.get("/", response_model=list[UserResponse])
def read_users(db: Session = Depends(get_db)):
    users = get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Read user by ID
@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Register a new user
@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    salt = bcrypt.gensalt().decode()  # Generate a unique salt
    hashed_password = hash_password(user.password, salt)  # Hash password
    db_user = create_user(db, user, salt)
    return UserResponse(
        user_id=db_user.user_id,
        firstname=db_user.firstname,
        lastname=db_user.lastname,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_verified=db_user.is_verified,
    )

# Login a user
@router.post("/login")
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user_login.username)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify the password using the stored salt
    if not verify_password(user_login.password, db_user.password, db_user.salt):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token
    token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=30),
    )
    return {"access_token": token, "token_type": "bearer"}

# Update an existing user
@router.put("/{user_id}", response_model=UserResponse)
def update_user_by_id(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    salt = bcrypt.gensalt().decode()  # Generate a new salt
    hashed_password = hash_password(user.password, salt)  # Hash password
    user.password = hashed_password
    updated_user = update_user(db, user_id, user, salt)
    return updated_user

# Delete a user
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
