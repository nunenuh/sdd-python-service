# Common Components

This directory contains reusable specification components for the FastAPI Service boilerplate.

## Purpose

Common components are reusable OpenAPI/JSON Schema components that can be referenced across multiple API specifications.

## Contents

- **Pagination**: Pagination response schemas
- **Error Responses**: Standard error response formats
- **Health Check Response**: Health check endpoint response format
- **Common Headers**: Standard HTTP headers

## Usage

Reference these components in your OpenAPI specifications using `$ref`:

```yaml
responses:
  '400':
    $ref: './components/common/error-responses.yaml#/BadRequest'
```

- **Health Check Response**: Health check endpoint response format
- **Common Headers**: Standard HTTP headers

## Usage

Reference these components in your OpenAPI specifications using `$ref`:

```yaml
responses:
  '400':
    $ref: './components/common/error-responses.yaml#/BadRequest'
```
