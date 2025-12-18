# Project Constitution - FastAPI Service

**Created:** 2025-12-18T12:00:00Z UTC  
**Modified:** 2025-12-18T12:00:00Z UTC

**Purpose:** Stable, non-negotiable rules and constraints for FastAPI Service boilerplate  
**Status:** Living document - update only when fundamental decisions change

---

## Non-Negotiable Rules

### Architecture
- ✅ **Clean Architecture**: Follow layered architecture pattern (Handler → UseCase → Service → Repository)
- ✅ **Module-based organization**: Features organized in `src/fastapi_service/modules/`
- ✅ **Separation of concerns**: Business logic in services, data access in repositories
- ✅ **Dependency injection**: Use FastAPI's dependency injection system
- ✅ **Async-first**: Use async/await for all I/O operations

### Technology Stack
- ✅ **Python 3.11+**: Minimum Python version required
- ✅ **FastAPI**: Web framework for building APIs
- ✅ **SQLAlchemy 2.0+**: ORM for database operations
- ✅ **Alembic**: Database migration tool
- ✅ **Pydantic 2.0+**: Data validation and settings management
- ✅ **Poetry**: Dependency management and packaging
- ✅ **PostgreSQL**: Primary database
- ✅ **Redis**: Caching and session management
- ✅ **Uvicorn**: ASGI server for production

### Coding Standards
- ✅ **PEP 8 compliance**: Follow Python style guide
- ✅ **Type hints required**: All function signatures must have type hints
- ✅ **Black formatting**: Code formatted with Black (line length: 88)
- ✅ **isort**: Import sorting with Black profile
- ✅ **Async/await**: Use async/await for I/O operations, not callbacks
- ✅ **Maximum function length**: 100 lines (prefer smaller)
- ✅ **Maximum file length**: 500 lines (prefer smaller)

### Security
- ✅ **Input validation**: All inputs validated with Pydantic schemas
- ✅ **SQL injection prevention**: Use SQLAlchemy ORM, never raw SQL with user input
- ✅ **HTTPS only**: Production must use HTTPS
- ✅ **Environment variables**: Sensitive data in environment variables, never hardcoded
- ✅ **Authentication**: Implement proper authentication/authorization
- ✅ **Rate limiting**: Implement rate limiting for public endpoints

### Performance
- ✅ **API response time**: Target < 200ms for standard endpoints
- ✅ **Database queries**: Optimize queries, use indexes, avoid N+1 problems
- ✅ **Caching**: Use Redis for frequently accessed data
- ✅ **Async operations**: Use async/await for concurrent I/O operations
- ✅ **Connection pooling**: Use SQLAlchemy connection pooling

---

## Architectural Decisions

### Decision 1: Layered Architecture Pattern
**Date:** 2025-12-18  
**Rationale:** Ensures separation of concerns, testability, and maintainability. Each layer has a single responsibility.  
**Alternatives Considered:** 
- Flat structure (all code in one place)
- MVC pattern
- Domain-driven design (DDD)

**Consequences:** 
- Clear separation: HTTP handlers, business logic, data access
- Easy to test: Mock dependencies at each layer
- Easy to maintain: Changes isolated to specific layers
- Consistent structure across all modules

### Decision 2: FastAPI Framework
**Date:** 2025-12-18  
**Rationale:** High performance, automatic API documentation, type safety with Pydantic, async support, modern Python features.  
**Alternatives Considered:** 
- Django REST Framework
- Flask
- Tornado

**Consequences:** 
- Automatic OpenAPI/Swagger documentation
- Type validation with Pydantic
- Excellent performance (comparable to Node.js)
- Modern async/await support
- Easy to learn and use

### Decision 3: SQLAlchemy 2.0+ with Alembic
**Date:** 2025-12-18  
**Rationale:** Mature ORM, excellent async support, type hints, migration management with Alembic.  
**Alternatives Considered:** 
- Django ORM
- Tortoise ORM
- Raw SQL with psycopg2

**Consequences:** 
- Type-safe database operations
- Automatic migration generation
- Database-agnostic queries
- Connection pooling built-in
- Async support for high concurrency

### Decision 4: Poetry for Dependency Management
**Date:** 2025-12-18  
**Rationale:** Better dependency resolution than pip, lock file for reproducible builds, project management features.  
**Alternatives Considered:** 
- pip + requirements.txt
- pipenv
- conda

**Consequences:** 
- Reproducible builds with lock file
- Better dependency conflict resolution
- Project metadata in pyproject.toml
- Easy publishing to PyPI

---

## Constraints

