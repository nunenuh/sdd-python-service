"""
Weather API endpoints for the FastAPI service.

This module provides HTTP endpoints for weather data retrieval. All business logic
is delegated to the weather service layer, keeping this module focused purely
on HTTP request/response handling.
"""

from datetime import UTC, datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import Field

from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException

from ..schemas import WeatherErrorResponse, WeatherResponse
from ..usecase import WeatherUseCase

logger = get_logger(__name__)
router = APIRouter()


@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(
    latitude: float = Query(
        ..., description="Latitude coordinate", ge=-90, le=90, example=52.52
    ),
    longitude: float = Query(
        ..., description="Longitude coordinate", ge=-180, le=180, example=13.41
    ),
    timezone: str = Query(
        default="auto",
        description="Timezone (e.g., 'Europe/Berlin' or 'auto' for automatic)",
        example="auto",
    ),
):
    """
    Get current weather conditions for a location.

    This endpoint provides current weather data including temperature, humidity,
    wind speed, and weather conditions for the specified coordinates.
    """
    usecase = WeatherUseCase()

    try:
        current, location_name, timezone_str, lat, lon = (
            await usecase.get_current_weather(latitude, longitude, timezone)
        )

        return WeatherResponse(
            location=location_name,
            latitude=float(lat),
            longitude=float(lon),
            timezone=timezone_str,
            current=current,
            hourly=None,
            daily=None,
            timestamp=datetime.now(UTC),
        )

    except ServiceException as e:
        logger.error(f"Weather service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "weather_service_error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )


@router.get("/forecast", response_model=WeatherResponse)
async def get_weather_forecast(
    latitude: float = Query(
        ..., description="Latitude coordinate", ge=-90, le=90, example=52.52
    ),
    longitude: float = Query(
        ..., description="Longitude coordinate", ge=-180, le=180, example=13.41
    ),
    timezone: str = Query(
        default="auto",
        description="Timezone (e.g., 'Europe/Berlin' or 'auto' for automatic)",
        example="auto",
    ),
    hourly: bool = Query(
        default=True, description="Include hourly forecast (next 48 hours)"
    ),
    daily: bool = Query(
        default=True, description="Include daily forecast (next 7 days)"
    ),
):
    """
    Get current weather with hourly and daily forecasts.

    This endpoint provides comprehensive weather data including current conditions,
    hourly forecast for the next 48 hours, and daily forecast for the next 7 days.
    """
    usecase = WeatherUseCase()

    try:
        (
            current,
            hourly_forecast,
            daily_forecast,
            location_name,
            timezone_str,
            lat,
            lon,
        ) = await usecase.get_weather_with_forecast(
            latitude, longitude, timezone, hourly, daily
        )

        return WeatherResponse(
            location=location_name,
            latitude=float(lat),
            longitude=float(lon),
            timezone=timezone_str,
            current=current,
            hourly=hourly_forecast,
            daily=daily_forecast,
            timestamp=datetime.now(UTC),
        )

    except ServiceException as e:
        logger.error(f"Weather service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "weather_service_error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
