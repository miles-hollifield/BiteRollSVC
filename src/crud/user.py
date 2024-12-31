from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserRegister, UserCreate

def get_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserRegister):
    """Create a new user without handling a separate salt."""
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        password=user.password,  # This should already be a hashed password
        is_active=True,
        is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserCreate):
    """Update an existing user's details."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.firstname = user.firstname
        db_user.lastname = user.lastname
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password  # This should already be a hashed password
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user by ID."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
