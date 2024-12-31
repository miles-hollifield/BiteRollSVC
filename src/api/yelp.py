from fastapi import APIRouter, HTTPException, Query
import requests
import os

router = APIRouter()

# Yelp API constants
YELP_API_BASE_URL = "https://api.yelp.com/v3/businesses/search"
CATEGORIES = ["restaurants", "food"]
RADIUS_METERS = 10000
RETURN_LIMIT = 50
SORT_BY = "best_match"


# Yelp API key from environment variables
YELP_API_KEY = os.getenv("YELP_API_KEY")


@router.get("/restaurants/search")
def search_restaurants(
    name: str = Query(..., description="Search term for the restaurant name"),
    lat: float = Query(None, description="Latitude of the user's location (optional)"),
    lon: float = Query(None, description="Longitude of the user's location (optional)"),
):
    """
    Search for restaurants by name and optionally by user location.
    If latitude and longitude are not provided, a default location is used.
    """
    if not YELP_API_KEY:
        raise HTTPException(status_code=500, detail="Yelp API Key is not configured")

    # Build request parameters
    params = {
        "term": name,
        "categories": ",".join(CATEGORIES),
        "radius": RADIUS_METERS,
        "sort_by": SORT_BY,
        "limit": RETURN_LIMIT,
    }

    # Use user-provided location if available, otherwise use a default location
    if lat and lon:
        params.update({"latitude": lat, "longitude": lon})
    else:
        # Default location (e.g., Raleigh, NC)
        params.update({"location": "Raleigh"})

    headers = {
        "Authorization": f"Bearer {YELP_API_KEY}"
    }

    try:
        response = requests.get(YELP_API_BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse the Yelp response
        businesses = [
            {
                "name": business.get("name"),
                "address": business["location"].get("address1"),
                "phone": business.get("display_phone"),
                "categories": [category["title"] for category in business.get("categories", [])],
                "image_url": business.get("image_url"),
                "yelp_url": business.get("url"),
            }
            for business in data.get("businesses", [])
        ]

        return {"results": businesses}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Yelp API request failed: {str(e)}")
