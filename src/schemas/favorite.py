from pydantic import BaseModel

class FavoriteBase(BaseModel):
    """Base schema shared by all favorite schemas."""
    restaurant_id: int

class FavoriteCreate(FavoriteBase):
    """Schema for creating a favorite."""
    pass

class Favorite(FavoriteBase):
    """Schema for returning favorite data."""
    favorite_id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility
