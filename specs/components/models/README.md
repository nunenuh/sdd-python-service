# Data Models

This directory contains reusable data model specifications for the FastAPI Service boilerplate.

## Purpose

Data models define the structure of entities used throughout the API, such as:
- User models
- Resource models
- Request/response models

## Contents

- **Model Specifications**: OpenAPI/JSON Schema definitions for each model
- **Model Relationships**: Documentation of relationships between models

## Usage

Reference these models in your API specifications:

```yaml
schema:
  $ref: './components/models/user-model.yaml'
```
