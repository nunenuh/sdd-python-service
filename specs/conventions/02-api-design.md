---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# API Design Conventions

API design standards and best practices for the FastAPI Service service.

## RESTful Principles

### Resource Naming

- Use plural nouns for collections: `/api/v1/articles`, `/api/v1/sources`
- Use singular nouns for individual resources: `/api/v1/articles/{id}`
- Use lowercase with hyphens for multi-word resources: `/api/v1/crawl-logs`
- Avoid verbs in URLs (use HTTP methods instead)

### HTTP Methods

- **GET** - Retrieve resources (idempotent, safe)
- **POST** - Create resources or trigger actions
- **PUT** - Update/replace entire resource
- **PATCH** - Partial update (not currently used)
- **DELETE** - Delete resources (idempotent)

### Status Codes

- `200 OK` - Success (GET, PUT)
- `201 Created` - Resource created (POST)
- `202 Accepted` - Request accepted, processing asynchronously
- `204 No Content` - Success with no response body (DELETE)
- `400 Bad Request` - Client error (validation, malformed request)
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., duplicate)
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service temporarily unavailable

---

## URL Structure

### Base Path

All API endpoints are prefixed with `/api/v1/`

### Path Patterns

```
/api/v1/{resource}              # Collection endpoint
/api/v1/{resource}/{id}         # Individual resource endpoint
/api/v1/{resource}/{id}/{sub}   # Sub-resource endpoint
```

### Examples

```
GET    /api/v1/articles              # List articles
POST   /api/v1/articles              # Create article
GET    /api/v1/articles/{id}         # Get article
PUT    /api/v1/articles/{id}         # Update article
DELETE /api/v1/articles/{id}         # Delete article
GET    /api/v1/articles/search       # Search articles (action)
POST   /api/v1/crawler/start         # Start crawl (action)
```

---

## Request/Response Format

### Content-Type

- **Request:** `application/json`
- **Response:** `application/json`

### Request Body

All request bodies must be valid JSON:

```json
{
  "field1": "value1",
  "field2": 123,
  "field3": true
}
```

### Response Body

Standard response format:

```json
{
  "id": 1,
  "field1": "value1",
  "field2": 123,
  "created_at": "2023-01-01T10:00:00Z"
}
```

### Pagination

List endpoints return paginated responses:

```json
{
  "items": [...],
  "total": 1000,
  "page": 1,
  "page_size": 100,
  "total_pages": 10
}
```

**Query Parameters:**
- `skip` (integer, default: 0) - Number of records to skip
- `limit` (integer, default: 100, max: 1000) - Maximum records to return

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message"
}
```

### Validation Errors

```json
{
  "detail": "Validation error: field 'url' is required"
}
```

### Multiple Errors

```json
{
  "detail": [
    "Field 'title' is required",
    "Field 'url' must be a valid URL"
  ]
}
```

---

## Query Parameters

### Filtering

Use query parameters for filtering:

```
GET /api/v1/articles?source_name=kompas&status=active
```

### Sorting

Use `sort` parameter:

```
GET /api/v1/articles/search?q=indonesia&sort=published_at:desc
```

Format: `field:order` where `order` is `asc` or `desc`

### Pagination

Use `skip` and `limit`:

```
GET /api/v1/articles?skip=0&limit=100
```

---

## Versioning

### Current Version

- **API Version:** `v1`
- **Base Path:** `/api/v1/`

### Versioning Strategy

- Use URL path versioning: `/api/v1/`, `/api/v2/`
- Maintain backward compatibility within major versions
- Deprecate endpoints with `Deprecated` header before removal

### Deprecation

Include deprecation header:

```
Deprecated: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
```

---

## Authentication

### Current Status

Authentication is optional. Future versions will require API key authentication.

### Future Authentication

**Header:**
```
X-API-Key: your-api-key-here
```

**Error Response (401):**
```json
{
  "detail": "No API key provided"
}
```

---

## Rate Limiting

### Current Status

Rate limiting is not currently implemented.

### Future Rate Limiting

**Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

**Error Response (429):**
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

---

## CORS

### Allowed Origins

Configured via `ALLOWED_ORIGINS_STR` environment variable.

**Default:** `*` (all origins)

**Production:** Specific origins (comma-separated)

---

## Best Practices

### Idempotency

- GET, PUT, DELETE operations should be idempotent
- POST operations that create resources should check for duplicates

### Caching

- Use appropriate cache headers for GET requests
- `Cache-Control: public, max-age=3600` for static resources
- `Cache-Control: no-cache` for dynamic resources

### Compression

- Support `gzip` compression for responses
- Client indicates support via `Accept-Encoding: gzip`

### Date Formats

- Use ISO 8601 format: `2023-01-01T10:00:00Z`
- Always use UTC timezone

### Field Naming

- Use `snake_case` for JSON fields: `source_name`, `published_at`
- Use `camelCase` for JavaScript clients (if needed)

---

## Related Specifications

- [API Contract](../contracts/api-contract.md)
- [Articles API](../features/articles/api.md)
- [Sources API](../features/sources/api.md)
- [Crawler API](../features/crawler/api.md)
- [Health API](../features/health/api.md)

