from pydantic import BaseModel

class SetEntryBase(BaseModel):
    """Base schema shared by all set entry schemas."""
    set_id: int
    restaurant_id: int

class SetEntryCreate(SetEntryBase):
    """Schema for creating or updating a set entry."""
    pass

class SetEntry(SetEntryBase):
    """Schema for returning set entry data."""
    set_entry_id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility
