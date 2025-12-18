"""
Date utility functions.
"""

from datetime import datetime
from typing import Optional

from dateutil import parser


def parse_date(date_string: Optional[str]) -> Optional[datetime]:
    """Parse a date string to datetime.

    Args:
        date_string: Date string to parse

    Returns:
        Datetime object or None if parsing fails
    """
    if not date_string:
        return None

    try:
        return parser.parse(date_string)
    except Exception:
        return None


def format_date(
    dt: Optional[datetime], format_str: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[str]:
    """Format a datetime to string.

    Args:
        dt: Datetime object
        format_str: Format string

    Returns:
        Formatted date string or None if dt is None
    """
    if not dt:
        return None
    return dt.strftime(format_str)
