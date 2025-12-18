---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Repository Overview

## Purpose

`fastapi-service` is a production-ready FastAPI boilerplate for building modern Python web services. It provides a solid foundation with PostgreSQL for data storage, Redis for caching, structured logging, and best practices for API development.

## Tech Stack

- **Runtime**: Python 3.11+
- **Framework**: FastAPI with Uvicorn
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0+
- **Cache**: Redis 7+
- **Dependency Management**: Poetry
- **Migrations**: Alembic
- **Logging**: structlog

## Architecture

The project follows clean architecture principles with clear separation of concerns:

```
src/fastapi_service/
├── core/                   # Core functionality
│   ├── config.py          # Configuration (Pydantic Settings)
│   ├── logging.py         # Structured logging setup
│   ├── auth.py            # Authentication (if implemented)
│   └── dependencies.py    # FastAPI dependencies
├── modules/                # Feature modules
│   ├── health/            # Health check endpoints
│   │   ├── apiv1/         # API handlers (HTTP layer)
│   │   ├── services.py    # Business logic services
│   │   ├── usecase.py     # Use case orchestration
│   │   └── schemas.py     # Pydantic models
│   └── <your-module>/     # Your feature modules
│       ├── apiv1/         # API handlers
│       ├── usecase.py     # Use case orchestration
│       ├── services.py    # Business logic
│       ├── repositories.py  # Data access (if needed)
│       ├── schemas.py     # Pydantic models
│       └── tasks.py       # Celery tasks (if needed)
├── dbase/                 # Database layer
│   └── sql/               # SQLAlchemy (PostgreSQL)
│       ├── models/        # SQLAlchemy models
│       ├── core/          # Database core (session, base)
│       └── services/      # Database services
├── shared/                # Shared utilities
│   ├── exceptions.py      # Custom exceptions
│   ├── services/          # Shared services
│   └── utils/             # Utility functions
├── main.py                # FastAPI application entry point
├── router.py              # Main API router
└── worker.py              # Celery worker configuration
```

## Key Patterns

1. **Layered Architecture**: Handler → UseCase → Service/Repository → Database
2. **Dependency Injection**: FastAPI dependencies for database sessions
3. **Repository Pattern**: Data access abstraction
4. **Use Case Pattern**: Business logic orchestration
5. **DTO Pattern**: Pydantic models for request/response validation
6. **Decorator Pattern**: FastAPI route decorators

## Entry Point

- **Main file**: `src/fastapi_service/main.py` - Creates FastAPI app, sets up middleware, includes routers

## Environment Variables

Configuration managed via `src/fastapi_service/core/config.py` using Pydantic Settings. See `env.example` for complete reference.

**Prefixes**:
- `APP_*` - Application settings
- `DB_*` - Database settings
- `REDIS_*` - Redis settings
- `MEILISEARCH_*` - Meilisearch settings
- `SCRAPY_*` - Scrapy settings
- `CRAWLER_*` - Crawler settings
- `CELERY_*` - Celery settings

## Database

- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic (`alembic/versions/`)
- **Models**: `src/fastapi_service/dbase/sql/models/`
- **Session**: `src/fastapi_service/dbase/sql/core/session.py`

## API Structure

- **Base Path**: `/api`
- **Version**: `v1`
- **Full Base Path**: `/api/v1`
- **Documentation**: Swagger UI available at `/docs` (development/staging only)
- **Modules**:
  - `/api/v1/health` - Health check endpoints
  - `/api/v1/articles` - Article management
  - `/api/v1/crawler` - Crawler control
  - `/api/v1/sources` - Source management

## Development Workflow

1. **Local Development**: `make dev` (uses `uvicorn` with auto-reload)
2. **Database**: `make db-migrate` (runs Alembic migrations)
3. **Testing**: `make test` (runs pytest)
4. **Linting**: `make lint-all` (runs flake8, mypy, etc.)
5. **Formatting**: `make format` (runs black + isort)

## Docker Development

- **Base Image**: `nunenuh/fastapi-service-base:latest`
- **Service Images**: `nunenuh/fastapi-service:{version}-{branch}`
- **Development**: `make docker-dev` (Docker Compose)
- **Production**: `make docker-run` (Docker Compose)

## Documentation Structure

All documentation is organized in `docs/`:
- `docs/api/` - API documentation
- `docs/architecture/` - System architecture and design
- `docs/implementation/` - Developer guides
- `docs/deployment/` - Deployment and operations
- `docs/planning/` - Project planning documents
- `docs/testing/` - Testing documentation
- See `docs/README.md` for complete index

## Specifications (Spec-Driven Development)

Specifications are maintained in `specs/` directory:
- `specs/api/` - API specifications
- `specs/schemas/` - Database and data schemas
- `specs/contracts/` - API contracts
- `specs/conventions/` - Coding conventions
- `specs/features/` - Feature specifications
- See `specs/README.md` for spec-driven development workflow

## Related Projects

Part of the Sain ecosystem. See repository README for related projects.

## Key Files to Reference

- `pyproject.toml` - Poetry dependencies and scripts
- `Makefile` - Development and deployment commands
- `docker/docker-compose.dev.yml` - Development Docker Compose
- `docker/docker-compose.run.yml` - Production Docker Compose
- `src/fastapi_service/main.py` - Application entry point
- `src/fastapi_service/router.py` - API router
- `src/fastapi_service/worker.py` - Celery worker
- `docs/README.md` - Documentation index
- `specs/index.md` - Specifications master index

