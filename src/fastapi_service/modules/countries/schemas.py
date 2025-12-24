"""
Country response schemas for the FastAPI service.

This module defines Pydantic models for structuring country API responses,
ensuring consistent API response formats.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class Currency(BaseModel):
    """Currency information."""

    code: str = Field(..., description="Currency code (e.g., USD)")
    name: str = Field(..., description="Currency name")
    symbol: str = Field(..., description="Currency symbol")


class Language(BaseModel):
    """Language information."""

    code: Optional[str] = Field(None, description="Language code")
    name: str = Field(..., description="Language name")


class Country(BaseModel):
    """Country information."""

    name: str = Field(..., description="Country name")
    official_name: str = Field(..., description="Official country name")
    capital: Optional[List[str]] = Field(None, description="Capital cities")
    region: str = Field(..., description="Region (e.g., Asia, Europe)")
    subregion: Optional[str] = Field(None, description="Subregion")
    population: int = Field(..., description="Population")
    area: Optional[float] = Field(None, description="Area in square kilometers")
    currencies: Optional[List[Currency]] = Field(None, description="Currencies")
    languages: Optional[List[Language]] = Field(None, description="Languages")
    flag: str = Field(..., description="Flag emoji")
    flag_url: Optional[str] = Field(None, description="Flag image URL")
    cca2: str = Field(..., description="ISO 3166-1 alpha-2 code")
    cca3: str = Field(..., description="ISO 3166-1 alpha-3 code")
    calling_codes: Optional[List[str]] = Field(None, description="Calling codes")
    timezones: Optional[List[str]] = Field(None, description="Timezones")


class CountryListResponse(BaseModel):
    """Response containing a list of countries."""

    countries: List[Country] = Field(..., description="List of countries")
    total: int = Field(..., description="Total number of countries")


class CountryResponse(BaseModel):
    """Response containing a single country."""

    country: Country = Field(..., description="Country information")


class CountryErrorResponse(BaseModel):
    """Error response for country API."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")

