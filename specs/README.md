---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Specifications Directory

This directory contains **AI-readable specifications** extracted from the source code in `src/` and original developer documentation in `docs/`. These specs are designed to be consumed by AI coding assistants (like Cursor, GitHub Copilot) to understand the codebase and generate consistent code.

**Important**: The **source of truth** is currently in `src/`. These specs are extracted/generated from the actual implementation to help AI tools understand the codebase structure.

## Source of Truth Mapping

| Spec Type | Source of Truth Location | Spec Location | Original Docs |
|-----------|-------------------------|---------------|---------------|
| **Database Schemas** | `src/fastapi_service/dbase/sql/models/*.py` (SQLAlchemy) | `specs/schemas/database-schema.md` | `docs/architecture/` |
| **API Contract** | `src/fastapi_service/modules/*/apiv1/handler.py` (FastAPI) | `specs/contracts/api-contract.md` | `docs/api/` |
| **DTOs/Schemas** | `src/fastapi_service/modules/*/schemas.py` (Pydantic) | `specs/schemas/*.schema.json` | - |
| **Services** | `src/fastapi_service/modules/*/services.py` | `specs/contracts/service-contracts.md` | - |
| **Repositories** | `src/fastapi_service/modules/*/repositories.py` | `specs/conventions/03-module-structure.md` | - |

## Structure

```
specs/
├── index.md               # Master index and table of contents
├── README.md             # This file
├── IMPLEMENTATION_STATUS.md  # Current implementation analysis
├── features/              # Feature-based specifications
│   ├── health/            # Health check feature
│   └── <your-feature>/    # Your feature specifications
├── api/                   # API specifications
│   ├── openapi.yaml       # OpenAPI 3.0 specification (to be generated)
│   └── api-reference.md   # API reference documentation
├── schemas/               # Data schemas
│   ├── database-schema.md  # Database structure documentation
│   └── <your-model>.schema.json
├── contracts/             # API contracts
│   └── api-contract.md    # Complete API contract documentation
├── conventions/           # Coding conventions
│   ├── 00-repository-overview.md
│   ├── 01-python-conventions.md
│   ├── 02-api-design.md
│   ├── 03-database-patterns.md
│   ├── 04-testing-standards.md
│   ├── 05-security-guidelines.md
│   ├── 06-deployment-rules.md
│   └── 07-documentation-standards.md
├── examples/              # Request/response examples
│   ├── requests/
│   └── responses/
├── components/            # Reusable specification components
│   ├── common/
│   └── models/
├── validation/            # Validation rules
│   └── business-rules.md
├── workflows/             # GitHub workflows and project management
│   ├── github-workflow.md
│   ├── issue-templates.md
│   └── pr-template.md
└── versions/              # Version history
```

## Purpose

In AI-driven spec development, specifications are **machine-readable artifacts** extracted from code that AI tools consume:

1. **API Specifications** (`specs/api/`)
   - OpenAPI/Swagger YAML files extracted from FastAPI routes
   - Complete API contract definitions
   - Used by AI to understand endpoints and generate consistent code
   - **Original spec**: `docs/api/` (if exists)

2. **Schemas** (`specs/schemas/`)
   - JSON Schema definitions extracted from SQLAlchemy models
   - Pydantic schema definitions extracted from `schemas.py`
   - Database schema documentation from `dbase/sql/models/` + `docs/architecture/`
   - AI uses these to understand data structures and generate types/validators

3. **Contracts** (`specs/contracts/`)
   - Protocol definitions extracted from implementation
   - Service contracts documented from `services.py`
   - Integration contracts from `repositories.py`
   - **Original spec**: `docs/api/` (if exists)

4. **Conventions** (`specs/conventions/`)
   - Coding conventions and best practices
   - Python style guides (PEP 8)
   - FastAPI design patterns
   - Scrapy patterns
   - Database patterns (SQLAlchemy)
   - Testing standards
   - Security guidelines
   - Deployment rules
   - Documentation standards
   - **Source**: Extracted from `.cursorrules` and project patterns

5. **Features** (`specs/features/`)
   - Feature-based specifications
   - Requirements, design, and tasks for each feature
   - **Source**: Extracted from `modules/` and `docs/planning/`

