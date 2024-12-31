from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
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
from src.utils.auth import verify_password, create_access_token, hash_password, decode_access_token
from datetime import timedelta

# Initialize router
router = APIRouter()

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get current user
@router.get("/me", response_model=UserResponse)
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        user_id=user.user_id,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
    )

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

    hashed_password = hash_password(user.password)  # Hash password directly
    db_user = create_user(
        db,
        UserRegister(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            password=hashed_password,
        )
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
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_login.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

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

    hashed_password = hash_password(user.password)  # Hash updated password directly
    user.password = hashed_password
    updated_user = update_user(db, user_id, user)
    return updated_user

# Delete a user
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
