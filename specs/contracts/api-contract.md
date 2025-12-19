---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# API Contract Specification

Complete API contract specification for FastAPI Service service.

## Base URL

- **Development**: `http://localhost:8080`
- **API Prefix**: `/api`
- **API Version**: `v1`
- **Full Base Path**: `/api/v1`
- **Production**: TBD

## Authentication

Currently, the API does not implement authentication. All endpoints are publicly accessible.

**Future**: Authentication may be added for administrative endpoints.

## Response Format

### Success Response
```json
{
  "id": 1,
  "title": "Article Title",
  "content": "Article content...",
  ...
}
```

Or for list endpoints:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

## HTTP Status Codes

- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST (resource created)
- `202 Accepted` - Request accepted for processing (async operations)
- `204 No Content` - Successful DELETE (no content returned)
- `400 Bad Request` - Invalid request data
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `501 Not Implemented` - Feature not yet implemented
- `503 Service Unavailable` - Service unavailable (health checks)

## API Endpoints

### Health Endpoints

#### GET `/api/v1/health/ping`
Simple liveness check.

**Response**: `200 OK`
```json
{
  "status": "ok",
  "timestamp": "2025-12-16T12:00:00Z",
  "message": "pong"
}
```

#### GET `/api/v1/health/status`
Basic health status with dependency checks.

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-12-16T12:00:00Z",
  "version": "0.1.0",
  "components": [
    {
      "name": "database",
      "status": "healthy",
      "message": "Database configured",
      "response_time_ms": 1.5
    },
    {
      "name": "redis",
      "status": "healthy",
      "message": "Redis configured",
      "response_time_ms": 0.8
    }
  ],
  "uptime_seconds": 3600
}
```

**Response**: `503 Service Unavailable` (if unhealthy)
```json
{
  "error": "health_check_failed",
  "message": "Error details",
  "timestamp": "2025-12-16T12:00:00Z"
}
```

#### GET `/api/v1/health/detailed`
Comprehensive health status with system metrics.

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-12-16T12:00:00Z",
  "version": "0.1.0",
  "uptime_seconds": 3600,
  "components": {...},
  "system_metrics": {
    "cpu_percent": 25.5,
    "memory_percent": 45.2,
    "disk_percent": 60.0
  },
  "process_metrics": {
    "threads": 10,
    "open_files": 50
  },
  "system_info": {
    "platform": "linux",
    "python_version": "3.11.0"
  },
  "environment": "development",
  "debug_mode": true
}
```

---

## Adding New Endpoints

When you add new features, document their endpoints here following the same format as the Health endpoints above.

---

## Error Handling

### Validation Errors (400 Bad Request)
```json
{
  "detail": "Field 'title' is required"
}
```

### Not Found Errors (404 Not Found)
```json
{
  "detail": "Resource with ID 1 not found"
}
```

### Server Errors (500 Internal Server Error)
```json
{
  "detail": "Internal server error message"
}
```

### Service Unavailable (503 Service Unavailable)
Used for health check failures:
```json
{
  "error": "health_check_failed",
  "message": "Database connection failed",
  "timestamp": "2025-12-16T12:00:00Z"
}
```

## Rate Limiting

Currently not implemented. May be added in the future.

## Pagination

List endpoints support pagination using `skip` and `limit` query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

Response includes pagination metadata:
- `total`: Total number of records
- `page`: Current page number (calculated from skip/limit)
- `page_size`: Page size (limit value)
- `total_pages`: Total number of pages (calculated)

## Filtering

Endpoints may support filtering via query parameters. Document filtering options for each endpoint that supports it.

## Sorting

Endpoints may support sorting via `sort` parameter:
- Format: `field:order` (e.g., `created_at:desc`, `name:asc`)
- Document supported fields for each endpoint that supports sorting

## Related Documentation

