from fastapi import APIRouter
from .yelp import router as yelp_router

# Initialize the main router
router = APIRouter()

# Include the Yelp router
router.include_router(yelp_router, prefix="/yelp", tags=["Yelp API"])
