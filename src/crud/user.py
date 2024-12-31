from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate, UserRegister

# Retrieve all users
def get_users(db: Session):
    return db.query(User).all()

# Retrieve a user by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

# Retrieve a user by username
def get_user_by_username(db: Session, username: str):
    """Fetch a user by username."""
    return db.query(User).filter(User.username == username).first()

# Create a new user
def create_user(db: Session, user: UserRegister, salt: str):
    """Register a new user with a hashed password and salt."""
    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        password=user.password,  # Already hashed
        salt=salt,  # Store the salt for the user
        is_active=True,
        is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update an existing user by ID
def update_user(db: Session, user_id: int, user: UserCreate, salt: str):
    """Update an existing user's details and rehash the password."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.firstname = user.firstname
        db_user.lastname = user.lastname
        db_user.username = user.username
        db_user.email = user.email
        db_user.avatar = user.avatar
        db_user.password = user.password  # Already hashed
        db_user.salt = salt  # Update the salt
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete a user by ID
def delete_user(db: Session, user_id: int):
    """Delete a user by ID."""
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
