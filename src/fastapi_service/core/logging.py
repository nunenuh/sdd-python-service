"""
Logging configuration for the application with structured logging support.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from .config import get_settings


def setup_logging() -> None:
    """Configure application logging with structured logging support."""
    settings = get_settings()

    # Determine log level based on environment
    log_level = (
        logging.DEBUG if settings.APP_ENVIRONMENT == "development" else logging.INFO
    )

    # Configure renderer based on environment
    if settings.APP_ENVIRONMENT == "production":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            renderer,
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    logging.getLogger("scrapy").setLevel(logging.WARNING)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance for the given name."""
    return structlog.get_logger(name)


def get_structured_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger with context support."""
    return structlog.get_logger(name)


def log_request_info(
    method: str,
    url: str,
    headers: Dict[str, Any] | None = None,
    body: Any = None,
) -> None:
    """Log request information for debugging."""
    logger = get_logger(__name__)
    logger.info(f"Request: {method} {url}")

    if headers:
        logger.debug(f"Headers: {headers}")

    if body:
        logger.debug(f"Body: {body}")


def log_response_info(
    status_code: int,
    response_time: float | None = None,
    error: Exception | None = None,
) -> None:
    """Log response information."""
    logger = get_logger(__name__)

    if error:
        logger.error(f"Response: {status_code} - Error: {str(error)}")
    else:
        logger.info(f"Response: {status_code}")

    if response_time:
        logger.info(f"Response time: {response_time:.2f}ms")
