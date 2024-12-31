from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    username: str
    email: str
    is_active: bool
    is_verified: bool

class User(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: EmailStr
    password: str