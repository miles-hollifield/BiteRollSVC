from pydantic import BaseModel
from typing import Optional

class RestaurantBase(BaseModel):
    """Base schema shared by all restaurant schemas."""
    restaurant_name: str
    restaurant_cuisine: Optional[str] = None
    restaurant_website: Optional[str] = None

class RestaurantCreate(RestaurantBase):
    """Schema for creating or updating a restaurant."""
    pass

class Restaurant(RestaurantBase):
    """Schema for returning restaurant data."""
    restaurant_id: int

    class Config:
        from_attributes = True  # Enable ORM compatibility
