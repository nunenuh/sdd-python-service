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
