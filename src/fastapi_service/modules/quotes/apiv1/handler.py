"""
Quotes API endpoints for the FastAPI service.

This module provides HTTP endpoints for quotes data retrieval. All business logic
is delegated to the quotes service layer, keeping this module focused purely
on HTTP request/response handling.
"""

from datetime import UTC, datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException

from ..schemas import (
    QuoteErrorResponse,
    QuoteResponse,
    QuotesListResponse,
    RandomQuoteResponse,
)
from ..usecase import QuotesUseCase

logger = get_logger(__name__)
router = APIRouter()


@router.get("/random", response_model=RandomQuoteResponse)
async def get_random_quote(
    tags: Optional[str] = Query(
        None, description="Comma-separated tags to filter by", example="inspirational"
    ),
    max_length: Optional[int] = Query(
        None, description="Maximum quote length in characters", ge=1, example=100
    ),
):
    """
    Get a random quote.

    This endpoint provides a random quote, optionally filtered by tags or maximum length.
    """
    usecase = QuotesUseCase()

    try:
        quote = await usecase.get_random_quote(tags=tags, max_length=max_length)

        return RandomQuoteResponse(quote=quote, timestamp=datetime.now(UTC))

    except ServiceException as e:
        logger.error(f"Quotes service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "quotes_service_error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )


@router.get("/author/{author_slug}", response_model=QuotesListResponse)
async def get_quotes_by_author(
    author_slug: str,
    limit: int = Query(20, description="Maximum number of quotes to return", ge=1, le=150),
    skip: int = Query(0, description="Number of quotes to skip for pagination", ge=0),
):
    """
    Get quotes by author slug.

    This endpoint retrieves all quotes from a specific author using their slug identifier.
    """
    usecase = QuotesUseCase()

    try:
        quotes, total_count = await usecase.get_quotes_by_author(
            author_slug=author_slug, limit=limit, skip=skip
        )

        page = (skip // limit) + 1 if limit > 0 else 1

        return QuotesListResponse(
            quotes=quotes,
            count=len(quotes),
            page=page,
            total_count=total_count,
            timestamp=datetime.now(UTC),
        )

    except ServiceException as e:
        logger.error(f"Quotes service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "quotes_service_error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )


@router.get("/", response_model=QuotesListResponse)
async def search_quotes(
    query: Optional[str] = Query(
        None, description="Search query string", example="success"
    ),
    author: Optional[str] = Query(
        None, description="Filter by author name", example="Einstein"
    ),
    tags: Optional[str] = Query(
        None,
        description="Comma-separated tags to filter by",
        example="inspirational,wisdom",
    ),
    min_length: Optional[int] = Query(
        None, description="Minimum quote length in characters", ge=1, example=50
    ),
    max_length: Optional[int] = Query(
        None, description="Maximum quote length in characters", ge=1, example=200
    ),
    limit: int = Query(20, description="Maximum number of quotes to return", ge=1, le=150),
    skip: int = Query(0, description="Number of quotes to skip for pagination", ge=0),
):
    """
    Search for quotes with filters.

    This endpoint provides a list of quotes matching the specified criteria,
    with support for pagination and various filters.
    """
    usecase = QuotesUseCase()

    try:
        quotes, total_count = await usecase.search_quotes(
            query=query,
            author=author,
            tags=tags,
            min_length=min_length,
            max_length=max_length,
            limit=limit,
            skip=skip,
        )

        page = (skip // limit) + 1 if limit > 0 else 1

        return QuotesListResponse(
            quotes=quotes,
            count=len(quotes),
            page=page,
            total_count=total_count,
            timestamp=datetime.now(UTC),
        )

    except ServiceException as e:
        logger.error(f"Quotes service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "quotes_service_error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )


@router.get("/{quote_id}", response_model=QuoteResponse)
async def get_quote_by_id(quote_id: str):
    """
    Get a specific quote by ID.

    This endpoint retrieves a quote using its unique identifier.
    """
    usecase = QuotesUseCase()

    try:
        quote = await usecase.get_quote_by_id(quote_id)

        return QuoteResponse(quote=quote, timestamp=datetime.now(UTC))

    except ServiceException as e:
        logger.error(f"Quotes service error: {str(e)}")
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "quote_not_found",
                    "message": str(e),
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )
        raise HTTPException(
            status_code=503,
            detail={
                "error": "quotes_service_error",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
