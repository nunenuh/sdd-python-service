---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# FastAPI Service Specifications - Master Index

Complete table of contents for all project specifications.

## Quick Links

- **[Features](#features)** - Feature-based specifications
- **[API Specifications](#api-specifications)** - API contracts and endpoints
- **[Data Schemas](#data-schemas)** - Database and validation schemas
- **[Conventions](#conventions)** - Coding standards and best practices
- **[Workflows](#workflows)** - GitHub workflows and project management
- **[Examples](#examples)** - Request/response examples
- **[Components](#components)** - Reusable specification components
- **[Glossary](./glossary.md)** - Terms and definitions

## Features

### Health Monitoring
- [API Specification](./features/health/api.md) - API endpoints ✅

### Your Features
When you add new features, create specifications here following the module structure conventions.

## API Specifications

### OpenAPI
- [OpenAPI Specification](./api/openapi.yaml) - Complete OpenAPI 3.0+ spec (to be generated)
- [API Reference](./api/api-reference.md) - Usage guide

### API Contracts
- [API Contract](./contracts/api-contract.md) - Complete API contract documentation

## Data Schemas

### Database Schemas
- [Database Schema](./schemas/database-schema.md) - Complete database structure

### JSON Schemas
- Create JSON schemas for your models as needed

### Pydantic Schemas
- Pydantic schemas are defined in `src/fastapi_service/modules/*/schemas.py`
- Health schemas are defined in `src/fastapi_service/modules/health/schemas.py`

## Conventions

### Coding Standards
- [Repository Overview](./conventions/00-repository-overview.md) ✅
- [Python Conventions](./conventions/01-python-conventions.md) ✅
- [API Design](./conventions/02-api-design.md) ✅
- [Module Structure](./conventions/03-module-structure.md) ✅ - Module organization patterns
- [Testing Standards](./conventions/04-testing-standards.md) ✅
- [Security Guidelines](./conventions/05-security-guidelines.md) ✅
- [Database Patterns](./conventions/06-database-patterns.md) - TODO
- [Deployment Rules](./conventions/07-deployment-rules.md) - TODO
- [Documentation Standards](./conventions/08-documentation-standards.md) - TODO

## Workflows

### GitHub & Project Management
- [GitHub Workflow](./workflows/github-workflow.md) - Complete workflow guide
- [Issue Templates](./workflows/issue-templates.md) - Issue creation templates
- [PR Template](./workflows/pr-template.md) - Pull request template

## Examples

### Request Examples
- [Create Article Request](./examples/requests/create-article.json)
- [Start Crawl Request](./examples/requests/start-crawl.json)
- [Create Source Request](./examples/requests/create-source.json)
- [Search Articles Request](./examples/requests/search-articles.json)

### Response Examples
- [Article Created](./examples/responses/article-created.json)
- [Crawl Started](./examples/responses/crawl-started.json)
- [Search Results](./examples/responses/search-results.json)
- [Error Response](./examples/responses/error-response.json)

## Components

### Common Components
- [Pagination](./components/common/pagination.yaml)
- [Error Responses](./components/common/error-responses.yaml)
- [Health Check Response](./components/common/health-response.yaml)

### Data Models
- [Article Model](./components/models/article-model.yaml)
- [Source Model](./components/models/source-model.yaml)
- [CrawlLog Model](./components/models/crawl-log-model.yaml)

## Validation

- [Business Rules](./validation/business-rules.md)
- [Input Validation](./validation/input-validation.yaml)

## Integrations

### External Services
- [Meilisearch Integration](./integrations/meilisearch.md)
- [Redis Integration](./integrations/redis.md)
- [PostgreSQL Integration](./integrations/postgresql.md)
- [Celery Integration](./integrations/celery.md)

## Security

- [Authentication Specification](./security/authentication-spec.md)
- [Rate Limiting](./security/rate-limiting-spec.md)
- [Data Privacy](./security/data-privacy-spec.md)

## Testing

- [API Test Scenarios](./tests/api-test-scenarios.yaml)
- [Integration Tests](./tests/integration-tests.yaml)
- [Infrastructure Tests](./tests/infrastructure-tests.md)

## Version History

- [Changelog](./CHANGELOG.md) - Version history and changes
- [Versions](./versions/) - Historical versions

## Related Documentation

- **Human-Readable Docs**: `../docs/` - Complete project documentation
- **Source Code**: `../src/` - Implementation (source of truth)
- **API Documentation**: `../docs/api/` - API guides and references
- **Architecture**: `../docs/architecture/` - Architecture documentation

## Navigation Tips

1. **By Feature**: Use the [Features](#features) section to find domain-specific specs
2. **By Type**: Use topic sections (API, Schemas, etc.) for technical specs
3. **Quick Reference**: Check [Examples](#examples) for practical use cases
4. **Standards**: Refer to [Conventions](#conventions) for coding guidelines

## Maintenance

- Update this index when adding new specifications
- Keep links current and valid
- Follow the [Documentation Standards](./conventions/07-documentation-standards.md)
- Review and update quarterly
