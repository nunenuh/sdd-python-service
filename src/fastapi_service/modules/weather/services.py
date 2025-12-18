"""
Weather service for fetching weather data from Open-Meteo API.

This module contains the core business logic for weather data retrieval,
separated from HTTP handling concerns.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import httpx

from fastapi_service.core.config import get_settings
from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException

from .schemas import CurrentWeather, DailyForecast, HourlyForecast

logger = get_logger(__name__)


class WeatherService:
    """Service for fetching weather data from Open-Meteo API."""

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self):
        """Initialize weather service."""
        self.settings = get_settings()
        self.timeout = 10.0

    def _get_weather_code_description(self, code: int) -> str:
        """Convert weather code to human-readable description."""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return weather_codes.get(code, "Unknown")

    async def get_current_weather(
        self, latitude: float, longitude: float, timezone: str = "auto"
    ) -> Tuple[CurrentWeather, str, str, float, float]:
        """Get current weather conditions for a location.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            timezone: Timezone (default: "auto")

        Returns:
            Tuple of (CurrentWeather, location_name, timezone, latitude, longitude)

        Raises:
            ServiceException: If weather data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "wind_speed_10m",
                        "wind_direction_10m",
                        "weather_code",
                        "surface_pressure",
                        "visibility",
                    ],
                    "timezone": timezone,
                }

                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()

                current = data.get("current", {})
                location_name = f"{latitude},{longitude}"
                timezone_str = data.get("timezone", timezone)

                current_weather = CurrentWeather(
                    temperature=current.get("temperature_2m", 0.0),
                    humidity=current.get("relative_humidity_2m", 0),
                    wind_speed=current.get("wind_speed_10m", 0.0),
                    wind_direction=current.get("wind_direction_10m", 0),
                    weather_code=current.get("weather_code", 0),
                    weather_description=self._get_weather_code_description(
                        current.get("weather_code", 0)
                    ),
                    pressure=current.get("surface_pressure"),
                    visibility=current.get("visibility"),
                )

                return (
                    current_weather,
                    location_name,
                    timezone_str,
                    float(latitude),
                    float(longitude),
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching weather data: {str(e)}")
            raise ServiceException(f"Failed to fetch weather data: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching weather data: {str(e)}")
            raise ServiceException(f"Network error fetching weather data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching weather data: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def get_weather_with_forecast(
        self,
        latitude: float,
        longitude: float,
        timezone: str = "auto",
        hourly: bool = True,
        daily: bool = True,
    ) -> Tuple[
        CurrentWeather,
        Optional[List[HourlyForecast]],
        Optional[List[DailyForecast]],
        str,
        str,
        float,
        float,
    ]:
        """Get current weather with hourly and daily forecasts.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            timezone: Timezone (default: "auto")
            hourly: Include hourly forecast
            daily: Include daily forecast

        Returns:
            Tuple of (CurrentWeather, hourly_forecast, daily_forecast, location_name, timezone, latitude, longitude)

        Raises:
            ServiceException: If weather data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "wind_speed_10m",
                        "wind_direction_10m",
                        "weather_code",
                        "surface_pressure",
                        "visibility",
                    ],
                    "timezone": timezone,
                }

                if hourly:
                    params.update(
                        {
                            "hourly": [
                                "temperature_2m",
                                "relative_humidity_2m",
                                "wind_speed_10m",
                                "wind_direction_10m",
                                "weather_code",
                                "precipitation_probability",
                            ],
                            "forecast_hours": 48,
                        }
                    )

                if daily:
                    params.update(
                        {
                            "daily": [
                                "temperature_2m_max",
                                "temperature_2m_min",
                                "weather_code",
                                "precipitation_sum",
                                "wind_speed_10m_max",
                            ],
                            "forecast_days": 7,
                        }
                    )

                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()

                current = data.get("current", {})
                location_name = f"{latitude},{longitude}"
                timezone_str = data.get("timezone", timezone)

                current_weather = CurrentWeather(
                    temperature=current.get("temperature_2m", 0.0),
                    humidity=current.get("relative_humidity_2m", 0),
                    wind_speed=current.get("wind_speed_10m", 0.0),
                    wind_direction=current.get("wind_direction_10m", 0),
                    weather_code=current.get("weather_code", 0),
                    weather_description=self._get_weather_code_description(
                        current.get("weather_code", 0)
                    ),
                    pressure=current.get("surface_pressure"),
                    visibility=current.get("visibility"),
                )

                hourly_forecast = None
                if hourly and "hourly" in data:
                    hourly_data = data["hourly"]
                    times = hourly_data.get("time", [])
                    hourly_forecast = []
                    for i, time_str in enumerate(times[:48]):  # Limit to 48 hours
                        hourly_forecast.append(
                            HourlyForecast(
                                time=datetime.fromisoformat(
                                    time_str.replace("Z", "+00:00")
                                ),
                                temperature=hourly_data.get("temperature_2m", [0.0])[i],
                                humidity=hourly_data.get("relative_humidity_2m", [0])[
                                    i
                                ],
                                wind_speed=hourly_data.get("wind_speed_10m", [0.0])[i],
                                wind_direction=hourly_data.get(
                                    "wind_direction_10m", [0]
                                )[i],
                                weather_code=hourly_data.get("weather_code", [0])[i],
                                weather_description=self._get_weather_code_description(
                                    hourly_data.get("weather_code", [0])[i]
                                ),
                                precipitation_probability=hourly_data.get(
                                    "precipitation_probability", [None]
                                )[i],
                            )
                        )

                daily_forecast = None
                if daily and "daily" in data:
                    daily_data = data["daily"]
                    dates = daily_data.get("time", [])
                    daily_forecast = []
                    for i, date_str in enumerate(dates[:7]):  # Limit to 7 days
                        daily_forecast.append(
                            DailyForecast(
                                date=datetime.fromisoformat(date_str),
                                temperature_max=daily_data.get(
                                    "temperature_2m_max", [0.0]
                                )[i],
                                temperature_min=daily_data.get(
                                    "temperature_2m_min", [0.0]
                                )[i],
                                weather_code=daily_data.get("weather_code", [0])[i],
                                weather_description=self._get_weather_code_description(
                                    daily_data.get("weather_code", [0])[i]
                                ),
                                precipitation_sum=daily_data.get(
                                    "precipitation_sum", [None]
                                )[i],
                                wind_speed_max=daily_data.get(
                                    "wind_speed_10m_max", [None]
                                )[i],
                            )
                        )

                return (
                    current_weather,
                    hourly_forecast,
                    daily_forecast,
                    location_name,
                    timezone_str,
                    float(latitude),
                    float(longitude),
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching weather data: {str(e)}")
            raise ServiceException(f"Failed to fetch weather data: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching weather data: {str(e)}")
            raise ServiceException(f"Network error fetching weather data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching weather data: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")


# Singleton instance
_weather_service = None


def get_weather_service() -> WeatherService:
    """Get weather service singleton instance."""
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService()
    return _weather_service
