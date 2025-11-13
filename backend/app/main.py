"""
Main file for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import trip_planner

app = FastAPI(
    title="Iterary App API",
    description="Collaborative Group Travel Planning Platform API",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(trip_planner.router)


@app.get("/")
async def root():
    """
    Root endpoint.
    """
    return {"message": "Iterary App API"}

@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
