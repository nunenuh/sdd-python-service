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

    # Environment alias
    @property
    def ENVIRONMENT(self) -> str:
        """Alias for APP_ENVIRONMENT."""
        return self.APP_ENVIRONMENT


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
