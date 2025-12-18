"""
Health check API endpoints for the news crawler service.

This module provides HTTP endpoints for health monitoring. All business logic
is delegated to the health service layer, keeping this module focused purely
on HTTP request/response handling.

Endpoints:
- GET /ping: Simple liveness check
- GET /status: Basic health with dependencies
- GET /detailed: Comprehensive health with system metrics
"""

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException

from fastapi_service.core.config import get_settings
from fastapi_service.core.logging import get_logger
from ..schemas import DetailedHealthResponse, HealthStatusResponse, PingResponse
from ..usecase import HealthUseCase

logger = get_logger(__name__)
router = APIRouter()


@router.get("/ping", response_model=PingResponse)
async def ping():
    """
    Simple ping endpoint for liveness checks.

    This endpoint should always return quickly and is used by load balancers
    and orchestration systems to determine if the service is alive.
    """
    return PingResponse(status="ok", timestamp=datetime.now(UTC), message="pong")


@router.get("/status", response_model=HealthStatusResponse)
async def get_health_status():
    """
    Get basic health status with dependency checks.

    This endpoint provides a quick overview of service health including
    essential dependencies. Used for readiness checks.
    """
    usecase = HealthUseCase()

    try:
        overall_status, components, uptime = usecase.get_basic_health()

        return HealthStatusResponse(
            status=overall_status,
            timestamp=datetime.now(UTC),
            version=get_settings().APP_VERSION,
            components=components,
            uptime_seconds=uptime,
        )

    except Exception as e:
        logger.error(f"Health status check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "health_check_failed",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )


@router.get("/detailed", response_model=DetailedHealthResponse)
async def get_detailed_health_status():
    """
    Get comprehensive health status with system metrics.

    This endpoint provides detailed health information including component
    checks, system metrics, and performance data. Used for monitoring
    and debugging purposes.
    """
    usecase = HealthUseCase()

    try:
        (
            overall_status,
            components,
            system_metrics,
            process_metrics,
            system_info,
            uptime,
        ) = usecase.get_detailed_health()

        return DetailedHealthResponse(
            status=overall_status,
            timestamp=datetime.now(UTC),
            version=get_settings().APP_VERSION,
            uptime_seconds=uptime,
            components=components,
            system_metrics=system_metrics,
            process_metrics=process_metrics,
            system_info=system_info,
            environment=get_settings().APP_ENVIRONMENT,
            debug_mode=get_settings().APP_DEBUG,
        )

    except Exception as e:
        logger.error(f"Detailed health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "error": "detailed_health_check_failed",
                "message": str(e),
                "timestamp": datetime.now(UTC).isoformat(),
            },
        )
