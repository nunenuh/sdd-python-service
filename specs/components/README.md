# Reusable Components

This directory contains reusable specification components for the FastAPI Service.

## Purpose

Components are reusable OpenAPI/JSON Schema definitions that can be referenced across multiple API specifications to ensure consistency and reduce duplication.

## Subdirectories

- **`common/`** - Common reusable components such as pagination schemas, error responses, and standard headers
- **`models/`** - Data model specifications that can be shared across multiple endpoints

## Usage

These components should be:
- **Referenced** in API specifications using `$ref` syntax
- **Reused** across multiple endpoints to maintain consistency
- **Updated** carefully as changes affect all referencing specifications

## Related Documentation

- API contracts: `../contracts/`
- Feature specifications: `../features/`
- API design conventions: `../conventions/02-api-design.md`

