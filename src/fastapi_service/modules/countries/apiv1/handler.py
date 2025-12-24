"""
Country API endpoints for the FastAPI service.

This module provides HTTP endpoints for country data retrieval. All business logic
is delegated to the country service layer, keeping this module focused purely
on HTTP request/response handling.
"""

from datetime import UTC, datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException

from ..schemas import CountryErrorResponse, CountryListResponse, CountryResponse
from ..usecase import CountryUseCase

logger = get_logger(__name__)
router = APIRouter()


@router.get("/all", response_model=CountryListResponse)
async def get_all_countries(
    fields: Optional[str] = Query(
        None,
        description="Comma-separated list of fields to include (e.g., 'name,capital,population')",
    ),
):
    """
    Get all countries.

    This endpoint retrieves information about all countries from the REST Countries API.
    You can optionally specify which fields to include in the response.
    """
    usecase = CountryUseCase()

    try:
        field_list = fields.split(",") if fields else None
        countries = await usecase.get_all_countries(field_list)

        return CountryListResponse(countries=countries, total=len(countries))

    except ServiceException as e:
        logger.error(f"Country service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "country_service_error",
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


@router.get("/name/{name}", response_model=CountryResponse)
async def get_country_by_name(name: str):
    """
    Get country by name.

    This endpoint retrieves information about a specific country by its name.
    The name can be either the common name or official name.
    """
    usecase = CountryUseCase()

    try:
        country = await usecase.get_country_by_name(name)

        if not country:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "not_found",
                    "message": f"Country '{name}' not found",
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        return CountryResponse(country=country)

    except HTTPException:
        raise
    except ServiceException as e:
        logger.error(f"Country service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "country_service_error",
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


@router.get("/code/{code}", response_model=CountryResponse)
async def get_country_by_code(code: str):
    """
    Get country by ISO code.

    This endpoint retrieves information about a specific country by its ISO code.
    Supports both alpha-2 (e.g., 'US', 'ID') and alpha-3 (e.g., 'USA', 'IDN') codes.
    """
    usecase = CountryUseCase()

    try:
        country = await usecase.get_country_by_code(code.upper())

        if not country:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "not_found",
                    "message": f"Country with code '{code}' not found",
                    "timestamp": datetime.now(UTC).isoformat(),
                },
            )

        return CountryResponse(country=country)

    except HTTPException:
        raise
    except ServiceException as e:
        logger.error(f"Country service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "country_service_error",
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


@router.get("/region/{region}", response_model=CountryListResponse)
async def get_countries_by_region(region: str):
    """
    Get countries by region.

    This endpoint retrieves all countries in a specific region.
    Common regions include: Asia, Europe, Americas, Africa, Oceania, Antarctic.
    """
    usecase = CountryUseCase()

    try:
        countries = await usecase.search_countries_by_region(region)

        return CountryListResponse(countries=countries, total=len(countries))

    except ServiceException as e:
        logger.error(f"Country service error: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "country_service_error",
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

