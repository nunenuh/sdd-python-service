---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Module Structure Conventions

Complete guide for organizing feature modules within `src/fastapi_service/modules/`.

**Source**: Actual codebase patterns and architectural decisions

## Overview

Modules are groups of related features. Each module follows a consistent layered architecture pattern:

```
Handler (HTTP) → UseCase (Orchestration) → Service (Business Logic) → Repository (Data Access) → Database
```

## Module Naming

- **Use singular nouns**: `article`, `crawler`, `source`, `health`
- **Maximum 2 words**: `crawl_log`, `user_profile` (if needed)
- **Lowercase with underscores**: `news_source`, not `NewsSource` or `news-source`
- **Descriptive**: Name should clearly indicate the module's purpose

**Examples**:
- ✅ `articles` - Managing news articles
- ✅ `crawler` - Web crawling functionality
- ✅ `sources` - News source management
- ✅ `health` - Health monitoring
- ❌ `article` - Use plural for collections
- ❌ `crawler_module` - Redundant suffix
- ❌ `NewsSource` - Wrong case

## Required Components

Every module **MUST** have these components:

### 1. `__init__.py`

Module initialization file with module docstring.

**Example**:
```python
"""
Articles module for managing news articles.
"""
```

**Location**: `src/fastapi_service/modules/{module_name}/__init__.py`

### 2. `apiv1/handler.py`

HTTP request/response handlers (FastAPI routes).

**Responsibilities**:
- Define API endpoints
- Handle HTTP request/response
- Validate input via Pydantic schemas
- Call use cases
- Handle HTTP exceptions
- Return appropriate HTTP status codes

**Structure**:
```python
"""
{Module} API endpoints.

This module provides HTTP endpoints for {module} management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.logging import get_logger
from ...dbase.sql.core.session import get_db_session
from ...shared.exceptions import ServiceException, ValidationException
from ..schemas import {Module}Create, {Module}Response, {Module}Update
from ..usecase import {Module}UseCase

logger = get_logger(__name__)
router = APIRouter()


@router.post("/", response_model={Module}Response, status_code=status.HTTP_201_CREATED)
async def create_{module}(
    {module}_data: {Module}Create,
    db: Session = Depends(get_db_session),
):
    """Create a new {module}."""
    try:
        usecase = {Module}UseCase(db=db)
        result = usecase.create_{module}({module}_data, db=db)
        return result
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ServiceException as e:
        logger.error(f"Failed to create {module}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
```

**Location**: `src/fastapi_service/modules/{module_name}/apiv1/handler.py`

**Note**: Also create `apiv1/__init__.py`:
```python
"""{Module} API v1 handlers."""
```

### 3. `schemas.py`

Pydantic models for request/response validation and serialization.

**Responsibilities**:
- Define request schemas (Create, Update)
- Define response schemas (Response, ListResponse)
- Define base schemas with common fields
- Validate data types and constraints

**Structure**:
```python
"""
{Module} schemas for request/response models.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class {Module}Base(BaseModel):
    """Base {module} schema with common fields."""

    field1: str = Field(..., description="Field description", max_length=100)
    field2: Optional[int] = Field(None, description="Optional field")


class {Module}Create({Module}Base):
    """Schema for creating a new {module}."""

    pass


class {Module}Update(BaseModel):
    """Schema for updating an existing {module}."""

    field1: Optional[str] = Field(None, description="Field description")
    field2: Optional[int] = Field(None, description="Optional field")


class {Module}Response({Module}Base):
    """Schema for {module} response."""

    id: int = Field(..., description="{Module} ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Update timestamp")

    class Config:
        from_attributes = True


class {Module}ListResponse(BaseModel):
    """Schema for {module} list response."""

    items: List[{Module}Response] = Field(..., description="List of {modules}")
    total: int = Field(..., description="Total count")
    skip: int = Field(..., description="Pagination offset")
    limit: int = Field(..., description="Pagination limit")
```

**Location**: `src/fastapi_service/modules/{module_name}/schemas.py`

### 4. `usecase.py`

Use case orchestration layer.

**Responsibilities**:
- Orchestrate business logic workflows
- Coordinate between multiple services
- Handle transaction management
- Provide high-level operations
- Bridge between handlers and services

