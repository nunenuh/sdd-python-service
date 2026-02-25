# CLAUDE.md — AI Assistant Guide for sdd-python-service

This file provides comprehensive guidance for AI assistants (Claude, Cursor, etc.) working in this codebase.

## Project Overview

**FastAPI Service Boilerplate** — a production-ready Python microservice template built with clean architecture. The stack:

- **Framework**: FastAPI 0.115+ with Uvicorn
- **Database**: PostgreSQL 15 via SQLAlchemy 2.0 + Alembic migrations
- **Cache/Queue**: Redis 7 + Celery (async task worker)
- **Search**: Meilisearch v1.7
- **Logging**: structlog (structured/JSON logging)
- **CLI**: Typer + Rich
- **Python**: 3.11+ | **Dependency Management**: Poetry

---

## Repository Structure

```
sdd-python-service/
├── src/fastapi_service/         # Main application package
│   ├── main.py                  # FastAPI app creation and entry point
│   ├── router.py                # Main API router (aggregates all modules)
│   ├── core/                    # Cross-cutting concerns
│   │   ├── config.py            # Pydantic Settings (env vars, DB URLs, Redis URLs)
│   │   ├── auth.py              # X-API-Key header authentication
│   │   ├── logging.py           # Structured logging setup
│   │   └── dependencies.py      # FastAPI dependency injection helpers
│   ├── modules/                 # Feature modules (one per domain)
│   │   ├── health/              # Health check endpoints (/api/v1/health)
│   │   ├── weather/             # Weather data via Open-Meteo (/api/v1/weather)
│   │   ├── quotes/              # Quotes data (/api/v1/quotes)
│   │   └── countries/           # Countries data (/api/v1/countries)
│   ├── dbase/sql/               # Database layer
│   │   ├── core/session.py      # SQLAlchemy engine, session factory
│   │   ├── core/base.py         # Declarative base for ORM models
│   │   └── models/              # SQLAlchemy ORM model definitions
│   └── shared/                  # Shared utilities
│       ├── exceptions.py        # Custom exception hierarchy
│       ├── services/            # Shared services (redis_service, article_extractor)
│       └── utils/               # Utilities (url_utils, text_utils, date_utils)
├── tests/
│   ├── unit/                    # Unit tests (mock all external deps)
│   ├── integration/             # API endpoint tests with real deps
│   └── e2e/                     # Full workflow tests
├── docker/
│   ├── docker-compose.dev.yml   # Development stack (with hot-reload)
│   ├── docker-compose.run.yml   # Production stack
│   ├── docker-compose.build.yml # Image build configuration
│   └── images/                  # Dockerfiles (base, prd, stg)
├── alembic/                     # Database migration scripts
├── specs/                       # AI-readable specifications and conventions
│   └── conventions/             # Coding standards, module structure, API design
├── docs/                        # Human-readable documentation
├── pyproject.toml               # Project config, dependencies, tool settings
├── Makefile                     # All development commands
└── env.example                  # Environment variable template
```

---

## Architecture: Layered Pattern

Every feature module follows this strict layered pattern:

```
HTTP Request
    ↓
Handler (apiv1/handler.py)   — HTTP only: routing, request parsing, response serialization
    ↓
UseCase (usecase.py)          — Orchestration: coordinates services, manages transactions
    ↓
Service (services.py)         — Business logic: domain rules, validation, transformations
    ↓
Repository (repositories.py) — Data access: CRUD operations, query building (if DB needed)
    ↓
Database / External API
```

**Rules:**
- Handlers must be thin — only HTTP concerns, delegate immediately to use cases
- Use cases orchestrate but do not contain business logic
- Services contain all domain logic
- Repositories are the only place that touches the database
- Use `shared/exceptions.py` exceptions at all layers

---

## Module Structure

Every feature module lives under `src/fastapi_service/modules/{module_name}/` and follows this layout:

```
{module_name}/
├── __init__.py              # Module docstring only
├── apiv1/
│   ├── __init__.py          # "{Module} API v1 handlers."
│   └── handler.py           # FastAPI routes
├── schemas.py               # Pydantic request/response models
├── usecase.py               # Orchestration layer (always required)
├── services.py              # Business logic (required unless purely CRUD)
├── repositories.py          # DB access (only if module uses database)
├── tasks.py                 # Celery tasks (only if async processing needed)
└── cli/
    ├── __init__.py
    └── commands.py          # Typer CLI commands (optional)
```

### Module Naming
- Plural nouns: `quotes`, `countries`, `articles`
- Lowercase with underscores: `news_sources`
- Never: `ArticleModule`, `article-module`

