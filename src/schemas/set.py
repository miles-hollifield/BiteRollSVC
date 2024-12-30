from pydantic import BaseModel

class SetBase(BaseModel):
    """Base schema shared by all set schemas."""
    set_name: str
    user_id: int

class SetCreate(SetBase):
    """Schema for creating or updating a set."""
    pass

class Set(SetBase):
    """Schema for returning set data."""
    set_id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility
