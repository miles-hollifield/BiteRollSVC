from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate

def get_users(db: Session):
    """Retrieve all users from the database."""
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a single user by ID."""
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Retrieve a user by their username."""
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        avatar=user.avatar,
        password=user.password,  # In production, hash the password!
    )
    db.add(db_user)
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
