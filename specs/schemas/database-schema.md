---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Database Schema Specification

Complete database structure documentation for FastAPI Service boilerplate.

**Source of Truth**: `src/fastapi_service/dbase/sql/models/*.py` (SQLAlchemy models)  
**Migrations**: `alembic/versions/`

## Database

- **Type**: PostgreSQL 15+
- **ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic
- **Connection**: Managed via `dbase/sql/core/session.py`

## Tables

### Your Models

When you create SQLAlchemy models, document them here following this format:

#### Example: `users`

Stores user information.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, INDEX | User ID (auto-increment) |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User email address |
| `name` | VARCHAR(200) | NOT NULL | User full name |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW | Creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW, ON UPDATE NOW | Last update timestamp |

**Indexes**:
- Primary key: `id`
- Unique: `email`
- Indexes: `email`

**Relationships**:
- Define relationships to other tables here

**Example**:
```python
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-12-16T10:00:00+00:00",
  "updated_at": "2025-12-16T10:00:00+00:00"
}
```

---

## Creating New Models

1. Create your SQLAlchemy model in `src/fastapi_service/dbase/sql/models/your_model.py`
2. Import it in `src/fastapi_service/dbase/sql/models/__init__.py`
3. Create a migration: `make db-migrate`
4. Apply the migration: `make db-upgrade`
5. Document the model in this file

## Migration Management

- **Create Migration**: `make db-migrate`
- **Apply Migrations**: `make db-upgrade`
- **Rollback**: `make db-downgrade`
- **View History**: `make db-history`

## Best Practices

1. Always use migrations for schema changes
2. Never modify existing migrations
3. Test migrations in development before production
4. Document all models in this file
5. Use appropriate indexes for frequently queried columns
6. Use foreign keys for relationships
7. Use timestamps (`created_at`, `updated_at`) for audit trails

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, INDEX | Source ID (auto-increment) |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL, INDEX | Source name (e.g., "kompas") |
| `url` | VARCHAR(500) | NOT NULL | Source base URL |
| `enabled` | BOOLEAN | NOT NULL, DEFAULT TRUE, INDEX | Whether source is enabled |
| `rate_limit` | INTEGER | NOT NULL, DEFAULT 1 | Requests per second |
| `retry_count` | INTEGER | NOT NULL, DEFAULT 3 | Number of retries on failure |
| `timeout` | INTEGER | NOT NULL, DEFAULT 30 | Request timeout in seconds |
| `selectors` | JSONB | NULL | Site-specific CSS selectors |
| `rss_url` | VARCHAR(500) | NULL | RSS feed URL |
| `sitemap_url` | VARCHAR(500) | NULL | Sitemap URL |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW | Creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW, ON UPDATE NOW | Last update timestamp |

**Indexes**:
- Primary key: `id`
- Unique: `name`
- Indexes: `name`, `enabled`

**Relationships**:
- None (standalone table)

**Selectors JSONB Structure**:
```json
{
  "title": ".read__title",
  "content": ".read__content",
  "author": ".read__author",
  "published_at": ".read__time",
  "category": ".read__category"
}
```

**Example**:
```python
{
  "id": 1,
  "name": "kompas",
  "url": "https://www.kompas.com",
  "enabled": true,
  "rate_limit": 1,
  "retry_count": 3,
  "timeout": 30,
  "selectors": {
    "title": ".read__title",
    "content": ".read__content"
  },
  "rss_url": null,
  "sitemap_url": "https://www.kompas.com/sitemap.xml",
  "created_at": "2025-12-01T00:00:00+00:00",
  "updated_at": "2025-12-16T00:00:00+00:00"
}
```

---

### `crawl_logs`

Stores crawl session logs for tracking crawling operations.