### Adding a New Module Checklist
- [ ] Create directory under `src/fastapi_service/modules/`
- [ ] Add `__init__.py` with module docstring
- [ ] Create `apiv1/__init__.py` and `apiv1/handler.py`
- [ ] Create `schemas.py`, `usecase.py`
- [ ] Add `services.py` if business logic exists
- [ ] Add `repositories.py` only if database access needed
- [ ] Register router in `src/fastapi_service/router.py`

---

## Key Code Patterns

### Handler Pattern
```python
from fastapi import APIRouter, HTTPException, Query
from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException
from ..schemas import MyResponse
from ..usecase import MyUseCase

logger = get_logger(__name__)
router = APIRouter()

@router.get("/", response_model=MyResponse)
async def get_items(limit: int = Query(20, ge=1, le=150)):
    """Get items."""
    usecase = MyUseCase()
    try:
        result = await usecase.get_items(limit=limit)
        return MyResponse(items=result)
    except ServiceException as e:
        logger.error(f"Service error: {str(e)}")
        raise HTTPException(status_code=503, detail={"error": "service_error", "message": str(e)})
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail={"error": "internal_error", "message": "Unexpected error"})
```

### UseCase Pattern
```python
class MyUseCase:
    def __init__(self):
        self.service = get_my_service()

    async def get_items(self, limit: int) -> List[MyModel]:
        return await self.service.fetch_items(limit=limit)
```

### Service Pattern
```python
class MyService:
    async def fetch_items(self, limit: int) -> List[MyModel]:
        # Business logic here
        ...
```

### Repository Pattern (when using DB)
```python
class MyRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, item_id: int) -> Optional[MyModel]:
        return self.db.query(MyModel).filter(MyModel.id == item_id).first()
```

### Exception Handling
Use the shared exception hierarchy from `shared/exceptions.py`:
```python
from fastapi_service.shared.exceptions import (
    ServiceException,       # Service-level errors
    ValidationException,    # Validation failures
    RepositoryException,    # Database/data access errors
    CrawlerException,       # Crawler-specific errors
)
```

Map exceptions in handlers:
- `ValidationException` → HTTP 400
- `NotFoundException` → HTTP 404
- `ServiceException` → HTTP 503
- Generic `Exception` → HTTP 500

---

## Code Style & Conventions

### Formatting
- **Black**: line length 88, target Python 3.11
- **isort**: profile `black`, multi-line output 3
- **Flake8**: linting
- Run: `make format` (auto-fix) or `make lint-all` (check only)

### Type Hints
Required on all function signatures:
```python
from typing import List, Optional, Dict, Tuple

async def search_items(
    query: Optional[str] = None,
    limit: int = 20,
) -> Tuple[List[Item], int]:
    ...
```

### Async/Await
- Use `async def` for all FastAPI route handlers
- Use `async def` for any I/O operations (HTTP, DB, Redis)
- Synchronous code only for CPU-bound pure functions

### Imports
Group in order: stdlib → third-party → local. Use relative imports within a module:
```python
# stdlib
from datetime import UTC, datetime
from typing import List, Optional

# third-party
from fastapi import APIRouter, HTTPException

# local (relative within module)
from ..schemas import MyResponse
from ..usecase import MyUseCase

# local (absolute for cross-module or core)
from fastapi_service.core.logging import get_logger
from fastapi_service.shared.exceptions import ServiceException
```

### Naming
| Category | Convention | Example |
|---|---|---|
| Modules/files | `snake_case` | `article_handler.py` |
| Classes | `PascalCase` | `ArticleService` |
| Functions/methods | `snake_case` | `get_article()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Boolean vars | `is_` / `has_` prefix | `is_enabled`, `has_error` |
| Private methods | `_` prefix | `_build_query()` |

### Docstrings
Use Google-style docstrings for all public functions and classes:
```python
def get_article(article_id: int, db: Session) -> Optional[Article]:
    """Get article by ID.

    Args:
        article_id: The article's unique identifier.
        db: Database session.

    Returns:
        Article object or None if not found.

    Raises:
        ServiceException: If the database query fails.
    """
```

### Logging
```python
from fastapi_service.core.logging import get_logger

logger = get_logger(__name__)

