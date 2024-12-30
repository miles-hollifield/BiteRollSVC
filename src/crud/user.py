from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate

# Retrieve all users
def get_users(db: Session):
    return db.query(User).all()

# Retrieve a user by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

# Create a new user
def create_user(db: Session, user: UserCreate):
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

# Update an existing user by ID
def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db_user.firstname = user.firstname
        db_user.lastname = user.lastname
        db_user.username = user.username
        db_user.email = user.email
        db_user.avatar = user.avatar
        db_user.password = user.password  # In production, hash the password!
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete a user by ID
def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
