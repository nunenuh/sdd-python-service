"""
Application configuration using Pydantic settings.
"""

from functools import lru_cache
from typing import List

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",  # Ignore extra fields from .env file
    )

    # Application
    APP_NAME: str = Field(default="FastAPI Service", description="Application name")
    APP_DESCRIPTION: str = Field(
        default="FastAPI Service Boilerplate - Indonesian Media Scraping System",
        description="Application description",
    )
    APP_HOST: str = Field(default="0.0.0.0", description="Server host")
    APP_PORT: int = Field(default=8080, description="Server port")
    APP_ENVIRONMENT: str = Field(
        default="development", description="Application environment"
    )
    APP_VERSION: str = Field(default="0.1.0", description="Application version")
    APP_DEBUG: bool = Field(default=False, description="Application debug")

    APP_X_API_KEY: str = Field(
        default="changeme",
        description="API key for FastAPI X-API-Key header authentication",
    )

    ALLOWED_ORIGINS_STR: str = Field(
        default="*",
        description="CORS allowed origins (comma-separated)",
    )

    @property
    def allowed_origins(self) -> List[str]:
        """Parse allowed_origins from comma-separated string."""
        if not self.ALLOWED_ORIGINS_STR:
            return ["*"]

        # Handle comma-separated string
        if "," in self.ALLOWED_ORIGINS_STR:
            return [origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")]
        # Handle single string
        return [self.ALLOWED_ORIGINS_STR.strip()]

    # Database Settings
    DB_HOST: str = Field(default="localhost", description="PostgreSQL database host")
    DB_PORT: int = Field(default=5432, description="PostgreSQL database port")
    DB_NAME: str = Field(
        default="fastapi_service", description="PostgreSQL database name"
    )
    DB_USER: str = Field(default="postgres", description="PostgreSQL database user")
    DB_PASSWORD: str = Field(
        default="postgres", description="PostgreSQL database password"
    )
    DB_POOL_SIZE: int = Field(default=10, description="Database connection pool size")
    DB_MAX_OVERFLOW: int = Field(default=20, description="Maximum overflow connections")
    DB_POOL_TIMEOUT: int = Field(
        default=30, description="Connection pool timeout in seconds"
    )
    DB_POOL_RECYCLE: int = Field(
        default=3600, description="Connection pool recycle time in seconds"
    )

    @property
    def database_url(self) -> str:
        """Get database connection URL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Redis Settings
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: str = Field(
        default="", description="Redis password (empty if no auth)"
    )

    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # Meilisearch Settings
    MEILISEARCH_URL: str = Field(
        default="http://localhost:7700", description="Meilisearch server URL"
    )
    MEILISEARCH_MASTER_KEY: str = Field(
        default="master-key-change-in-production", description="Meilisearch master key"
    )
    MEILISEARCH_INDEX_NAME: str = Field(
        default="articles", description="Meilisearch index name"
    )

    # Elasticsearch Settings (kept for migration period)
    ELASTICSEARCH_HOST: str = Field(
        default="localhost", description="Elasticsearch host"
    )
    ELASTICSEARCH_PORT: int = Field(default=9200, description="Elasticsearch port")
    ELASTICSEARCH_USERNAME: str = Field(
        default="", description="Elasticsearch username (empty if no auth)"
    )
    ELASTICSEARCH_PASSWORD: str = Field(
        default="", description="Elasticsearch password (empty if no auth)"
    )

    @property
    def elasticsearch_url(self) -> str:
        """Get Elasticsearch connection URL."""
        if self.ELASTICSEARCH_USERNAME and self.ELASTICSEARCH_PASSWORD:
            return f"http://{self.ELASTICSEARCH_USERNAME}:{self.ELASTICSEARCH_PASSWORD}@{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"
        return f"http://{self.ELASTICSEARCH_HOST}:{self.ELASTICSEARCH_PORT}"

    # Scrapy Settings
    SCRAPY_CONCURRENT_REQUESTS: int = Field(
        default=16, description="Maximum concurrent requests per spider"
    )
    SCRAPY_DOWNLOAD_DELAY: float = Field(
        default=0.5, description="Download delay between requests (seconds)"
    )
    SCRAPY_RANDOMIZE_DOWNLOAD_DELAY: bool = Field(
        default=True, description="Randomize download delay"
    )
    SCRAPY_AUTOTHROTTLE_ENABLED: bool = Field(
        default=True, description="Enable automatic throttling"
    )

    # Crawler Settings
    CRAWLER_USER_AGENT: str = Field(
        default="SainCrawlerNews/0.1.0 (+https://github.com/OneDataID/fastapi-service)",
        description="User agent for crawler requests",
    )
    CRAWLER_ROBOTS_TXT_COMPLIANCE: bool = Field(
        default=True, description="Respect robots.txt"
    )
    CRAWLER_MAX_ARTICLES_PER_RUN: int = Field(
        default=1000, description="Maximum articles to crawl per run"
    )

    # HTTP Client Settings
    HTTP_VERIFY_SSL: bool = Field(
        default=True,
        description="Verify SSL certificates for HTTP requests (set False only for development/testing)",
    )

    # Environment alias
    @property
    def ENVIRONMENT(self) -> str:
        """Alias for APP_ENVIRONMENT."""
        return self.APP_ENVIRONMENT


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