- **Implementation Status**: [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)
- **Database Schema**: [schemas/database-schema.md](./schemas/database-schema.md)
- **Feature Specs**: [features/](./features/)


**Request Body**:
```json
{
  "title": "Article Title",
  "content": "Article content...",
  "summary": "Article summary",
  "url": "https://example.com/article",
  "source_name": "kompas",
  "author": "Author Name",
  "published_at": "2025-12-15T10:00:00Z",
  "category": "nasional",
  "tags": ["tag1", "tag2"],
  "image_url": "https://example.com/image.jpg",
  "status": "active"
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "title": "Article Title",
  ...
}
```

**Response**: `400 Bad Request` (validation error)
```json
{
  "detail": "Validation error message"
}
```

#### PUT `/api/v1/articles/{article_id}`
Update an article.

**Path Parameters**:
- `article_id` (int) - Article ID

**Request Body** (all fields optional):
```json
{
  "title": "Updated Title",
  "content": "Updated content",
  "status": "archived"
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "title": "Updated Title",
  ...
}
```

#### DELETE `/api/v1/articles/{article_id}`
Delete an article.

**Path Parameters**:
- `article_id` (int) - Article ID

**Response**: `204 No Content`

**Response**: `404 Not Found`
```json
{
  "detail": "Article with ID 1 not found"
}
```

#### GET `/api/v1/articles/search`
Search articles using Meilisearch.

**Query Parameters**:
- `q` (string, required, min: 1) - Search query string
- `limit` (int, default: 10, min: 1, max: 100) - Number of results to return
- `offset` (int, default: 0, min: 0) - Pagination offset
- `source_name` (string, optional) - Filter by source name
- `category` (string, optional) - Filter by category
- `sort` (string, optional, default: "published_at:desc") - Sort order (e.g., "published_at:desc", "title:asc")

**Response**: `200 OK`
```json
{
  "hits": [
    {
      "id": 1,
      "title": "Article Title",
      "content": "Article content...",
      "url": "https://example.com/article",
      "source_name": "kompas",
      "published_at": "2025-12-15T10:00:00Z",
      "_formatted": {
        "title": "<em>Article</em> Title"
      }
    }
  ],
  "total": 100,
  "offset": 0,
  "limit": 10,
  "query": "indonesia"
}
```

**Examples**:
- Simple search: `/api/v1/articles/search?q=indonesia`
- With filter: `/api/v1/articles/search?q=indonesia&source_name=kompas`
- With sort: `/api/v1/articles/search?q=indonesia&sort=published_at:desc`
- Pagination: `/api/v1/articles/search?q=indonesia&limit=20&offset=0`

---

### Crawler Endpoints

#### POST `/api/v1/crawler/start`
Start a crawl for a news source.

**Request Body**:
```json
{
  "source_name": "kompas",
  "mode": "incremental"
}
```

**Parameters**:
- `source_name` (string, required) - Name of the source to crawl
- `mode` (string, default: "incremental") - Crawl mode: "full" or "incremental"
  - `incremental`: Crawl new articles only (max 1000 articles)
  - `full`: Full crawl (max 10000 articles)

**Response**: `202 Accepted`
```json
{
  "status": "started",
  "source_name": "kompas",
  "mode": "incremental",
  "message": "Crawl task started with ID: abc123",
  "started_at": "2025-12-16T12:00:00Z"
}
```

**Response**: `400 Bad Request`
```json
{
  "detail": "Source 'kompas' not found or disabled"
}
```

#### GET `/api/v1/crawler/logs/{log_id}`
Get crawl log by ID.

**Path Parameters**:
- `log_id` (int) - Crawl log ID

**Response**: `200 OK`
```json
{
  "id": 1,
  "source_name": "kompas",
  "started_at": "2025-12-16T12:00:00Z",
  "finished_at": "2025-12-16T12:30:00Z",
  "articles_found": 150,
  "articles_new": 120,
  "articles_updated": 30,
  "errors": 0,
  "status": "completed",
  "error_details": null
}
```

