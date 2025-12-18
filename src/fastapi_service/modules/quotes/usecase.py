"""
Quotes use case orchestration layer.
"""

from typing import List, Tuple

from .schemas import Quote
from .services import QuotesService, get_quotes_service


class QuotesUseCase:
    """Use case for orchestrating quotes operations."""

    def __init__(self):
        """Initialize quotes use case."""
        self.service = get_quotes_service()

    async def get_random_quote(
        self, tags: str = None, max_length: int = None
    ) -> Quote:
        """Get a random quote.

        Args:
            tags: Comma-separated tags to filter by (optional)
            max_length: Maximum quote length in characters (optional)

        Returns:
            Quote object
        """
        return await self.service.get_random_quote(tags=tags, max_length=max_length)

    async def get_quote_by_id(self, quote_id: str) -> Quote:
        """Get a specific quote by ID.

        Args:
            quote_id: Quote identifier

        Returns:
            Quote object
        """
        return await self.service.get_quote_by_id(quote_id)

    async def search_quotes(
        self,
        query: str = None,
        author: str = None,
        tags: str = None,
        min_length: int = None,
        max_length: int = None,
        limit: int = 20,
        skip: int = 0,
    ) -> Tuple[List[Quote], int]:
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
        """
        return await self.service.search_quotes(
            query=query,
            author=author,
            tags=tags,
            min_length=min_length,
            max_length=max_length,
            limit=limit,
            skip=skip,
        )

    async def get_quotes_by_author(
        self, author_slug: str, limit: int = 20, skip: int = 0
    ) -> Tuple[List[Quote], int]:
        """Get quotes by author slug.

        Args:
            author_slug: Author slug identifier
            limit: Maximum number of quotes to return (default: 20)
            skip: Number of quotes to skip for pagination (default: 0)

        Returns:
            Tuple of (list of Quote objects, total count)
        """
        return await self.service.get_quotes_by_author(
            author_slug=author_slug, limit=limit, skip=skip
        )

