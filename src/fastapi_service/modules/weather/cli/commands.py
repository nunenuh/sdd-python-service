"""
Weather CLI commands.

This module provides command-line interface commands for weather-related operations.
Commands are organized here to keep them close to the weather module while maintaining
separation from the REST API handlers.
"""

import asyncio

import typer
from rich.console import Console
from rich.table import Table

from fastapi_service.core.logging import setup_logging
from fastapi_service.modules.weather.usecase import WeatherUseCase

# Initialize console for rich output
console = Console()

# Create weather subcommand group
weather_app = typer.Typer(help="Weather-related commands")


@weather_app.command("current")
def weather_current(
    latitude: float = typer.Argument(..., help="Latitude coordinate (-90 to 90)"),
    longitude: float = typer.Argument(..., help="Longitude coordinate (-180 to 180)"),
    timezone: str = typer.Option("auto", "--tz", help="Timezone (default: auto)"),
):
    """Get current weather conditions for a location."""
    setup_logging()
    console.print(f"[bold]Fetching weather for {latitude}, {longitude}...[/bold]")

    async def fetch_weather():
        usecase = WeatherUseCase()
        current, location_name, tz, lat, lon = await usecase.get_current_weather(
            latitude, longitude, timezone
        )

        # Create a rich table for output
        table = Table(
            title=f"Weather for {location_name}",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Location", f"{lat}, {lon}")
        table.add_row("Timezone", tz)
        table.add_row("Temperature", f"{current.temperature}°C")
        table.add_row("Humidity", f"{current.humidity}%")
        table.add_row("Wind Speed", f"{current.wind_speed} km/h")
        table.add_row("Wind Direction", f"{current.wind_direction}°")
        table.add_row("Weather", current.weather_description)
        if current.pressure:
            table.add_row("Pressure", f"{current.pressure} hPa")
        if current.visibility:
            table.add_row("Visibility", f"{current.visibility} km")

        console.print(table)

    asyncio.run(fetch_weather())


@weather_app.command("forecast")
def weather_forecast(
    latitude: float = typer.Argument(..., help="Latitude coordinate (-90 to 90)"),
    longitude: float = typer.Argument(..., help="Longitude coordinate (-180 to 180)"),
    timezone: str = typer.Option("auto", "--tz", help="Timezone (default: auto)"),
    no_hourly: bool = typer.Option(
        False, "--no-hourly", help="Exclude hourly forecast"
    ),
    no_daily: bool = typer.Option(
        False, "--no-daily", help="Exclude daily forecast"
    ),
):
    """Get weather forecast with current conditions."""
    setup_logging()
    console.print(
        f"[bold]Fetching weather forecast for {latitude}, {longitude}...[/bold]"
    )

    async def fetch_forecast():
        usecase = WeatherUseCase()
        (
            current,
            hourly_forecast,
            daily_forecast,
            location_name,
            tz,
            lat,
            lon,
        ) = await usecase.get_weather_with_forecast(
            latitude, longitude, timezone, not no_hourly, not no_daily
        )

        # Current weather table
        current_table = Table(
            title=f"Current Weather - {location_name}",
            show_header=True,
            header_style="bold magenta",
        )
        current_table.add_column("Property", style="cyan")
        current_table.add_column("Value", style="green")

        current_table.add_row("Temperature", f"{current.temperature}°C")
        current_table.add_row("Humidity", f"{current.humidity}%")
        current_table.add_row(
            "Wind", f"{current.wind_speed} km/h @ {current.wind_direction}°"
        )
        current_table.add_row("Weather", current.weather_description)

        console.print(current_table)

        # Hourly forecast table
        if hourly_forecast:
            hourly_table = Table(
                title="Hourly Forecast (Next 24 Hours)",
                show_header=True,
                header_style="bold blue",
            )
            hourly_table.add_column("Time", style="cyan")
            hourly_table.add_column("Temp", style="green")
            hourly_table.add_column("Weather", style="yellow")
            hourly_table.add_column("Precip %", style="magenta")

            for forecast in hourly_forecast[:24]:  # Show next 24 hours
                time_str = forecast.time.strftime("%Y-%m-%d %H:%M")
                hourly_table.add_row(
                    time_str,
                    f"{forecast.temperature}°C",
                    forecast.weather_description,
                    f"{forecast.precipitation_probability or 0}%",
                )

            console.print("\n")
            console.print(hourly_table)

        # Daily forecast table
        if daily_forecast:
            daily_table = Table(
                title="Daily Forecast (Next 7 Days)",
                show_header=True,
                header_style="bold green",
            )
            daily_table.add_column("Date", style="cyan")
            daily_table.add_column("High/Low", style="green")
            daily_table.add_column("Weather", style="yellow")
            daily_table.add_column("Precip", style="blue")
            daily_table.add_column("Wind", style="magenta")

            for forecast in daily_forecast:
                date_str = forecast.date.strftime("%Y-%m-%d")
                temp_str = (
                    f"{forecast.temperature_max}°/{forecast.temperature_min}°"
                )
                precip_str = (
                    f"{forecast.precipitation_sum or 0}mm"
                    if forecast.precipitation_sum
                    else "0mm"
                )
                wind_str = (
                    f"{forecast.wind_speed_max or 0} km/h"
                    if forecast.wind_speed_max
                    else "N/A"
                )

                daily_table.add_row(
                    date_str,
                    temp_str,
                    forecast.weather_description,
                    precip_str,
                    wind_str,
                )

            console.print("\n")
            console.print(daily_table)

    asyncio.run(fetch_forecast())


def get_weather_app() -> typer.Typer:
    """Get the weather Typer app for registration in main CLI."""
    return weather_app