**Response**: `404 Not Found`
```json
{
  "detail": "Crawl log with ID 1 not found"
}
```

#### GET `/api/v1/crawler/logs`
List crawl logs.

**Query Parameters**:
- `source_name` (string, optional) - Filter by source name
- `skip` (int, default: 0) - Number of records to skip
- `limit` (int, default: 100, max: 1000) - Maximum number of records to return

**Response**: `501 Not Implemented`
```json
{
  "detail": "List crawl logs not yet implemented"
}
```

---

### Source Endpoints

#### GET `/api/v1/sources`
List all sources.

**Query Parameters**:
- `enabled_only` (bool, default: false) - Only return enabled sources

**Response**: `200 OK`
```json
{
  "items": [
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
      "created_at": "2025-12-01T00:00:00Z",
      "updated_at": "2025-12-16T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### GET `/api/v1/sources/{source_id}`
Get source by ID.

**Path Parameters**:
- `source_id` (int) - Source ID

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "kompas",
  "url": "https://www.kompas.com",
  ...
}
```

**Response**: `404 Not Found`
```json
{
  "detail": "Source with ID 1 not found"
}
```

#### POST `/api/v1/sources`
Create a new source.

**Request Body**:
```json
{
  "name": "detik",
  "url": "https://www.detik.com",
  "enabled": true,
  "rate_limit": 1,
  "retry_count": 3,
  "timeout": 30,
  "selectors": {
    "title": ".detail__title",
    "content": ".detail__body"
  },
  "rss_url": "https://www.detik.com/rss",
  "sitemap_url": "https://www.detik.com/sitemap.xml"
}
```

**Response**: `201 Created`
```json
{
  "id": 2,
  "name": "detik",
  ...
}
```

#### PUT `/api/v1/sources/{source_id}`
Update a source.

**Path Parameters**:
- `source_id` (int) - Source ID

**Request Body** (all fields optional):
```json
{
  "enabled": false,
  "rate_limit": 2
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "kompas",
  "enabled": false,
  ...
}
```

#### DELETE `/api/v1/sources/{source_id}`
Delete a source.

**Path Parameters**:
- `source_id` (int) - Source ID

**Response**: `204 No Content`

**Response**: `404 Not Found`
```json
{
  "detail": "Source with ID 1 not found"
}
```

---

## Error Handling

### Validation Errors (400 Bad Request)
```json
{
  "detail": "Field 'title' is required"
}
```

### Not Found Errors (404 Not Found)
```json
{
  "detail": "Article with ID 1 not found"
}
```

### Server Errors (500 Internal Server Error)
```json
{
  "detail": "Internal server error message"
}
```

### Service Unavailable (503 Service Unavailable)
Used for health check failures:
```json
{
  "error": "health_check_failed",
  "message": "Database connection failed",
  "timestamp": "2025-12-16T12:00:00Z"
}
```

## Rate Limiting

Currently not implemented. May be added in the future.

## Pagination

List endpoints support pagination using `skip` and `limit` query parameters:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 1000)

Response includes pagination metadata:
- `total`: Total number of records
- `page`: Current page number (calculated from skip/limit)
- `page_size`: Page size (limit value)
- `total_pages`: Total number of pages (calculated)

## Filtering

Several endpoints support filtering:
- Articles: `source_name`, `status`, `category`
- Crawl Logs: `source_name` (when implemented)
- Sources: `enabled_only`

## Sorting

Search endpoint supports sorting via `sort` parameter:
- Format: `field:order` (e.g., `published_at:desc`, `title:asc`)
- Default: `published_at:desc`
- Supported fields: `published_at`, `crawled_at`, `title`

## Related Documentation

- **Implementation Status**: [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)
- **Database Schema**: [schemas/database-schema.md](./schemas/database-schema.md)
- **Feature Specs**: [features/](./features/)

