# Alembic Versions

This directory contains Alembic migration version scripts.

## Purpose

Each file in this directory represents a database schema migration. Migrations are applied in order based on their revision chain.

## Naming Convention

Migrations are named: \`{revision}_{description}.py\`

Example: \`001_initial_schema.py\`

## Creating Migrations

Use Alembic commands to create migrations - do not create files manually.

\`\`\`bash
make db-migrate
\`\`\`
