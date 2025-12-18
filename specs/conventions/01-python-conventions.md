---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Python Conventions

Complete Python coding conventions for FastAPI Service service.

**Source**: `.cursorrules` and actual codebase patterns

## Code Style

### PEP 8 Compliance
- Follow PEP 8 Python style guide
- Use Black for code formatting (line length: 88)
- Use isort for import sorting (profile: black)

### Type Hints
- Use type hints for all function signatures
- Prefer explicit types over `Any`
- Use `Optional[T]` for nullable types
- Use `List[T]`, `Dict[K, V]` for collections

**Example**:
```python
from typing import List, Optional, Dict, Any

def get_articles(
    skip: int = 0,
    limit: int = 100,
    source_name: Optional[str] = None
) -> List[Dict[str, Any]]:
    ...
```

### Async/Await
- Prefer async/await for I/O operations
- Use `async def` for FastAPI route handlers
- Use `await` for database operations, HTTP requests, etc.

**Example**:
```python
@router.get("/articles")
async def list_articles(
    db: Session = Depends(get_db_session)
) -> ArticleListResponse:
    articles = await article_service.get_all(db)
    return ArticleListResponse(items=articles)
```

### Imports
- Use absolute imports
- Group imports: standard library, third-party, local
- Use isort with black profile for consistent ordering

**Example**:
```python
# Standard library
from datetime import datetime
from typing import Optional

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Local
from ...core.logging import get_logger
from ..schemas import ArticleResponse
```

## Naming Conventions

### Modules and Packages
- Use lowercase with underscores: `article_handler.py`
- Package names: `fastapi_service`

### Classes
- Use PascalCase: `ArticleRepository`, `CrawlerService`
- Base classes: `BaseNewsSpider`, `BaseModel`

### Functions and Methods
- Use snake_case: `get_article()`, `create_crawl_log()`
- Private methods: prefix with underscore `_internal_method()`

### Constants
- Use UPPER_SNAKE_CASE: `MAX_ARTICLES`, `DEFAULT_TIMEOUT`

### Variables
- Use snake_case: `article_id`, `source_name`
- Boolean variables: `is_enabled`, `has_error`

## Project Structure Patterns

### Module Structure
Each feature module follows this structure:
```
modules/<feature>/
├── apiv1/
│   └── handler.py      # FastAPI route handlers
├── usecase.py          # Use case orchestration
├── services.py         # Business logic services
├── repositories.py     # Data access layer
└── schemas.py          # Pydantic models
```

### Handler Pattern
```python
@router.get("/{id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: Session = Depends(get_db_session),
):
    """Get article by ID."""
    usecase = ArticleUseCase(db=db)
    article = usecase.get_article(article_id, db=db)
    if not article:
        raise HTTPException(status_code=404, detail="Not found")
    return article
```

### UseCase Pattern
```python
class ArticleUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.service = ArticleService()
        self.repository = ArticleRepository(db)
    
    def get_article(self, article_id: int, db: Session) -> Optional[ArticleResponse]:
        """Get article by ID."""
        article = self.repository.find_by_id(article_id)
        if not article:
            return None
        return ArticleResponse.from_orm(article)
```

### Repository Pattern
```python
class ArticleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, article_id: int) -> Optional[Article]:
        """Find article by ID."""
        return self.db.query(Article).filter(Article.id == article_id).first()
```

### Service Pattern
```python
class ArticleService:
    def validate_article(self, article_data: ArticleCreate) -> bool:
        """Validate article data."""
        # Business logic validation
        return True
```

## Pydantic Models

### Request/Response Models
- Use Pydantic `BaseModel` for all request/response models
- Define in `schemas.py` files
- Use `Field()` for validation and documentation

**Example**:
```python
from pydantic import BaseModel, Field

class ArticleCreate(BaseModel):
    title: str = Field(..., max_length=500, description="Article title")
    content: str = Field(..., description="Article content")
    url: str = Field(..., max_length=1000, description="Article URL")
```

### Configuration
- Use `Config` class for model configuration
- Use `from_attributes = True` for SQLAlchemy model conversion

**Example**:
```python
class ArticleResponse(BaseModel):
    id: int
    title: str
    ...
    
    class Config:
        from_attributes = True
```

## Error Handling

### Custom Exceptions
- Use custom exceptions from `shared.exceptions`
- Inherit from appropriate base exception

**Example**:
```python
from ...shared.exceptions import ServiceException, ValidationException

try:
    result = usecase.create_article(data)
except ValidationException as e:
    raise HTTPException(status_code=400, detail=str(e))
except ServiceException as e:
    raise HTTPException(status_code=500, detail=str(e))
```

### HTTP Exceptions
- Use FastAPI's `HTTPException`
- Provide meaningful error messages
- Use appropriate status codes

**Status Codes**:
- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `202 Accepted` - Async operation started
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Logging

### Structured Logging
- Use `structlog` for structured logging
- Use `get_logger()` from `core.logging`
- Include context in log messages

**Example**:
```python
from ...core.logging import get_logger

logger = get_logger(__name__)

logger.info(
    "article_created",
    article_id=article.id,
    source_name=article.source_name,
    url=article.url
)
```

### Log Levels
- `DEBUG` - Detailed debugging information
- `INFO` - General informational messages
- `WARNING` - Warning messages
- `ERROR` - Error messages
- `CRITICAL` - Critical errors

## Database Patterns

### SQLAlchemy Models
- Inherit from `Base` (from `dbase.sql.core.base`)
- Use type hints for columns
- Define indexes in table definition

**Example**:
```python
from sqlalchemy import Column, Integer, String, DateTime
from ..core.base import Base

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    ...
```

### Database Sessions
- Use dependency injection: `db: Session = Depends(get_db_session)`
- Create session per request
- Close session automatically (FastAPI handles it)

**Example**:
```python
from ...dbase.sql.core.session import get_db_session

@router.get("/articles")
async def list_articles(db: Session = Depends(get_db_session)):
    articles = db.query(Article).all()
    return articles
```

## Testing Patterns

### Test Structure
```
tests/
├── unit/              # Unit tests
├── integration/        # Integration tests
└── e2e/               # End-to-end tests
```

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

**Example**:
```python
import pytest

class TestArticleRepository:
    def test_find_by_id(self):
        """Test finding article by ID."""
        ...
```

### Fixtures
- Use pytest fixtures for test setup
- Mock external dependencies
- Use database fixtures for integration tests

## Documentation

### Docstrings
- Use Google-style docstrings
- Document all public functions and classes
- Include parameter and return type descriptions

**Example**:
```python
def get_article(article_id: int, db: Session) -> Optional[Article]:
    """
    Get article by ID.
    
    Args:
        article_id: Article ID
        db: Database session
    
    Returns:
        Article object or None if not found
    """
    ...
```

### Type Hints as Documentation
- Use type hints for inline documentation
- Pydantic models serve as API documentation
- FastAPI auto-generates OpenAPI docs from type hints

## Related Documentation

- **PEP 8**: https://pep8.org/
- **Black**: https://black.readthedocs.io/
- **isort**: https://pycqa.github.io/isort/
- **Pydantic**: https://docs.pydantic.dev/
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/