### Infrastructure
- ✅ **Docker-based deployment**: All services containerized
- ✅ **Environment variables**: Configuration via environment variables (no hardcoded values)
- ✅ **Stateless services**: Services must be stateless (use Redis for sessions)
- ✅ **Database migrations**: All schema changes via Alembic migrations
- ✅ **Health checks**: All services must expose `/api/v1/health` endpoint

### External Dependencies
- ✅ **Rate limiting**: External API calls must implement rate limiting and retry logic
- ✅ **Timeout handling**: All external API calls must have timeout (default: 10 seconds)
- ✅ **Error handling**: Graceful degradation when external services fail
- ✅ **No direct database access**: Frontend/clients access via REST API only
- ✅ **API versioning**: Use `/api/v1/` prefix for all endpoints

### Compliance
- ✅ **Code quality**: All code must pass linting (`make lint-all`)
- ✅ **Type safety**: Type hints required, mypy checks (if enabled)
- ✅ **Testing**: Aim for >80% code coverage
- ✅ **Documentation**: All public APIs documented with docstrings
- ✅ **Security**: Regular dependency updates, security scanning

---

## Coding Standards

### Language-Specific Rules
- ✅ **Python 3.11+**: Use modern Python features (type hints, dataclasses, etc.)
- ✅ **Type hints required**: All function signatures must have type hints
- ✅ **PEP 8 compliance**: Follow Python style guide
- ✅ **Black formatting**: Code formatted with Black (line length: 88)
- ✅ **isort**: Import sorting with Black profile
- ✅ **No `Any` types**: Prefer explicit types, use `Any` only when necessary
- ✅ **Async/await**: Use async/await for I/O operations

### Code Organization
- ✅ **Module structure**: Each module follows Handler → UseCase → Service → Repository pattern
- ✅ **One class per file**: Each class in its own file (except small related classes)
- ✅ **Maximum file length**: 500 lines (prefer smaller, split if needed)
- ✅ **Maximum function length**: 100 lines (prefer smaller)
- ✅ **Dependency injection**: Use FastAPI's `Depends()` for dependencies
- ✅ **Import organization**: Standard library → third-party → local imports

### Testing Requirements
- ✅ **Minimum 80% code coverage**: Aim for high test coverage
- ✅ **All public APIs tested**: All endpoints must have tests
- ✅ **Unit tests**: Test business logic in isolation
- ✅ **Integration tests**: Test API endpoints end-to-end
- ✅ **Test organization**: Tests mirror source structure (`tests/unit/`, `tests/integration/`)
- ✅ **Test fixtures**: Use pytest fixtures for test setup
- ✅ **Mock external dependencies**: Mock database, Redis, external APIs in tests

---

## How to Use This File

1. **For AI Agents (Cursor AI, GitHub Copilot):**
   - Load this file first for stable context
   - Reference before generating code
   - Never violate constraints listed here
   - Follow the architectural patterns (Handler → UseCase → Service → Repository)
   - Use type hints, async/await, and Pydantic schemas
   - Format code with Black (88 char line length)

2. **For Developers:**
   - Review before making architectural decisions
   - Follow the module structure conventions
   - Ensure all code has type hints
   - Run `make lint-all` before committing
   - Update when fundamental changes occur
   - Reference in code reviews

3. **For Project Managers:**
   - Understand project constraints
   - Reference when planning features
   - Use for stakeholder communication
   - Know that architecture changes require team discussion

---

## Update Guidelines

**When to Update:**
- Fundamental architectural changes
- New non-negotiable constraints
- Technology stack changes
- Security requirement changes

**When NOT to Update:**
- Temporary decisions
- Feature-specific choices
- Implementation details
- Frequently changing requirements

**Update Process:**
1. Discuss with team (architecture decisions affect everyone)
2. Document rationale in this file
3. Update related documentation (`specs/conventions/`, `README.md`)
4. Communicate changes to team
5. Commit with clear message: `docs(constitution): update [decision]`
6. Update `IMPLEMENTATION_STATUS.md` if needed

---

**Note:** This file should change infrequently. If you find yourself updating it often, consider if those decisions belong in feature specifications (`specs/features/`) or conventions (`specs/conventions/`) instead.

---

## Related Documentation

- [Python Conventions](../conventions/01-python-conventions.md)
- [Module Structure](../conventions/03-module-structure.md)
- [API Design](../conventions/02-api-design.md)
- [Testing Standards](../conventions/04-testing-standards.md)
- [Security Guidelines](../conventions/05-security-guidelines.md)
- [Git Commit Rules](../../.cursor/rules/git-commit-rules-v1.mdc)