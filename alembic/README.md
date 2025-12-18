# Alembic Migrations

This directory contains Alembic database migration scripts.

## Purpose

Alembic migrations manage database schema changes over time, allowing you to:
- Version control database schema
- Apply schema changes consistently across environments
- Rollback schema changes if needed

## Usage

\`\`\`bash
# Create a new migration
make db-migrate

# Apply migrations
make db-upgrade

# Rollback last migration
make db-downgrade

# View migration history
make db-history
\`\`\`

## Structure

- \`versions/\`: Contains migration scripts
- \`env.py\`: Alembic environment configuration
- \`script.py.mako\`: Migration script template

## Creating Migrations

1. Modify your SQLAlchemy models in \`src/fastapi_service/dbase/sql/models/\`
2. Run \`make db-migrate\` to auto-generate migration
3. Review the generated migration in \`alembic/versions/\`
4. Apply with \`make db-upgrade\`
