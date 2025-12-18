"""
Redis service for caching and deduplication.
"""

from typing import Optional

import redis
from redis import Redis

from ..core.config import get_settings
from ..core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()

# Redis connection pool (singleton)
_redis_client: Optional[Redis] = None


def get_redis_client() -> Redis:
    """Get Redis client instance (singleton).

    Returns:
        Redis client instance
    """
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
            )
            # Test connection
            _redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    return _redis_client


class RedisService:
    """Service for Redis operations."""

    def __init__(self):
        """Initialize Redis service."""
        self.client = get_redis_client()

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set a key-value pair.

        Args:
            key: Redis key
            value: Value to store
            ttl: Optional time-to-live in seconds

        Returns:
            True if successful
        """
        try:
            if ttl:
                return self.client.setex(key, ttl, value)
            return self.client.set(key, value)
        except Exception as e:
            logger.error(f"Failed to set Redis key {key}: {str(e)}")
            return False

    def get(self, key: str) -> Optional[str]:
        """Get a value by key.

        Args:
            key: Redis key

        Returns:
            Value or None if not found
        """
        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Failed to get Redis key {key}: {str(e)}")
            return None

    def delete(self, key: str) -> bool:
        """Delete a key.

        Args:
            key: Redis key

        Returns:
            True if deleted
        """
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Failed to delete Redis key {key}: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        """Check if a key exists.

        Args:
            key: Redis key

        Returns:
            True if key exists
        """
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Failed to check Redis key {key}: {str(e)}")
            return False

    def set_url_seen(self, url: str, ttl: int = 86400) -> bool:
        """Mark a URL as seen (for deduplication).

        Args:
            url: URL to mark as seen
            ttl: Time-to-live in seconds (default: 24 hours)

        Returns:
            True if URL was not seen before, False if already seen
        """
        key = f"url_seen:{url}"
        if self.exists(key):
            return False
        return self.set(key, "1", ttl=ttl)
