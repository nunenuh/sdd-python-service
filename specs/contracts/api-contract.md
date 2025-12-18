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

