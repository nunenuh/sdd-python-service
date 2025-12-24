"""
Country service for fetching country data from REST Countries API.

This module contains the core business logic for country data retrieval,
separated from HTTP handling concerns.
"""

from typing import List, Optional

import httpx

from fastapi_service.core.config import get_settings
from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException

from .schemas import Country, Currency, Language

logger = get_logger(__name__)


class CountryService:
    """Service for fetching country data from REST Countries API."""

    BASE_URL = "https://restcountries.com/v3.1"

    def __init__(self):
        """Initialize country service."""
        self.settings = get_settings()
        self.timeout = 10.0

    def _transform_country_data(self, data: dict) -> Country:
        """Transform API response to Country schema.

        Args:
            data: Raw country data from API

        Returns:
            Country object
        """
        # Extract currencies
        currencies = None
        if "currencies" in data and data["currencies"]:
            currencies = [
                Currency(
                    code=code,
                    name=currency_info.get("name", ""),
                    symbol=currency_info.get("symbol", ""),
                )
                for code, currency_info in data["currencies"].items()
            ]

        # Extract languages
        languages = None
        if "languages" in data and data["languages"]:
            languages = [
                Language(code=code, name=name)
                for code, name in data["languages"].items()
            ]

        # Extract calling codes
        calling_codes = None
        if "idd" in data and "root" in data["idd"]:
            root = data["idd"].get("root", "")
            suffixes = data["idd"].get("suffixes", [])
            calling_codes = [f"{root}{suffix}" for suffix in suffixes]

        # Get flag URL
        flag_url = None
        if "flags" in data and "png" in data["flags"]:
            flag_url = data["flags"]["png"]

        return Country(
            name=data.get("name", {}).get("common", ""),
            official_name=data.get("name", {}).get("official", ""),
            capital=data.get("capital", []),
            region=data.get("region", ""),
            subregion=data.get("subregion"),
            population=data.get("population", 0),
            area=data.get("area"),
            currencies=currencies,
            languages=languages,
            flag=data.get("flag", ""),
            flag_url=flag_url,
            cca2=data.get("cca2", ""),
            cca3=data.get("cca3", ""),
            calling_codes=calling_codes,
            timezones=data.get("timezones"),
        )

    async def get_all_countries(
        self, fields: Optional[List[str]] = None
    ) -> List[Country]:
        """Get all countries.

        Args:
            fields: Optional list of fields to include (if None, returns all fields)

        Returns:
            List of Country objects

        Raises:
            ServiceException: If country data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.BASE_URL}/all"
                params = {}
                if fields:
                    params["fields"] = ",".join(fields)

                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                return [self._transform_country_data(country) for country in data]

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching countries: {str(e)}")
            raise ServiceException(f"Failed to fetch countries: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching countries: {str(e)}")
            raise ServiceException(f"Network error fetching countries: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching countries: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def get_country_by_name(self, name: str) -> Optional[Country]:
        """Get country by name.

        Args:
            name: Country name (common or official)

        Returns:
            Country object or None if not found

        Raises:
            ServiceException: If country data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.BASE_URL}/name/{name}"
                params = {"fullText": "false"}

                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if not data:
                    return None

                # Return the first match
                return self._transform_country_data(data[0])

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            logger.error(f"HTTP error fetching country: {str(e)}")
            raise ServiceException(f"Failed to fetch country: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching country: {str(e)}")
            raise ServiceException(f"Network error fetching country: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching country: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def get_country_by_code(self, code: str) -> Optional[Country]:
        """Get country by ISO code (alpha-2 or alpha-3).

        Args:
            code: ISO country code (e.g., 'US', 'USA', 'ID', 'IDN')

        Returns:
            Country object or None if not found

        Raises:
            ServiceException: If country data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.BASE_URL}/alpha/{code}"

                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                if not data:
                    return None

                return self._transform_country_data(data)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            logger.error(f"HTTP error fetching country: {str(e)}")
            raise ServiceException(f"Failed to fetch country: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching country: {str(e)}")
            raise ServiceException(f"Network error fetching country: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching country: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def search_countries_by_region(self, region: str) -> List[Country]:
        """Search countries by region.

        Args:
            region: Region name (e.g., 'Asia', 'Europe', 'Americas')

        Returns:
            List of Country objects

        Raises:
            ServiceException: If country data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                url = f"{self.BASE_URL}/region/{region}"

                response = await client.get(url)
                response.raise_for_status()
                data = response.json()

                return [self._transform_country_data(country) for country in data]

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching countries by region: {str(e)}")
            raise ServiceException(
                f"Failed to fetch countries by region: {str(e)}"
            )
        except httpx.RequestError as e:
            logger.error(f"Request error fetching countries by region: {str(e)}")
            raise ServiceException(
                f"Network error fetching countries by region: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching countries by region: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")


# Singleton instance
_country_service = None


def get_country_service() -> CountryService:
    """Get country service singleton instance."""
    global _country_service
    if _country_service is None:
        _country_service = CountryService()
    return _country_service

