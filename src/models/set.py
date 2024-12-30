from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Set(Base):
    __tablename__ = "sets"

    set_id = Column(Integer, primary_key=True, autoincrement=True)
    set_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="sets")
    set_entries = relationship("SetEntry", back_populates="set", cascade="all, delete-orphan")