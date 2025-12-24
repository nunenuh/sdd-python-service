"""
Country use case orchestration layer.
"""

from typing import List, Optional

from .schemas import Country
from .services import CountryService, get_country_service


class CountryUseCase:
    """Use case for orchestrating country operations."""

    def __init__(self):
        """Initialize country use case."""
        self.service = get_country_service()

    async def get_all_countries(
        self, fields: Optional[List[str]] = None
    ) -> List[Country]:
        """Get all countries.

        Args:
            fields: Optional list of fields to include

        Returns:
            List of Country objects
        """
        return await self.service.get_all_countries(fields)

    async def get_country_by_name(self, name: str) -> Optional[Country]:
        """Get country by name.

        Args:
            name: Country name (common or official)

        Returns:
            Country object or None if not found
        """
        return await self.service.get_country_by_name(name)

    async def get_country_by_code(self, code: str) -> Optional[Country]:
        """Get country by ISO code.

        Args:
            code: ISO country code (alpha-2 or alpha-3)

        Returns:
            Country object or None if not found
        """
        return await self.service.get_country_by_code(code)

    async def search_countries_by_region(self, region: str) -> List[Country]:
        """Search countries by region.

        Args:
            region: Region name (e.g., 'Asia', 'Europe', 'Americas')

        Returns:
            List of Country objects
        """
        return await self.service.search_countries_by_region(region)