logger.info("item_created", item_id=item.id, name=item.name)
logger.error(f"Failed to process item: {str(e)}")
```

---

## API Design Standards

### URL Structure
All endpoints are prefixed with `/api/v1/`:
```
GET    /api/v1/{resource}           # List/search
POST   /api/v1/{resource}           # Create
GET    /api/v1/{resource}/{id}      # Get single
PUT    /api/v1/{resource}/{id}      # Update
DELETE /api/v1/{resource}/{id}      # Delete
GET    /api/v1/{resource}/random    # Special action (before {id} route)
```

### HTTP Status Codes
- `200 OK` — GET, PUT success
- `201 Created` — POST success
- `202 Accepted` — async operation started
- `204 No Content` — DELETE success
- `400 Bad Request` — validation/malformed request
- `403 Forbidden` — invalid/missing API key
- `404 Not Found` — resource not found
- `409 Conflict` — duplicate resource
- `503 Service Unavailable` — upstream service failure
- `500 Internal Server Error` — unexpected server error

### Pagination
Use `skip` and `limit` query parameters. Response includes `count`, `total_count`, and `page`:
```json
{
  "items": [...],
  "count": 20,
  "total_count": 500,
  "page": 1,
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Authentication
Optional `X-API-Key` header authentication. Protected endpoints use:
```python
from fastapi import Depends
from fastapi_service.core.auth import get_api_key

@router.get("/protected", dependencies=[Depends(get_api_key)])
async def protected_endpoint():
    ...
```

---

## Configuration & Environment

### Settings Access
Use the cached settings singleton — never instantiate `Settings()` directly:
```python
from fastapi_service.core.config import get_settings

settings = get_settings()
db_url = settings.database_url
redis_url = settings.redis_url
```

### Environment Variables (copy `env.example` to `.env`)

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `"FastAPI Service"` | Application name |
| `APP_ENVIRONMENT` | `"development"` | `development`/`staging`/`production` |
| `APP_HOST` | `"0.0.0.0"` | Server host |
| `APP_PORT` | `8080` | Server port |
| `APP_DEBUG` | `false` | Enable debug mode |
| `APP_X_API_KEY` | `"changeme"` | API key for protected routes |
| `ALLOWED_ORIGINS_STR` | `"*"` | CORS allowed origins (comma-separated) |
| `DB_HOST` | `"localhost"` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `"fastapi_service"` | Database name |
| `DB_USER` | `"postgres"` | DB username |
| `DB_PASSWORD` | `"postgres"` | DB password |
| `REDIS_HOST` | `"localhost"` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `QUOTES_VERIFY_SSL` | `false` | SSL verification for quotes API |

**Important**: Docs/ReDoc are only exposed in `development`, `local`, and `staging` environments.

---

## Development Workflow

### Initial Setup
```bash
make install          # Install deps + pre-commit hooks
cp env.example .env   # Create .env (edit as needed)
```

### Running Locally
```bash
make run              # Start server (production mode, port 8080)
make dev              # Start with auto-reload (development mode)
```

### Testing
```bash
make test                    # Run all tests
make test-unit               # Unit tests only (tests/unit/)
make test-integration        # Integration tests (tests/integration/)
make test-e2e                # End-to-end tests (tests/e2e/)
make test-coverage           # All tests with HTML coverage report
make test-coverage-unit      # Unit tests with coverage
```

Run specific tests:
```bash
poetry run pytest tests/unit/test_articles.py::test_create_article -v
```

### Code Quality
```bash
make format           # Auto-format: black + isort
make lint-all         # Run all pre-commit checks (black, isort, flake8)
make clean            # Remove __pycache__, .pyc, htmlcov, dist, etc.
```

### Database Migrations
```bash
make db-upgrade       # Apply all pending migrations
make db-migrate       # Generate new migration (prompts for message)
make db-downgrade     # Rollback last migration
make db-current       # Show current schema revision
make db-history       # Show migration history
```

### Docker Development
```bash
make docker-dev           # Start full dev stack (API + PostgreSQL + Redis + Meilisearch + Celery)
make docker-logs-dev      # Tail development logs
make docker-dev-restart   # Restart dev stack
make docker-stop          # Stop all services
```

### Docker Production
```bash
make docker-base-build    # Build base image (do this first)
make docker-build         # Build service image (SERVICE=api-local|api-staging|api-main)
make docker-run           # Start production stack
make docker-logs          # Tail production logs
make docker-restart       # Restart production stack
```

---

## Testing Standards

### Test Organization (Arrange-Act-Assert)
```python
class TestMyService:
    def test_create_item_succeeds(self):
        """Test successful item creation."""
        # Arrange
        service = MyService(mock_db)
        item_data = ItemCreate(name="Test", value=42)

        # Act
        result = service.create_item(item_data)

        # Assert
        assert result["id"] is not None
        assert result["name"] == "Test"

    def test_create_item_raises_on_duplicate(self):
        """Test that duplicate items raise ValidationException."""
        ...
```

### Test Types
- **Unit tests** (`tests/unit/`): No I/O, mock all external dependencies, < 1ms each
- **Integration tests** (`tests/integration/`): Test full API endpoints with TestClient
- **E2E tests** (`tests/e2e/`): Complete workflow tests

### Common Fixtures
```python
import pytest
from fastapi.testclient import TestClient
from fastapi_service.main import app

@pytest.fixture
def client():
    return TestClient(app)
```

### Coverage Targets
- Overall: ≥ 80%
- Business logic (services): ≥ 90%
- Critical paths: 100%

### Pytest Markers
```python
@pytest.mark.unit
def test_something(): ...

@pytest.mark.integration
def test_api_endpoint(): ...

@pytest.mark.slow
def test_heavy_operation(): ...
```

---

## Git Workflow

### Branch Naming (Mandatory)
```
<type>/issue-<number>-<short-description>
```
Examples:
- `feature/issue-123-add-quotes-module`
- `fix/issue-456-handle-redis-timeout`
- `docs/issue-789-update-readme`

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

Closes #<issue-number>
```

Commit types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`

Examples:
```
feat(quotes): add quotes module with Quotable API integration

Closes #42
```

```
fix(config): remove unused HTTP_VERIFY_SSL setting

Refs #55
```

### Pre-commit Checks
Pre-commit hooks run automatically on commit: black, isort, flake8. Set up with `make install`.

---

## Pydantic Schemas

All request/response models go in `schemas.py`. Use Pydantic v2 patterns:

```python
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

class ItemBase(BaseModel):
    name: str = Field(..., max_length=255, description="Item name")
    value: Optional[int] = Field(None, description="Item value", ge=0)

class ItemCreate(ItemBase):
    """Schema for creating a new item."""
    pass

class ItemResponse(ItemBase):
    """Schema for item response."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ItemListResponse(BaseModel):
    """Schema for paginated item list."""
    items: List[ItemResponse]
    count: int
    total_count: int
    page: int
    timestamp: datetime
```

---

## Database Models

SQLAlchemy 2.0 style — inherit from `Base`:

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from fastapi_service.dbase.sql.core.base import Base

class MyModel(Base):
    __tablename__ = "my_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

After adding a new model, generate a migration:
```bash
make db-migrate   # prompts for migration message
make db-upgrade   # apply the migration
```

---

## Current API Endpoints

| Module | Prefix | Endpoints |
|---|---|---|
| Health | `/api/v1/health` | `GET /ping`, `GET /status`, `GET /detailed` |
| Quotes | `/api/v1/quotes` | `GET /`, `GET /random`, `GET /{id}`, `GET /author/{slug}` |
| Weather | `/api/v1/weather` | `GET /current`, `GET /forecast`, `GET /daily` |
| Countries | `/api/v1/countries` | `GET /`, `GET /{name}`, `GET /code/{code}`, `GET /region/{region}` |

Interactive API docs (dev/staging only): `http://localhost:8080/docs`

---

## Shared Utilities

### Logging
```python
from fastapi_service.core.logging import get_logger
logger = get_logger(__name__)
```

### Redis Service
```python
from fastapi_service.shared.services.redis_service import get_redis_client
redis = get_redis_client()
```

### Utilities
```python
from fastapi_service.shared.utils.url_utils import normalize_url
from fastapi_service.shared.utils.text_utils import clean_text
from fastapi_service.shared.utils.date_utils import parse_date
```

---

## Documentation Structure

When adding documentation:
- Architecture changes → `docs/architecture/`
- Implementation guides → `docs/implementation/`
- Deployment procedures → `docs/deployment/`
- Known issues → `docs/issues/`
- Development setup → `docs/development/`
- Testing guides → `docs/testing/`
- Troubleshooting → `docs/troubleshooting/`

Specifications for AI code generation → `specs/`

---

## Common Pitfalls

1. **Route ordering**: Define specific routes (e.g., `/random`) before parameterized routes (e.g., `/{id}`) in the same router to avoid shadowing.

2. **Settings caching**: `get_settings()` uses `@lru_cache`. Call `get_settings.cache_clear()` in tests when overriding env vars.

3. **Async database**: Use async SQLAlchemy patterns with `async with AsyncSession` for async routes — or use sync sessions carefully with `Depends(get_db_session)`.

4. **Circular imports**: Keep cross-module imports using absolute paths (`from fastapi_service.modules.x import ...`), never relative cross-module.

5. **Exception mapping**: Always catch `ServiceException` separately from generic `Exception` in handlers — the former maps to 503, the latter to 500.

6. **Alembic URL**: The `alembic.ini` placeholder URL (`driver://user:pass@localhost/dbname`) is overridden at runtime by `alembic/env.py` reading from `get_settings().database_url`.
