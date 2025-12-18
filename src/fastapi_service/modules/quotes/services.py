"""
Quotes service for fetching quotes data from Quotable API.

This module contains the core business logic for quotes data retrieval,
separated from HTTP handling concerns.
"""

import os
from typing import List, Optional

import httpx

from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException

from .schemas import Quote

logger = get_logger(__name__)


class QuotesService:
    """Service for fetching quotes data from Quotable API."""

    BASE_URL = "https://api.quotable.io"

    def __init__(self):
        """Initialize quotes service."""
        self.timeout = 10.0
        # SSL verification setting specific to quotes module
        # Set QUOTES_VERIFY_SSL=true to enable SSL verification
        # Default is False for development/testing environments
        self.verify_ssl = os.getenv("QUOTES_VERIFY_SSL", "false").lower() in (
            "true",
            "1",
            "yes",
        )

    def _parse_quote(self, data: dict) -> Quote:
        """Parse quote data from API response.

        Args:
            data: Raw quote data from API

        Returns:
            Quote object
        """
        return Quote(
            id=data.get("_id", ""),
            content=data.get("content", ""),
            author=data.get("author", ""),
            author_slug=data.get("authorSlug"),
            tags=data.get("tags", []),
            length=data.get("length", 0),
            date_added=data.get("dateAdded"),
            date_modified=data.get("dateModified"),
        )

    async def get_random_quote(
        self, tags: Optional[str] = None, max_length: Optional[int] = None
    ) -> Quote:
        """Get a random quote.

        Args:
            tags: Comma-separated tags to filter by (optional)
            max_length: Maximum quote length in characters (optional)

        Returns:
            Quote object

        Raises:
            ServiceException: If quote data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                params = {}
                if tags:
                    params["tags"] = tags
                if max_length:
                    params["maxLength"] = max_length

                response = await client.get(
                    f"{self.BASE_URL}/quotes/random", params=params
                )
                response.raise_for_status()
                data = response.json()

                # API returns array with single quote for random endpoint
                if isinstance(data, list) and len(data) > 0:
                    return self._parse_quote(data[0])
                elif isinstance(data, dict):
                    return self._parse_quote(data)
                else:
                    raise ServiceException("Invalid response format from quotes API")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching random quote: {str(e)}")
            raise ServiceException(f"Failed to fetch random quote: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching random quote: {str(e)}")
            raise ServiceException(f"Network error fetching random quote: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching random quote: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def get_quote_by_id(self, quote_id: str) -> Quote:
        """Get a specific quote by ID.

        Args:
            quote_id: Quote identifier

        Returns:
            Quote object

        Raises:
            ServiceException: If quote data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                response = await client.get(f"{self.BASE_URL}/quotes/{quote_id}")
                response.raise_for_status()
                data = response.json()

                return self._parse_quote(data)

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ServiceException(f"Quote with ID '{quote_id}' not found")
            logger.error(f"HTTP error fetching quote: {str(e)}")
            raise ServiceException(f"Failed to fetch quote: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching quote: {str(e)}")
            raise ServiceException(f"Network error fetching quote: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching quote: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def search_quotes(
        self,
        query: Optional[str] = None,
        author: Optional[str] = None,
        tags: Optional[str] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        limit: int = 20,
        skip: int = 0,
    ) -> tuple[List[Quote], int]:
        """Search for quotes with filters.

        Args:
            query: Search query string (optional)
            author: Filter by author name (optional)
            tags: Comma-separated tags to filter by (optional)
            min_length: Minimum quote length in characters (optional)
            max_length: Maximum quote length in characters (optional)
            limit: Maximum number of quotes to return (default: 20)
            skip: Number of quotes to skip for pagination (default: 0)

        Returns:
            Tuple of (list of Quote objects, total count)

        Raises:
            ServiceException: If quotes data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                params = {
                    "limit": limit,
                    "skip": skip,
                }

                if query:
                    params["query"] = query
                if author:
                    params["author"] = author
                if tags:
                    params["tags"] = tags
                if min_length:
                    params["minLength"] = min_length
                if max_length:
                    params["maxLength"] = max_length

                response = await client.get(f"{self.BASE_URL}/quotes", params=params)
                response.raise_for_status()
                data = response.json()

                quotes = [self._parse_quote(quote_data) for quote_data in data.get("results", [])]
                total_count = data.get("totalCount", len(quotes))

                return quotes, total_count

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error searching quotes: {str(e)}")
            raise ServiceException(f"Failed to search quotes: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error searching quotes: {str(e)}")
            raise ServiceException(f"Network error searching quotes: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error searching quotes: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")

    async def get_quotes_by_author(
        self, author_slug: str, limit: int = 20, skip: int = 0
    ) -> tuple[List[Quote], int]:
        """Get quotes by author slug.

        Args:
            author_slug: Author slug identifier
            limit: Maximum number of quotes to return (default: 20)
            skip: Number of quotes to skip for pagination (default: 0)

        Returns:
            Tuple of (list of Quote objects, total count)

        Raises:
            ServiceException: If quotes data cannot be fetched
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify_ssl) as client:
                params = {
                    "limit": limit,
                    "skip": skip,
                }

                response = await client.get(
                    f"{self.BASE_URL}/quotes", params={**params, "author": author_slug}
                )
                response.raise_for_status()
                data = response.json()

                quotes = [self._parse_quote(quote_data) for quote_data in data.get("results", [])]
                total_count = data.get("totalCount", len(quotes))

                return quotes, total_count

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error fetching quotes by author: {str(e)}")
            raise ServiceException(f"Failed to fetch quotes by author: {str(e)}")
        except httpx.RequestError as e:
            logger.error(f"Request error fetching quotes by author: {str(e)}")
            raise ServiceException(f"Network error fetching quotes by author: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching quotes by author: {str(e)}")
            raise ServiceException(f"Unexpected error: {str(e)}")


# Singleton instance
_quotes_service = None


def get_quotes_service() -> QuotesService:
    """Get quotes service singleton instance."""
    global _quotes_service
    if _quotes_service is None:
        _quotes_service = QuotesService()
    return _quotes_service

