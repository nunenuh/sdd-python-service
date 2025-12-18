# Health Module Specifications

This directory contains specifications for the Health module, which provides health check and monitoring endpoints.

## Purpose

The Health module provides endpoints for:
- **Liveness checks** - Simple ping endpoint for load balancers
- **Readiness checks** - Basic health status with dependency checks
- **Detailed monitoring** - Comprehensive health information with system metrics

## Files

- **`api.md`** - Complete API specification for health check endpoints, including request/response formats, status codes, and error handling.

## Endpoints

- `GET /api/v1/health/ping` - Simple liveness check
- `GET /api/v1/health/status` - Basic health status with dependencies
- `GET /api/v1/health/detailed` - Comprehensive health with system metrics

## Implementation

The Health module follows the layered architecture pattern:
- **Handler**: `src/fastapi_service/modules/health/apiv1/handler.py`
- **Use Case**: `src/fastapi_service/modules/health/usecase.py`
- **Service**: `src/fastapi_service/modules/health/services.py`
- **Schemas**: `src/fastapi_service/modules/health/schemas.py`

## Related Documentation

- API contract: `../../contracts/api-contract.md`
- Module structure conventions: `../../conventions/03-module-structure.md`

