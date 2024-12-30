from sqlalchemy import Column, Integer, String
from src.database import Base
from sqlalchemy.orm import relationship

class Restaurant(Base):
    __tablename__ = "restaurants"

    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_name = Column(String(100), nullable=False)
    restaurant_cuisine = Column(String(100), nullable=True)
    restaurant_website = Column(String(255), nullable=True)

    # New Relationships
    favorites = relationship("Favorite", back_populates="restaurant", cascade="all, delete-orphan")
    set_entries = relationship("SetEntry", back_populates="restaurant", cascade="all, delete-orphan")