**Structure**:
```python
"""
{Module} use case orchestration layer.
"""

from typing import Optional

from sqlalchemy.orm import Session

from ...dbase.sql.core.session import get_db_session
from ...shared.exceptions import ServiceException
from .schemas import {Module}Create, {Module}Update
from .services import {Module}Service


class {Module}UseCase:
    """Use case for orchestrating {module} operations."""

    def __init__(self, db: Optional[Session] = None):
        """Initialize {module} use case.

        Args:
            db: Optional database session. If not provided, will use dependency injection.
        """
        self.db = db

    def _get_service(self, db: Session) -> {Module}Service:
        """Get {module} service instance.

        Args:
            db: Database session

        Returns:
            {Module}Service instance
        """
        return {Module}Service(db)

    def create_{module}(
        self, {module}_data: {Module}Create, db: Optional[Session] = None
    ) -> dict:
        """Create a new {module}.

        Args:
            {module}_data: {Module} creation data
            db: Optional database session

        Returns:
            Dictionary with created {module} data

        Raises:
            ServiceException: If creation fails
        """
        db_session = db or next(get_db_session())
        try:
            service = self._get_service(db_session)
            return service.create_{module}({module}_data)
        except Exception as e:
            raise ServiceException(f"Failed to create {module}: {str(e)}")
```

**Location**: `src/fastapi_service/modules/{module_name}/usecase.py`

**Note**: Even simple modules like `health` should have a use case layer for consistency.

## Conditional Components

Add these components only when needed:

### 5. `repositories.py` (Conditional)

Data access layer for SQLAlchemy models.

**When to create**:
- ✅ Module needs to access database
- ✅ Module uses SQLAlchemy models
- ❌ Module has no database operations

**Responsibilities**:
- CRUD operations on database models
- Query building and filtering
- Database transaction management
- Data mapping between models and dictionaries

**Structure**:
```python
"""
{Module} repository for data access operations.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ...dbase.sql.models.{module} import {Module}Model
from ...shared.exceptions import RepositoryException


class {Module}Repository:
    """Repository for {module} data access."""

    def __init__(self, db: Session):
        """Initialize {module} repository.

        Args:
            db: Database session
        """
        self.db = db

    def create(self, {module}_data: dict) -> {Module}Model:
        """Create a new {module}.

        Args:
            {module}_data: {Module} data dictionary

        Returns:
            Created {Module}Model instance

        Raises:
            RepositoryException: If creation fails
        """
        try:
            {module} = {Module}Model(**{module}_data)
            self.db.add({module})
            self.db.commit()
            self.db.refresh({module})
            return {module}
        except Exception as e:
            self.db.rollback()
            raise RepositoryException(f"Failed to create {module}: {str(e)}")

    def get_by_id(self, {module}_id: int) -> Optional[{Module}Model]:
        """Get {module} by ID.

        Args:
            {module}_id: {Module} ID

        Returns:
            {Module}Model instance or None if not found
        """
        return self.db.query({Module}Model).filter({Module}Model.id == {module}_id).first()
```

**Location**: `src/fastapi_service/modules/{module_name}/repositories.py`

**Note**: Only create if module needs database access. Modules like `health` that don't use database models should not have this file.

### 6. `services.py` (Conditional)

Business logic layer.

**When to create**:
- ✅ Module has business logic beyond simple CRUD
- ✅ Module needs validation or transformation logic
- ✅ Module coordinates between repositories
- ❌ Module is purely CRUD (can use repository directly in use case)

**Responsibilities**:
- Business rule validation
- Data transformation and enrichment
- Complex business operations
- Coordination between repositories
- Error handling and exception translation

**Structure**:
```python
"""
{Module} business logic services.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from ...shared.exceptions import ServiceException, ValidationException
from .repositories import {Module}Repository
from .schemas import {Module}Create, {Module}Update


class {Module}Service:
    """Service for {module} business logic."""

    def __init__(self, db: Session):
        """Initialize {module} service.

        Args:
            db: Database session
        """
        self.repository = {Module}Repository(db)

    def create_{module}(self, {module}_data: {Module}Create) -> dict:
        """Create a new {module}.

        Args:
            {module}_data: {Module} creation data

        Returns:
            Dictionary with created {module} data

        Raises:
            ValidationException: If {module} data is invalid
            ServiceException: If creation fails
        """
        # Business logic validation
        existing = self.repository.get_by_field({module}_data.field)
        if existing:
            raise ValidationException(f"{Module} with field '{field}' already exists")

        try:
            {module} = self.repository.create({module}_data.model_dump())
            return {
                "id": {module}.id,
                "field1": {module}.field1,
            }
        except Exception as e:
            raise ServiceException(f"Failed to create {module}: {str(e)}")
```

**Location**: `src/fastapi_service/modules/{module_name}/services.py`

**Note**: If multiple services are needed, create a `services/` package:
```
services/
  __init__.py
  main_service.py
  helper_service.py
```

### 7. `tasks.py` (Conditional)

Celery tasks for asynchronous/background processing.

**When to create**:
- ✅ Module needs Celery tasks
- ✅ Module has background jobs
- ✅ Module needs async processing
- ❌ Module has no background processing needs

**Responsibilities**:
- Define Celery tasks
- Handle task execution
- Manage task state and retries
- Coordinate with use cases/services

