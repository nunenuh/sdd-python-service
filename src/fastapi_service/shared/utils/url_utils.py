"""
URL utility functions.
"""

from typing import Optional
from urllib.parse import urljoin, urlparse


def normalize_url(url: str, base_url: Optional[str] = None) -> str:
    """Normalize a URL.

    Args:
        url: URL to normalize
        base_url: Optional base URL for relative URLs

    Returns:
        Normalized URL
    """
    if base_url and not url.startswith(("http://", "https://")):
        url = urljoin(base_url, url)

    parsed = urlparse(url)
    # Remove fragment and normalize
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    if parsed.query:
        normalized += f"?{parsed.query}"

    return normalized


def is_valid_url(url: str) -> bool:
    """Check if URL is valid.

    Args:
        url: URL to validate

    Returns:
        True if URL is valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
