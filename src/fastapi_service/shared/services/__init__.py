"""
Shared services for the news crawler service.
"""

from .article_extractor import ArticleExtractorService
from .elasticsearch_service import ElasticsearchService, get_elasticsearch_client
from .redis_service import RedisService, get_redis_client

__all__ = [
    "ArticleExtractorService",
    "ElasticsearchService",
    "get_elasticsearch_client",
    "RedisService",
    "get_redis_client",
]
