---
created: 2025-12-16T12:00:00Z
updated: 2025-12-16T12:00:00Z
---

# Security Guidelines

Security best practices and guidelines for the FastAPI Service service.

## Authentication

### Current Implementation

**Status:** Optional API key authentication

**Header:** `X-API-Key`

**Configuration:** `APP_X_API_KEY` environment variable

**Default:** `changeme` (must be changed in production)

### Future Enhancements

- JWT token authentication
- OAuth2 integration
- Role-based access control (RBAC)

---

## API Security

### Input Validation

**All inputs must be validated:**

- Use Pydantic models for request validation
- Validate data types, ranges, formats
- Sanitize user input to prevent injection attacks

**Example:**
```python
class ArticleCreate(BaseModel):
    title: str = Field(..., max_length=500)
    url: str = Field(..., max_length=1000)
    # Validation happens automatically
```

### SQL Injection Prevention

**Use parameterized queries:**

- SQLAlchemy ORM (automatic protection)
- Never use string concatenation for SQL queries
- Use query builders and ORM methods

**Example:**
```python
# ✅ Safe - SQLAlchemy ORM
article = db.query(Article).filter(Article.id == article_id).first()

# ❌ Unsafe - Never do this
query = f"SELECT * FROM articles WHERE id = {article_id}"
```

### XSS Prevention

**Sanitize output:**

- FastAPI automatically escapes HTML in JSON responses
- Use appropriate content types
- Validate and sanitize user-generated content

---

## Data Protection

### Sensitive Data

**Never log sensitive information:**

- Passwords
- API keys
- Authentication tokens
- Personal information

**Example:**
```python
# ✅ Safe
logger.info("user_authenticated", user_id=user_id)

# ❌ Unsafe
logger.info(f"User {username} logged in with password {password}")
```

### Data Encryption

**At Rest:**
- Database encryption (PostgreSQL)
- Environment variable encryption
- Secret management (future: HashiCorp Vault)

**In Transit:**
- HTTPS/TLS for all API communication
- Encrypted database connections
- Encrypted Redis connections

---

## Environment Variables

### Secrets Management

**Never commit secrets to version control:**

- Use `.env` files (gitignored)
- Use environment variables in production
- Rotate secrets regularly

**Example `.env`:**
```bash
# Database
DB_PASSWORD=secure_password_here

# API Keys
APP_X_API_KEY=secure_api_key_here
MEILISEARCH_MASTER_KEY=secure_master_key_here

# Redis
REDIS_PASSWORD=secure_redis_password_here
```

### Secret Rotation

- Rotate API keys quarterly
- Rotate database passwords annually
- Rotate immediately if compromised

---

## Rate Limiting

### Current Status

**Not implemented** - To be added in future versions

### Future Implementation

**Per-IP Rate Limiting:**
- 1000 requests per hour per IP
- 100 requests per minute per IP
- Exponential backoff on limit exceeded

**Per-API-Key Rate Limiting:**
- Tiered limits based on API key type
- Higher limits for premium keys

---

## CORS Configuration

### Current Configuration

**Development:** `*` (all origins)

**Production:** Specific origins only

**Configuration:**
```python
ALLOWED_ORIGINS_STR = "https://example.com,https://app.example.com"
```

### Best Practices

- Never use `*` in production
- Specify exact origins
- Use HTTPS only in production

---

## HTTPS/TLS

### Production Requirements

- **Required:** All API endpoints must use HTTPS
- **TLS Version:** TLS 1.2 or higher
- **Certificate:** Valid SSL certificate from trusted CA

### Development

- HTTP allowed for local development
- Use HTTPS for testing production-like environments

---

## Dependency Security

### Dependency Management

**Regular Updates:**
- Update dependencies monthly
- Check for security vulnerabilities
- Use `poetry update` to update dependencies

**Vulnerability Scanning:**
- Use `safety` or `pip-audit` to check for vulnerabilities
- Fix critical vulnerabilities immediately
- Review security advisories regularly

**Example:**
```bash
# Check for vulnerabilities
poetry run safety check

# Update dependencies
poetry update
```

---

## Logging Security

### Sensitive Data

**Never log:**
- Passwords
- API keys
- Authentication tokens
- Credit card numbers
- Personal identification numbers

### Log Sanitization

**Sanitize before logging:**
```python
# ✅ Safe
logger.info("api_request", endpoint="/api/v1/articles", user_id=user_id)

# ❌ Unsafe
logger.info(f"API request: {request.headers}")  # May contain auth tokens
```

---

## Error Handling

### Information Disclosure

**Don't expose internal details:**

- Don't expose stack traces in production
- Don't expose database schema details
- Don't expose file paths or system information

**Example:**
```python
# ✅ Safe - Generic error message
raise HTTPException(
    status_code=500,
    detail="An error occurred processing your request"
)

# ❌ Unsafe - Exposes internal details
raise HTTPException(
    status_code=500,
    detail=f"Database error: {str(e)}"  # May expose schema
)
```

---

## Crawler Security

### Robots.txt Compliance

**Always respect robots.txt:**
- Configured via `CRAWLER_ROBOTS_TXT_COMPLIANCE=true`
- Scrapy automatically checks robots.txt
- Respect crawl-delay directives

### Rate Limiting

**Be respectful:**
- Use appropriate delays between requests
- Configure per-source rate limits
- Monitor for rate limit violations

### User-Agent

**Identify crawler:**
- Use descriptive user agent
- Include contact information
- Follow website terms of service

---

## Database Security

### Connection Security

**Use secure connections:**
- SSL/TLS for database connections
- Strong passwords
- Limited database user permissions

### Access Control

**Principle of least privilege:**
- Database user should only have necessary permissions
- Separate read/write users if possible
- Regular access reviews

---

## Monitoring and Alerting

### Security Monitoring

**Monitor for:**
- Failed authentication attempts
- Unusual API usage patterns
- Rate limit violations
- Error rate spikes

### Alerting

**Alert on:**
- Multiple failed authentication attempts
- Unusual traffic patterns
- Security-related errors
- Dependency vulnerabilities

---

## Incident Response

### Security Incidents

**If a security incident occurs:**

1. **Immediate:** Revoke compromised credentials
2. **Investigate:** Review logs and identify scope
3. **Contain:** Limit damage and prevent further access
4. **Notify:** Inform affected users if necessary
5. **Document:** Record incident details and response
6. **Prevent:** Implement measures to prevent recurrence

---

## Related Specifications

- [API Design](./02-api-design.md#authentication)
- [Deployment Rules](./06-deployment-rules.md)
- [Security Documentation](../../docs/security/)

