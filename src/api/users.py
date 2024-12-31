from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.crud.user import (
    get_users,
    get_user_by_id,
    get_user_by_username,
    create_user,
    update_user,
    delete_user,
)
from src.schemas.user import User, UserCreate, UserRegister, UserLogin, UserResponse
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
    salt = bcrypt.gensalt().decode()  # Generate a unique salt
    user.password = hash_password(user.password, salt)  # Hash the password with the salt
    return create_user(db, user, salt)

# Update an existing user by ID
@router.put("/{user_id}", response_model=User)
def update_user_by_id(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    salt = bcrypt.gensalt().decode()  # Generate a new salt
    user.password = hash_password(user.password, salt)  # Hash the updated password
    db_user = update_user(db, user_id, user, salt)
    return db_user

# Delete a user by ID
@router.delete("/{user_id}", response_model=User)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Register a new user
@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    salt = bcrypt.gensalt().decode()  # Generate a unique salt
    hashed_password = hash_password(user.password, salt)  # Hash the password with the salt
    db_user = create_user(
        db,
        UserRegister(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            password=hashed_password,
        ),
        salt,
    )
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
    if not db_user or not verify_password(user_login.password, db_user.password, db_user.salt):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=30),
    )
    return {"access_token": token, "token_type": "bearer"}