## AI-Driven Spec Development Workflow

### Current State: Code-First (Reverse Engineering Specs)
1. **Code exists** in `src/` (source of truth)
2. **Original specs exist** in `docs/` (created by developers)
3. **Extract specs** from code + docs → Generate specs in `specs/`
4. **AI reads specs** → Understands codebase structure
5. **AI generates code** → Consistent with existing patterns

### Future State: Spec-First (True Spec-Driven)
1. **Write specs first** in `specs/` (source of truth)
2. **AI reads specs** → Generates code in `src/`
3. **Validate code** → Ensure matches specs
4. **Update specs** → Regenerate code

## How to Keep Specs in Sync

### Manual Sync (Current)
- When code changes in `src/`, manually update corresponding specs
- When original specs in `docs/` are updated, sync to `specs/`
- Review specs periodically to ensure they match implementation

### Automated Sync (Future)
```bash
# Generate OpenAPI spec from FastAPI routes
poetry run python scripts/generate_openapi.py > specs/api/openapi.yaml

# Generate JSON schemas from SQLAlchemy models
poetry run python scripts/generate_schemas.py

# Generate feature specs from modules
poetry run python scripts/generate_feature_specs.py
```

## OpenAPI Specification

The OpenAPI specification should be **auto-generated** from FastAPI routes:

- **Source**: `src/fastapi_service/modules/*/apiv1/handler.py` with FastAPI decorators
- **Generator**: FastAPI's built-in OpenAPI generation
- **Output**: Available at `/docs` when server runs (Swagger UI)
- **Manual Copy**: Should be copied to `specs/api/openapi.yaml` for AI consumption

### Current Status
- ✅ FastAPI auto-generates OpenAPI spec from route decorators
- ✅ Available at `/docs` when server is running
- ⚠️ Manual OpenAPI spec in `specs/api/openapi.yaml` needs to be synced with code

## Schema Management

### JSON Schemas
- **Source**: `src/fastapi_service/dbase/sql/models/*.py` (SQLAlchemy models)
- **Extracted to**: `specs/schemas/*.schema.json`
- **Usage**: AI can generate TypeScript types or Python types from JSON Schema

### Pydantic Schemas
- **Source**: `src/fastapi_service/modules/*/schemas.py`
- **Already in Python**: Pydantic models are already Python-native
- **Usage**: AI can use these directly for validation and type hints

### Database Schemas
- **Source**: `src/fastapi_service/dbase/sql/models/*.py` (SQLAlchemy ORM)
- **Original Spec**: `docs/architecture/` (if exists)
- **Documented in**: `specs/schemas/database-schema.md`
- **Usage**: AI understands database structure for migrations and queries

## Best Practices

1. **Keep Specs Updated**: When code changes, update specs
2. **Single Source of Truth**: Currently `src/` is source of truth, specs are extracted
3. **Reference Original Docs**: Link to original developer specs in `docs/`
4. **Version Control**: Track spec changes in git
5. **AI Consumption**: Write specs in formats AI can easily parse (YAML, JSON, Markdown)
6. **Documentation**: Markdown files explain the specs, but aren't consumed by AI

## Related Documentation

- **API Documentation**: `docs/api/` - Human-readable API documentation
- **Architecture**: `docs/architecture/` - System architecture and design
- **Implementation**: `docs/implementation/` - Developer guides
- **Planning**: `docs/planning/` - Project planning documents
- **Testing**: `docs/testing/` - Testing documentation

## Tools

### OpenAPI Tools
- **Swagger Editor**: Edit OpenAPI specs visually
- **OpenAPI Generator**: Generate client SDKs from specs
- **Spectral**: Lint OpenAPI specs

### Schema Tools
- **JSON Schema Validator**: Validate JSON against schemas
- **Pydantic**: Runtime validation from schemas
- **SQLAlchemy**: Database schema management

## Future Enhancements

- [ ] Set up automated spec extraction from `src/`
- [ ] Create script to sync OpenAPI spec from running server
- [ ] Generate JSON schemas automatically from SQLAlchemy models
- [ ] Set up CI validation of specs against code
- [ ] Migrate to spec-first development (specs become source of truth)
- [ ] Link specs more directly to original developer docs in `docs/`
