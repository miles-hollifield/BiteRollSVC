from pydantic import BaseModel

class FavoriteBase(BaseModel):
    """Base schema shared by all favorite schemas."""
    user_id: int
    restaurant_id: int

class FavoriteCreate(FavoriteBase):
    """Schema for creating or updating a favorite."""
    pass

class Favorite(FavoriteBase):
    """Schema for returning favorite data."""
    favorite_id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility
