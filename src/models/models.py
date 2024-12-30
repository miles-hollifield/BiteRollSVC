from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    avatar = Column(Text, nullable=True)
    salt = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

class Restaurant(Base):
    __tablename__ = "restaurants"
    restaurant_id = Column(Integer, primary_key=True, autoincrement=True)
    restaurant_name = Column(String(100), nullable=False)
    restaurant_cuisine = Column(String(100), nullable=True)
    restaurant_website = Column(String(255), nullable=True)

class Set(Base):
    __tablename__ = "sets"
    set_id = Column(Integer, primary_key=True, autoincrement=True)
    set_name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user = relationship("User")

class Favorite(Base):
    __tablename__ = "favorites"
    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    user = relationship("User")
    restaurant = relationship("Restaurant")

class SetEntry(Base):
    __tablename__ = "set_entries"
    set_entry_id = Column(Integer, primary_key=True, autoincrement=True)
    set_id = Column(Integer, ForeignKey("sets.set_id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.restaurant_id"), nullable=False)
    set = relationship("Set")
    restaurant = relationship("Restaurant")
