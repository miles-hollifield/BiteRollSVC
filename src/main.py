import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import users, restaurants, sets, favorites, set_entries, yelp

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="BiteRoll API",
    description="API for managing users, restaurants, sets, and integrating Yelp",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(sets.router, prefix="/sets", tags=["Sets"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(set_entries.router, prefix="/set-entries", tags=["Set Entries"])
app.include_router(yelp.router, prefix="/yelp", tags=["Yelp API"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the BiteRoll Backend!"}