**Structure**:
```python
"""
Celery tasks for {module} module.

This module defines Celery tasks for {module} operations.
"""

from typing import Any, Dict

from ...core.logging import get_logger
from ...dbase.sql.core.session import SessionLocal
from ...worker import app
from .usecase import {Module}UseCase

logger = get_logger(__name__)


@app.task(name="fastapi_service.modules.{module}.tasks.{task_name}", bind=True)
def {task_name}(
    self, param1: str, param2: int = None
) -> Dict[str, Any]:
    """
    Celery task to {task description}.

    Args:
        param1: Parameter description
        param2: Optional parameter description

    Returns:
        Dictionary with task results
    """
    logger.info(
        "{task_name}_started",
        param1=param1,
        param2=param2,
    )

    db_session = SessionLocal()
    try:
        usecase = {Module}UseCase(db=db_session)
        result = usecase.{operation}(param1, param2)
        return result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise
    finally:
        db_session.close()
```

**Location**: `src/fastapi_service/modules/{module_name}/tasks.py`

**Note**: Only create if module needs Celery tasks. Most modules don't need this.

## Module Structure Examples

### Simple Module (No Database)

**Example**: `health` module

```
health/
├── __init__.py
├── apiv1/
│   ├── __init__.py
│   └── handler.py
├── schemas.py
├── services.py      # No repository needed
└── usecase.py       # Still required for consistency
```

### Standard Module (With Database)

**Example**: `articles` module

```
articles/
├── __init__.py
├── apiv1/
│   ├── __init__.py
│   └── handler.py
├── schemas.py
├── repositories.py  # Database access
├── services.py      # Business logic
└── usecase.py       # Orchestration
```

### Complex Module (With Tasks)

**Example**: `crawler` module

```
crawler/
├── __init__.py
├── apiv1/
│   ├── __init__.py
│   └── handler.py
├── schemas.py
├── repositories.py
├── services.py
├── usecase.py
├── tasks.py         # Celery tasks
└── scrapy/          # Special subdirectory for Scrapy integration
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        ├── __init__.py
        ├── base.py
        └── kompas.py
```

## Special Cases

### Subdirectories

Modules can have subdirectories for specific integrations or complex features:

- `crawler/scrapy/` - Scrapy integration
- `articles/search/` - Search-specific functionality
- `sources/config/` - Source configuration management

**Guidelines**:
- Use subdirectories for clearly separated concerns
- Keep subdirectory structure consistent
- Document subdirectory purpose in module `__init__.py`

### Multiple Services

If a module needs multiple services, create a `services/` package:

```
services/
├── __init__.py          # Export main services
├── main_service.py      # Primary service
└── helper_service.py    # Supporting service
```

**Example**:
```python
# services/__init__.py
from .main_service import MainService
from .helper_service import HelperService

__all__ = ["MainService", "HelperService"]
```

## Import Patterns

### Within Module

```python
# handler.py
from ..schemas import ArticleCreate, ArticleResponse
from ..usecase import ArticleUseCase

# usecase.py
from .services import ArticleService
from .schemas import ArticleCreate

# services.py
from .repositories import ArticleRepository
from .schemas import ArticleCreate
```

### From Other Modules

```python
# Use absolute imports from package root
from ...dbase.sql.core.session import get_db_session
from ...shared.exceptions import ServiceException
from ...core.logging import get_logger
```

### From Other Modules (Cross-Module)

```python
# Use full module path
from ...modules.articles.schemas import ArticleResponse
from ...modules.sources.services import SourceService
```

## File Organization Checklist

When creating a new module, ensure:

- [ ] Module name follows naming conventions (singular, lowercase, max 2 words)
- [ ] `__init__.py` exists with module docstring
- [ ] `apiv1/handler.py` exists with API endpoints
- [ ] `apiv1/__init__.py` exists
- [ ] `schemas.py` exists with Pydantic models
- [ ] `usecase.py` exists (always required)
- [ ] `repositories.py` exists (only if database access needed)
- [ ] `services.py` exists (only if business logic needed)
- [ ] `tasks.py` exists (only if Celery tasks needed)
- [ ] All imports use relative imports within module
- [ ] All imports use absolute imports for external modules

## Best Practices

1. **Keep handlers thin**: Handlers should only handle HTTP concerns, delegate to use cases
2. **Use cases orchestrate**: Use cases coordinate between services and repositories
3. **Services contain business logic**: Business rules and validation go in services
4. **Repositories handle data access**: Database operations only in repositories
5. **Schemas validate**: Use Pydantic schemas for all input/output validation
6. **Consistent error handling**: Use shared exceptions from `shared.exceptions`
7. **Type hints everywhere**: All functions should have type hints
8. **Documentation**: All public functions should have docstrings

## Related Documentation

- [Python Conventions](./01-python-conventions.md) - General Python coding standards
- [API Design](./02-api-design.md) - API endpoint design patterns
- [Testing Standards](./04-testing-standards.md) - Testing module components

