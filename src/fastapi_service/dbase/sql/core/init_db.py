"""
Database initialization.

This module handles database initialization and setup.
Note: Tables should be created with Alembic migrations.
"""

from sqlalchemy.orm import Session

# Import all models here to ensure they are registered with SQLAlchemy
# This is important for Alembic migrations to detect all models
from ..models import Article, CrawlLog, Source  # noqa: F401


def init_db(db: Session) -> None:
    """
    Initialize database with any required setup.

    Note: Tables should be created with Alembic migrations.
    If you don't want to use migrations, uncomment the next line.
    """
    # Base.metadata.create_all(bind=engine)
    pass
