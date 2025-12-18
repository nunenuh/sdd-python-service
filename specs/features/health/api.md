---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Health Check API Specification

Complete API specification for the Health module.

## Base Path

`/api/v1/health`

## Endpoints

### Ping

**GET** `/api/v1/health/ping`

Simple liveness check endpoint. Always returns quickly and is used by load balancers and orchestration systems.

**Response:** `200 OK`
```json
{
  "status": "ok",
  "timestamp": "2023-01-01T10:00:00Z",
  "message": "pong"
}
```

**Use Cases:**
- Kubernetes liveness probe
- Load balancer health check
- Service discovery health check

---

### Health Status

**GET** `/api/v1/health/status`

Basic health status with dependency checks. Provides a quick overview of service health including essential dependencies.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T10:00:00Z",
  "version": "0.1.0",
  "components": [
    {
      "name": "database",
      "status": "healthy",
      "message": "Database configured: localhost/fastapi_service",
      "response_time_ms": 5.2
    },
    {
      "name": "redis",
      "status": "healthy",
      "message": "Redis configured: localhost:6379",
      "response_time_ms": 2.1
    },
    {
      "name": "elasticsearch",
      "status": "unhealthy",
      "message": "Elasticsearch not configured",
      "response_time_ms": null
    }
  ],
  "uptime_seconds": 3600.5
}
```

**Component Status Values:**
- `healthy` - Component is operational
- `unhealthy` - Component is not operational or not configured

**Overall Status:**
- `healthy` - All components are healthy
- `unhealthy` - At least one component is unhealthy

**Use Cases:**
- Kubernetes readiness probe
- Monitoring dashboards
- Service dependency checks

**Error Responses:**
- `503 Service Unavailable` - Health check failed

---

### Detailed Health Status

**GET** `/api/v1/health/detailed`

Comprehensive health status with system metrics. Provides detailed health information including component checks, system metrics, and performance data.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T10:00:00Z",
  "version": "0.1.0",
  "uptime_seconds": 3600.5,
  "components": [
    {
      "name": "database",
      "status": "healthy",
      "message": "Database configured: localhost/fastapi_service",
      "response_time_ms": 5.2
    },
    {
      "name": "redis",
      "status": "healthy",
      "message": "Redis configured: localhost:6379",
      "response_time_ms": 2.1
    },
    {
      "name": "elasticsearch",
      "status": "unhealthy",
      "message": "Elasticsearch not configured",
      "response_time_ms": null
    }
  ],
  "system_metrics": {
    "cpu_percent": 25.5,
    "memory_percent": 45.2,
    "memory_available_gb": 4.5,
    "disk_usage_percent": 60.0,
    "disk_free_gb": 100.0,
    "network_bytes_sent": 1024000,
    "network_bytes_recv": 2048000
  },
  "process_metrics": {
    "pid": 12345,
    "memory_rss_mb": 256.5,
    "memory_vms_mb": 512.0,
    "cpu_percent": 5.2,
    "num_threads": 8,
    "uptime_seconds": 3600.5,
    "open_files": 50
  },
  "system_info": {
    "python_version": "3.11.0",
    "platform": "Linux-5.15.0-x86_64",
    "hostname": "fastapi-service-api",
    "boot_time": "2023-01-01T00:00:00Z",
    "load_average": [1.2, 1.5, 1.8]
  },
  "environment": "production",
  "debug_mode": false
}
```

**Use Cases:**
- Detailed monitoring and debugging
- Performance analysis
- Capacity planning
- Troubleshooting

**Error Responses:**
- `503 Service Unavailable` - Health check failed

---

## Architecture

### Request Flow

```
HTTP Request
  ↓
Handler (apiv1/handler.py)
  ↓
HealthService (services.py)
  ↓
ComponentHealthService (services.py)
  ↓
System Metrics (psutil)
```

### Components

- **Handler**: HTTP request/response handling
- **HealthService**: Aggregates health checks and metrics
- **ComponentHealthService**: Individual component health checks
- **System Metrics**: Collected via `psutil` library

---

## Health Check Components

### Database

Checks PostgreSQL connectivity and configuration.

**Status Determination:**
- `healthy` - Database is configured and accessible
- `unhealthy` - Database not configured or connection failed

### Redis

Checks Redis connectivity and configuration.

**Status Determination:**
- `healthy` - Redis is configured and accessible
- `unhealthy` - Redis not configured or connection failed

### Elasticsearch (Deprecated)

Checks Elasticsearch connectivity and configuration. Currently deprecated in favor of Meilisearch.

**Status Determination:**
- `healthy` - Elasticsearch is configured and accessible
- `unhealthy` - Elasticsearch not configured or connection failed

---

## System Metrics

### CPU

- **cpu_percent** (float) - CPU usage percentage (0-100)

### Memory

- **memory_percent** (float) - Memory usage percentage (0-100)
- **memory_available_gb** (float) - Available memory in GB

### Disk

- **disk_usage_percent** (float) - Disk usage percentage (0-100)
- **disk_free_gb** (float) - Free disk space in GB

### Network

- **network_bytes_sent** (integer) - Total bytes sent
- **network_bytes_recv** (integer) - Total bytes received

---

## Process Metrics

- **pid** (integer) - Process ID
- **memory_rss_mb** (float) - Resident memory in MB
- **memory_vms_mb** (float) - Virtual memory in MB
- **cpu_percent** (float) - Process CPU usage percentage
- **num_threads** (integer) - Number of threads
- **uptime_seconds** (float) - Process uptime in seconds
- **open_files** (integer) - Number of open file descriptors

---

## System Information

- **python_version** (string) - Python version
- **platform** (string) - Operating system platform
- **hostname** (string) - System hostname
- **boot_time** (datetime) - System boot time
- **load_average** (array of floats) - System load average (1, 5, 15 min)

---

## Error Handling

All endpoints use standard HTTP status codes:
- `200 OK` - Success
- `503 Service Unavailable` - Health check failed

Error response format:
```json
{
  "error": "health_check_failed",
  "message": "Error message",
  "timestamp": "2023-01-01T10:00:00Z"
}
```

---

## Performance Considerations

- **Ping**: Should return in < 10ms
- **Status**: Should return in < 100ms
- **Detailed**: May take longer (up to 500ms) due to system metrics collection

---

## Related Specifications

- [Health Schemas](../../src/fastapi_service/modules/health/schemas.py)
- [Health Services](../../src/fastapi_service/modules/health/services.py)

