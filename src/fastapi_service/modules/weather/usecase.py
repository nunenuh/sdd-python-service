"""
Weather use case orchestration layer.
"""

from typing import List, Optional, Tuple

from .schemas import CurrentWeather, DailyForecast, HourlyForecast
from .services import WeatherService, get_weather_service


class WeatherUseCase:
    """Use case for orchestrating weather operations."""

    def __init__(self):
        """Initialize weather use case."""
        self.service = get_weather_service()

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
        """
        return await self.service.get_current_weather(latitude, longitude, timezone)

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
        """
        return await self.service.get_weather_with_forecast(
            latitude, longitude, timezone, hourly, daily
        )