**Columns**:

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, INDEX | Crawl log ID (auto-increment) |
| `source_name` | VARCHAR(100) | NOT NULL, INDEX | Source name that was crawled |
| `started_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW | Crawl start time |
| `finished_at` | TIMESTAMP WITH TIME ZONE | NULL | Crawl finish time |
| `articles_found` | INTEGER | NOT NULL, DEFAULT 0 | Total articles found |
| `articles_new` | INTEGER | NOT NULL, DEFAULT 0 | New articles added |
| `articles_updated` | INTEGER | NOT NULL, DEFAULT 0 | Existing articles updated |
| `errors` | INTEGER | NOT NULL, DEFAULT 0 | Number of errors encountered |
| `status` | VARCHAR(50) | NOT NULL, DEFAULT 'running', INDEX | Crawl status |
| `error_details` | JSONB | NULL | Error details (if any) |

**Indexes**:
- Primary key: `id`
- Indexes: `source_name`, `status`, `started_at`

**Relationships**:
- None (standalone table)

**Status Values**:
- `running` - Crawl is in progress (default)
- `completed` - Crawl completed successfully
- `failed` - Crawl failed
- `partial` - Crawl completed with some errors

**Error Details JSONB Structure**:
```json
{
  "error": "Connection timeout",
  "timestamp": "2025-12-16T12:00:00Z",
  "url": "https://example.com/article"
}
```

**Example**:
```python
{
  "id": 1,
  "source_name": "kompas",
  "started_at": "2025-12-16T12:00:00+00:00",
  "finished_at": "2025-12-16T12:30:00+00:00",
  "articles_found": 150,
  "articles_new": 120,
  "articles_updated": 30,
  "errors": 0,
  "status": "completed",
  "error_details": null
}
```

---

## Database Relationships

Currently, all tables are standalone with no foreign key relationships. This is intentional for simplicity and performance.

**Future Considerations**:
- Foreign key from `articles.source_name` → `sources.name` (if needed)
- Foreign key from `crawl_logs.source_name` → `sources.name` (if needed)

## Indexes Summary

### Articles Table
- `id` (PRIMARY KEY)
- `url` (UNIQUE)
- `title`
- `source_name`
- `published_at`
- `category`
- `status`

### Sources Table
- `id` (PRIMARY KEY)
- `name` (UNIQUE)
- `enabled`

### Crawl Logs Table
- `id` (PRIMARY KEY)
- `source_name`
- `status`
- `started_at`

## Migration History

### 001_initial_schema.py
Creates initial database schema:
- `articles` table
- `sources` table
- `crawl_logs` table
- All indexes and constraints

**Migration Command**:
```bash
alembic upgrade head
```

## Data Types Reference

### PostgreSQL Types Used
- `INTEGER` - Integer values
- `VARCHAR(n)` - Variable-length strings with max length
- `TEXT` - Unlimited length text
- `BOOLEAN` - Boolean values
- `TIMESTAMP WITH TIME ZONE` - Timestamps with timezone
- `JSONB` - Binary JSON (PostgreSQL-specific)

### SQLAlchemy Mappings
- `Column(Integer)` → `INTEGER`
- `Column(String(n))` → `VARCHAR(n)`
- `Column(Text)` → `TEXT`
- `Column(Boolean)` → `BOOLEAN`
- `Column(DateTime(timezone=True))` → `TIMESTAMP WITH TIME ZONE`
- `Column(JSONB)` → `JSONB`

## Constraints

### Primary Keys
- All tables have `id` as primary key (auto-increment)

### Unique Constraints
- `articles.url` - URLs must be unique
- `sources.name` - Source names must be unique

### Default Values
- `articles.status` - Default: `'active'`
- `articles.crawled_at` - Default: `NOW()`
- `articles.updated_at` - Default: `NOW()`, auto-update on change
- `sources.enabled` - Default: `TRUE`
- `sources.rate_limit` - Default: `1`
- `sources.retry_count` - Default: `3`
- `sources.timeout` - Default: `30`
- `sources.created_at` - Default: `NOW()`
- `sources.updated_at` - Default: `NOW()`, auto-update on change
- `crawl_logs.started_at` - Default: `NOW()`
- `crawl_logs.articles_found` - Default: `0`
- `crawl_logs.articles_new` - Default: `0`
- `crawl_logs.articles_updated` - Default: `0`
- `crawl_logs.errors` - Default: `0`
- `crawl_logs.status` - Default: `'running'`

## Related Documentation

- **SQLAlchemy Models**: `src/fastapi_service/dbase/sql/models/`
- **Migration Script**: `alembic/versions/001_initial_schema.py`
- **Database Session**: `src/fastapi_service/dbase/sql/core/session.py`
- **Architecture**: `docs/architecture/database-design.md` (if exists)

