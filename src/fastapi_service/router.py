"""
Main API router that aggregates all service endpoints.
"""

from fastapi import APIRouter

from .modules.health.apiv1.handler import router as health_router
from .modules.quotes.apiv1.handler import router as quotes_router
from .modules.weather.apiv1.handler import router as weather_router

# Main API router
api_router = APIRouter()

# Include all module routers
api_router.include_router(health_router, prefix="/v1/health", tags=["Health"])
api_router.include_router(weather_router, prefix="/v1/weather", tags=["Weather"])
api_router.include_router(quotes_router, prefix="/v1/quotes", tags=["Quotes"])
