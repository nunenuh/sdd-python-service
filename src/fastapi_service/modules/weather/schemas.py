"""
Weather response schemas for the FastAPI service.

This module defines Pydantic models for structuring weather API responses,
ensuring consistent API response formats.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CurrentWeather(BaseModel):
    """Current weather conditions."""

    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: int = Field(..., description="Relative humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    wind_direction: int = Field(..., description="Wind direction in degrees")
    weather_code: int = Field(..., description="Weather condition code")
    weather_description: str = Field(
        ..., description="Human-readable weather description"
    )
    pressure: Optional[float] = Field(None, description="Atmospheric pressure in hPa")
    visibility: Optional[float] = Field(None, description="Visibility in km")


class HourlyForecast(BaseModel):
    """Hourly weather forecast."""

    time: datetime = Field(..., description="Forecast time")
    temperature: float = Field(..., description="Temperature in Celsius")
    humidity: int = Field(..., description="Relative humidity percentage")
    wind_speed: float = Field(..., description="Wind speed in km/h")
    wind_direction: int = Field(..., description="Wind direction in degrees")
    weather_code: int = Field(..., description="Weather condition code")
    weather_description: str = Field(
        ..., description="Human-readable weather description"
    )
    precipitation_probability: Optional[int] = Field(
        None, description="Precipitation probability percentage"
    )


class DailyForecast(BaseModel):
    """Daily weather forecast."""

    date: datetime = Field(..., description="Forecast date")
    temperature_max: float = Field(..., description="Maximum temperature in Celsius")
    temperature_min: float = Field(..., description="Minimum temperature in Celsius")
    weather_code: int = Field(..., description="Weather condition code")
    weather_description: str = Field(
        ..., description="Human-readable weather description"
    )
    precipitation_sum: Optional[float] = Field(
        None, description="Total precipitation in mm"
    )
    wind_speed_max: Optional[float] = Field(
        None, description="Maximum wind speed in km/h"
    )


class WeatherResponse(BaseModel):
    """Weather response with current conditions and forecasts."""

    location: str = Field(..., description="Location name or coordinates")
    latitude: float = Field(..., description="Latitude")
    longitude: float = Field(..., description="Longitude")
    timezone: str = Field(..., description="Timezone")
    current: CurrentWeather = Field(..., description="Current weather conditions")
    hourly: Optional[List[HourlyForecast]] = Field(
        None, description="Hourly forecast (next 24-48 hours)"
    )
    daily: Optional[List[DailyForecast]] = Field(
        None, description="Daily forecast (next 7 days)"
    )
    timestamp: datetime = Field(..., description="Response timestamp")


class WeatherErrorResponse(BaseModel):
    """Error response for weather API."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: datetime = Field(..., description="Error timestamp")
