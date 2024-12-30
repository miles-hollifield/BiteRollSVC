from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    """Base schema shared by all user schemas."""
    firstname: str
    lastname: str
    username: str
    email: str
    avatar: Optional[str] = None

class UserCreate(UserBase):
    """Schema for creating or updating a user."""
    password: str

class User(UserBase):
    """Schema for returning user data."""
    user_id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility
