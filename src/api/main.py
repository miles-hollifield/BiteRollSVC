from fastapi import FastAPI
from src.api import users, restaurants

# Initialize FastAPI app
app = FastAPI(
    title="BiteRoll API",
    description="API for managing users and restaurants in BiteRoll",
    version="1.0.0"
)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the BiteRoll Backend!"}
