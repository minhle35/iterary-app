"""
Trip planner API endpoint.
Combines trip parsing with POI suggestions.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.trip_parser import TripParserRequest, TripPlanResponse, Activity
from app.services.trip_parser_simple import get_simple_trip_parser
from app.services.poi_service import get_poi_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/trip-planner", tags=["trip-planner"])


@router.post("/plan", response_model=TripPlanResponse)
async def plan_trip(request: TripParserRequest):
    """
    Parse trip query and suggest activities.

    Example queries:
    - "3 days in Melbourne"
    - "going to Sydney for 5 days"
    - "weekend trip to Tokyo"
    """
    try:
        # Parse the query
        parser = get_simple_trip_parser()
        parsed = parser.parse(request.query)

        city = parsed.get("city", "")
        duration_days = parsed.get("duration_days")

        if not city:
            raise HTTPException(
                status_code=400,
                detail="Could not extract city from query. Please specify a city name."
            )

        # Get activities from POI APIs
        poi_service = get_poi_service()

        # Use duration to determine how many activities to suggest
        # Default to 5 activities if duration not specified
        limit = (duration_days * 2) if duration_days else 10

        activities = poi_service.get_activities_multi_provider(
            city=city,
            duration_days=duration_days or 3,
            limit=limit
        )

        # Convert to response format
        activity_list = [
            Activity(**activity) for activity in activities
        ]

        return TripPlanResponse(
            city=city,
            duration_days=duration_days,
            activities=activity_list
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error planning trip: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to plan trip: {str(e)}"
        ) from e


@router.get("/activities/{city}")
async def get_city_activities(
    city: str,
    duration_days: int = 3,
    limit: int = 10,
    provider: str = "yelp"
):
    """
    Get activities for a specific city.

    Args:
        city: City name
        duration_days: Number of days for the trip
        limit: Maximum number of activities
        provider: POI API provider (yelp, foursquare, tripadvisor, amadeus)
    """
    try:
        poi_service = get_poi_service()
        activities = poi_service.get_activities(
            city=city,
            duration_days=duration_days,
            limit=limit,
            provider=provider
        )

        return {
            "city": city,
            "duration_days": duration_days,
            "activities": activities
        }

    except Exception as e:
        logger.error("Error fetching activities: %s", e, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch activities: {str(e)}"
        ) from e

