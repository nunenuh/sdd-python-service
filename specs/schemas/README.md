# Database Schemas

This directory contains database schema specifications and documentation.

## Purpose

Schema specifications document:
- Database structure and table definitions
- Column types and constraints
- Relationships and foreign keys
- Indexes and performance optimizations
- Migration history and changes

## Files

- **`database-schema.md`** - Complete database structure documentation, including all tables, columns, relationships, and indexes.

## Source of Truth

The actual database schema is defined in:
- **SQLAlchemy Models**: `src/fastapi_service/dbase/sql/models/*.py`
- **Migrations**: `alembic/versions/`

## Usage

These schemas serve as:
- **Documentation** for developers working with the database
- **Reference** for understanding data relationships
- **Specification** for database migrations
- **Guide** for API response modeling

## Related Documentation

- Database models: `../../src/fastapi_service/dbase/sql/models/`
- Migration files: `../../alembic/versions/`
- Component models: `../components/models/`

