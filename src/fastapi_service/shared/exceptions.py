"""Custom exception classes for the news crawler service."""

from typing import Any, Dict, Optional

from fastapi import HTTPException, status


class BaseException(Exception):
    """Base exception class for the application."""

    def __init__(self, message: str = "An error occurred") -> None:
        """Initialize base exception.

        Args:
            message: Error message.
        """
        self.message = message
        super().__init__(self.message)


class ValidationException(BaseException):
    """Exception raised for validation errors."""

    def __init__(self, message: str = "Validation error") -> None:
        """Initialize validation exception.

        Args:
            message: Validation error message.
        """
        super().__init__(message)


class RepositoryException(BaseException):
    """Exception raised for repository errors."""

    def __init__(self, message: str = "Repository error") -> None:
        """Initialize repository exception.

        Args:
            message: Repository error message.
        """
        super().__init__(message)


class ServiceException(BaseException):
    """Exception raised for service-level errors."""

    def __init__(self, message: str = "Service error") -> None:
        """Initialize service exception.

        Args:
            message: Service error message.
        """
        super().__init__(message)


class CrawlerException(BaseException):
    """Exception raised for crawler errors."""

    def __init__(self, message: str = "Crawler error") -> None:
        """Initialize crawler exception.

        Args:
            message: Crawler error message.
        """
        super().__init__(message)


class BaseHTTPException(HTTPException):
    """Base HTTP exception for the microservice."""

    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.message = message
        self.details = details or {}
