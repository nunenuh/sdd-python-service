"""FastAPI dependency injection providers."""

import uuid

from fastapi import Depends

from .logging import get_logger


def get_request_id() -> str:
    """Generate a unique request ID for tracing."""
    return str(uuid.uuid4())


def get_logger_for_module(module_name: str):
    """Get logger for a specific module."""

    def _get_logger():
        return get_logger(f"fastapi_service.{module_name}")

    return _get_logger


# Common dependencies that can be injected into endpoints
CommonDeps = {
    "request_id": Depends(get_request_id),
}
