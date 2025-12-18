"""
Quotes response schemas for the FastAPI service.

This module defines Pydantic models for structuring quotes API responses,
ensuring consistent API response formats.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class QuoteAuthor(BaseModel):
    """Author information for a quote."""

    name: str = Field(..., description="Author name")
    slug: Optional[str] = Field(None, description="Author slug/identifier")


class Quote(BaseModel):
    """Single quote with author information."""

    id: str = Field(..., description="Unique quote identifier")
    content: str = Field(..., description="Quote content/text")
    author: str = Field(..., description="Author name")
    author_slug: Optional[str] = Field(None, description="Author slug/identifier")
    tags: List[str] = Field(default_factory=list, description="Quote tags/categories")
    length: int = Field(..., description="Quote length in characters")
    date_added: Optional[str] = Field(None, description="Date quote was added")
    date_modified: Optional[str] = Field(None, description="Date quote was last modified")


class QuoteResponse(BaseModel):
    """Single quote response."""

    quote: Quote = Field(..., description="Quote data")
    timestamp: datetime = Field(..., description="Response timestamp")


class QuotesListResponse(BaseModel):
    """List of quotes response."""

    quotes: List[Quote] = Field(..., description="List of quotes")
    count: int = Field(..., description="Total number of quotes returned")
    page: Optional[int] = Field(None, description="Current page number")
    total_count: Optional[int] = Field(None, description="Total quotes available")
    timestamp: datetime = Field(..., description="Response timestamp")


class RandomQuoteResponse(BaseModel):
    """Random quote response."""

    quote: Quote = Field(..., description="Random quote data")
    timestamp: datetime = Field(..., description="Response timestamp")


class QuoteErrorResponse(BaseModel):
    """Error response for quotes API."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    timestamp: datetime = Field(..., description="Error timestamp")

