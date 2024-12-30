from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class SetEntry(Base):
    __tablename__ = "set_entries"

    set_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    set_id = Column(Integer, ForeignKey("sets.set_id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)

    # Relationships
    set = relationship("Set", back_populates="set_entries")
    restaurant = relationship("Restaurant", back_populates="set_entries")
