---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Testing Standards

Testing conventions and standards for the FastAPI Service service.

## Test Structure

### Directory Layout

```
tests/
├── unit/                    # Unit tests
│   ├── test_config.py
│   ├── test_scrapy_pipelines.py
│   └── test_scrapy_middlewares.py
├── integration/             # Integration tests
│   ├── test_health_api.py
│   └── test_articles_api.py
├── e2e/                    # End-to-end tests
│   └── test_crawl_flow.py
├── infrastructure/         # Infrastructure tests
│   ├── test_postgres.py
│   ├── test_redis.py
│   ├── test_meilisearch.py
│   ├── test_celery.py
│   └── test_flower.py
└── conftest.py             # Shared fixtures
```

---

## Test Types

### Unit Tests

**Purpose:** Test individual components in isolation

**Location:** `tests/unit/`

**Scope:**
- Functions and methods
- Classes and modules
- Business logic
- Utilities

**Example:**
```python
def test_article_service_create():
    """Test ArticleService.create_article()."""
    # Arrange
    service = ArticleService(mock_db)
    article_data = ArticleCreate(...)
    
    # Act
    result = service.create_article(article_data)
    
    # Assert
    assert result["id"] is not None
    assert result["title"] == article_data.title
```

### Integration Tests

**Purpose:** Test API endpoints with real dependencies

**Location:** `tests/integration/`

**Scope:**
- API endpoints
- Database operations
- Service interactions

**Example:**
```python
def test_create_article_endpoint(client):
    """Test POST /api/v1/articles."""
    response = client.post(
        "/api/v1/articles",
        json={"title": "Test", "url": "https://example.com"}
    )
    assert response.status_code == 201
    assert response.json()["id"] is not None
```

### End-to-End Tests

**Purpose:** Test complete workflows

**Location:** `tests/e2e/`

**Scope:**
- Full crawl flow
- Article lifecycle
- Search functionality

**Example:**
```python
def test_crawl_to_search_flow():
    """Test complete flow from crawl to search."""
    # Start crawl
    crawl_response = start_crawl("kompas")
    assert crawl_response.status_code == 202
    
    # Wait for completion
    wait_for_crawl_completion(crawl_response.json()["crawl_log_id"])
    
    # Search articles
    search_response = search_articles("indonesia")
    assert len(search_response.json()["hits"]) > 0
```

### Infrastructure Tests

**Purpose:** Test external service connectivity

**Location:** `tests/infrastructure/`

**Scope:**
- PostgreSQL connectivity
- Redis connectivity
- Meilisearch connectivity
- Celery worker/beat
- Flower monitoring

**Example:**
```python
def test_postgres_connection(postgres_engine):
    """Test PostgreSQL connection."""
    with postgres_engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
```

---

## Testing Tools

### Framework

- **pytest** - Primary testing framework
- **pytest-asyncio** - Async test support
- **pytest-cov** - Coverage reporting
- **pytest-mock** - Mocking support

### Fixtures

**Location:** `tests/conftest.py`

**Common Fixtures:**
- `client` - FastAPI test client
- `db_session` - Database session
- `redis_client` - Redis client
- `meilisearch_client` - Meilisearch client

**Example:**
```python
@pytest.fixture
def client():
    """FastAPI test client."""
    from fastapi_service.main import app
    return TestClient(app)
```

---

## Test Naming

### File Naming

- Prefix with `test_`: `test_articles_api.py`
- Match module structure: `test_scrapy_pipelines.py`

### Function Naming

- Prefix with `test_`: `test_create_article()`
- Use descriptive names: `test_article_service_create_with_duplicate_url()`

### Class Naming

- Prefix with `Test`: `TestArticleService`
- Group related tests: `TestArticleRepository`

---

## Test Organization

### Arrange-Act-Assert Pattern

```python
def test_example():
    # Arrange - Set up test data
    article_data = ArticleCreate(...)
    service = ArticleService(mock_db)
    
    # Act - Execute the code under test
    result = service.create_article(article_data)
    
    # Assert - Verify the results
    assert result["id"] is not None
    assert result["title"] == article_data.title
```

### Test Isolation

- Each test should be independent
- Use fixtures for setup/teardown
- Clean up test data after each test

---

## Mocking

### When to Mock

- External services (Redis, Meilisearch, PostgreSQL)
- Network requests
- File system operations
- Time-dependent operations

### Mock Examples

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test with mocked dependency."""
    mock_service = Mock()
    mock_service.get_data.return_value = {"key": "value"}
    
    result = function_under_test(mock_service)
    assert result == {"key": "value"}
```

---

## Coverage

### Target Coverage

- **Minimum:** 80% overall coverage
- **Critical Paths:** 100% coverage
- **Business Logic:** 90%+ coverage

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=fastapi_service --cov-report=html

# View report
open htmlcov/index.html
```

---

## Test Data

### Fixtures

Use pytest fixtures for test data:

```python
@pytest.fixture
def sample_article():
    """Sample article data."""
    return {
        "title": "Test Article",
        "url": "https://example.com/article",
        "source_name": "test_source"
    }
```

### Factories

Use factories for complex test data:

```python
def create_article_factory(**kwargs):
    """Create article with defaults."""
    defaults = {
        "title": "Test Article",
        "url": "https://example.com/article",
        "source_name": "test_source"
    }
    defaults.update(kwargs)
    return ArticleCreate(**defaults)
```

---

## Running Tests

### All Tests

```bash
make test
```

### Specific Test Type

```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Infrastructure tests only
pytest tests/infrastructure/
```

### Specific Test File

```bash
pytest tests/unit/test_articles.py
```

### Specific Test Function

```bash
pytest tests/unit/test_articles.py::test_create_article
```

### With Coverage

```bash
make test-coverage
```

---

## Best Practices

### Test Independence

- Tests should not depend on each other
- Tests should be runnable in any order
- Use fixtures for shared setup

### Test Speed

- Unit tests should be fast (< 1ms each)
- Integration tests may be slower (< 100ms each)
- E2E tests may take longer (< 1s each)

### Test Clarity

- Use descriptive test names
- Add docstrings for complex tests
- Keep tests focused on one behavior

### Error Testing

- Test both success and failure cases
- Test edge cases and boundary conditions
- Test error handling and recovery

---

## Related Specifications

- [Infrastructure Tests](../../docs/testing/infrastructure-tests.md)
- [Testing Documentation](../../docs/testing/)
- [pytest Documentation](https://docs.pytest.org/)

