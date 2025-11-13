"""
Pydantic schemas for trip parser and planner API.
These schemas define the API contract between frontend and backend.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class TripParserRequest(BaseModel):
    """Request schema for trip parsing - FROM frontend."""
    query: str = Field(..., description="Natural language trip query", example="3 days in Melbourne")


class Activity(BaseModel):
    """Activity/POI schema - TO frontend."""
    name: str
    category: Optional[str] = None
    rating: Optional[float] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    price: Optional[str] = None


class TripPlanResponse(BaseModel):
    """Response schema for trip planning - TO frontend."""
    city: str
    duration_days: Optional[int] = None
    activities: List[Activity] = []
