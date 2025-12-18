# Weather Module Specifications

This directory contains specifications for the Weather module, which provides weather data retrieval endpoints using the Open-Meteo API.

## Purpose

The Weather module provides endpoints for:
- **Current Weather** - Get current weather conditions for any location
- **Weather Forecast** - Get current weather with hourly (48h) and daily (7d) forecasts

## API Provider

This module uses **Open-Meteo API** (https://open-meteo.com/):
- **Free and Open-Source** - No API key required
- **High Resolution Forecasts** - 1-11km resolution
- **Global Coverage** - Weather data for any location worldwide
- **Historical Data** - Access to 80+ years of historical weather data

## Files

- **`api.md`** - Complete API specification for weather endpoints (to be created)

## Endpoints

- `GET /api/v1/weather/current` - Get current weather conditions
- `GET /api/v1/weather/forecast` - Get current weather with forecasts

## Implementation

The Weather module follows the layered architecture pattern:
- **Handler**: `src/fastapi_service/modules/weather/apiv1/handler.py`
- **Use Case**: `src/fastapi_service/modules/weather/usecase.py`
- **Service**: `src/fastapi_service/modules/weather/services.py`
- **Schemas**: `src/fastapi_service/modules/weather/schemas.py`

## Request Parameters

### Current Weather
- `latitude` (required): Latitude coordinate (-90 to 90)
- `longitude` (required): Longitude coordinate (-180 to 180)
- `timezone` (optional): Timezone (default: "auto")

### Forecast
- `latitude` (required): Latitude coordinate (-90 to 90)
- `longitude` (required): Longitude coordinate (-180 to 180)
- `timezone` (optional): Timezone (default: "auto")
- `hourly` (optional): Include hourly forecast (default: true)
- `daily` (optional): Include daily forecast (default: true)

## Response Format

All responses include:
- Location information (name, coordinates, timezone)
- Current weather conditions (temperature, humidity, wind, weather code)
- Optional hourly forecast (48 hours)
- Optional daily forecast (7 days)
- Response timestamp

## Related Documentation

- API contract: `../../contracts/api-contract.md`
- Module structure conventions: `../../conventions/03-module-structure.md`
- Open-Meteo API: https://open-meteo.com/

