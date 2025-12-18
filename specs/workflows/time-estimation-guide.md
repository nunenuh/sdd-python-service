---
created: 2025-12-16T12:00:00Z
created_timestamp: 1765886400
updated: 2025-12-16T12:00:00Z
updated_timestamp: 1765886400
---

# Time Estimation Guide for Issues

AI-assisted time estimation guide for GitHub issues, providing estimates for different developer experience levels.

## Purpose

Enable accurate sprint planning by providing time estimates that consider:
- Task complexity
- Developer experience level
- Team member availability (30 min/day to full-time)

## Effort Categories

### XS (Extra Small)
- **Junior Dev**: 1-2 hours
- **Mid-level Dev**: 30 minutes - 1 hour
- **Senior Dev**: 15-30 minutes

**Examples:**
- Add a simple constant or configuration value
- Update environment variable defaults
- Fix a typo in documentation
- Add a simple Pydantic validation rule
- Update a single import statement

### S (Small)
- **Junior Dev**: 2-8 hours (< 1 day)
- **Mid-level Dev**: 1-4 hours
- **Senior Dev**: 30 minutes - 2 hours

**Examples:**
- Add a simple utility function
- Create a basic Pydantic schema with validation
- Add a simple API endpoint (CRUD)
- Write unit tests for existing function
- Update documentation for a feature

### M (Medium)
- **Junior Dev**: 1-3 days (8-24 hours)
- **Mid-level Dev**: 4-16 hours (0.5-2 days)
- **Senior Dev**: 2-8 hours (0.25-1 day)

**Examples:**
- Implement a service with business logic
- Create a complete CRUD handler (Handler → UseCase → Service)
- Add authentication to an endpoint
- Write integration tests for a feature
- Refactor a complex module
- Design and implement a database model with Alembic migration

### L (Large)
- **Junior Dev**: 3-7 days (24-56 hours)
- **Mid-level Dev**: 2-5 days (16-40 hours)
- **Senior Dev**: 1-3 days (8-24 hours)

**Examples:**
- Implement a complete feature module (Handler → UseCase → Service → Repository)
- Build external API integration (e.g., weather API)
- Create a complex reporting system
- Implement a notification system
- Major refactoring across multiple modules

### XL (Extra Large)
- **Junior Dev**: 1-2 weeks (40-80+ hours)
- **Mid-level Dev**: 1-1.5 weeks (40-60 hours)
- **Senior Dev**: 3-7 days (24-56 hours)

**Examples:**
- Build entire authentication system
- Implement complex multi-module feature
- Create comprehensive API documentation
- Major architectural changes
- Full feature with multiple components and database migrations

## Time Estimation Template

Add this to every issue:

```markdown
## Time Estimation

### Estimated Effort
- [ ] XS (< 2 hours)
- [ ] S (< 1 day)
- [ ] M (1-3 days)
- [ ] L (1 week)
- [ ] XL (> 1 week)

### Estimated Time by Developer Level

| Developer Level | Estimated Time | Notes |
|----------------|----------------|-------|
| **Junior** | X hours/days | Includes learning time |
| **Mid-level** | X hours/days | Familiar with patterns |
| **Senior** | X hours/days | Expert level |

**Complexity Factors:**
- [ ] New technology/library
- [ ] Complex business logic
- [ ] Multiple integrations
- [ ] Extensive testing required
- [ ] Documentation heavy
```

## AI Estimation Guidelines

### Factors to Consider

1. **Code Complexity**
   - Lines of code to write
   - Number of files to modify
   - Complexity of logic (conditional, loops, algorithms)

2. **Dependencies**
   - External libraries to learn
   - Integration with existing code
   - API integrations

3. **Testing Requirements**
   - Unit tests needed
   - Integration tests needed
   - Manual testing scenarios

4. **Documentation Requirements**
   - API documentation
   - Code comments
   - User guides
   - Technical specs

5. **Learning Curve**
   - New patterns for junior devs
   - Unfamiliar technologies
   - Complex domain knowledge

### Estimation Formula

**Base Time** = Code writing + Testing + Documentation

**Junior Developer Multiplier**: Base Time × 2.5-3.0
- Includes learning time
- Debugging time
- Code review iterations

**Mid-level Developer Multiplier**: Base Time × 1.5-2.0
- Some learning time
- Faster debugging
- Fewer review iterations

**Senior Developer Multiplier**: Base Time × 1.0-1.2
- Minimal learning
- Quick implementation
- Architectural decisions included

## Example Estimations

### Example 1: Add Favicon

**Task**: Add favicon.ico to the application

**Complexity Analysis:**
- Copy file to public directory
- Update HTML template
- Test in browser

**Estimates:**
- **Effort**: XS
- **Junior**: 1 hour (includes finding how to add it, testing)
- **Mid-level**: 30 minutes (knows where to put it)
- **Senior**: 15 minutes (routine task)

### Example 2: Create User Profile Endpoint

**Task**: Create GET /api/v1/users/{user_id}/profile endpoint

**Complexity Analysis:**
- Create handler method (15 min)
- Add Pydantic schema for response (15 min)
- Add authorization check (15 min)
- Write unit tests (30 min)
- Write integration test (30 min)
- Update API docs (15 min)
- Total base: ~2 hours

**Estimates:**
- **Effort**: S
- **Junior**: 6 hours (learning FastAPI, Pydantic, testing patterns)
- **Mid-level**: 3 hours (familiar with FastAPI patterns)
- **Senior**: 2 hours (quick implementation)

### Example 3: Implement Password Reset Flow

**Task**: Complete password reset feature (email, token, validation)

**Complexity Analysis:**
- Email service integration (2 hours)
- Token generation/validation (2 hours)
- Reset password endpoint (1 hour)
- Email templates (1 hour)
- Security considerations (1 hour)
- Unit tests (2 hours)
- Integration tests (2 hours)
- Documentation (1 hour)
- Total base: ~12 hours

**Estimates:**
- **Effort**: L
- **Junior**: 3-4 days (24-32 hours) - learning email services, tokens, security, FastAPI patterns
- **Mid-level**: 2-3 days (16-24 hours) - some learning, faster implementation
- **Senior**: 1.5-2 days (12-16 hours) - quick implementation, handles security well

### Example 4: Build Complete Report Management System

**Task**: Full CRUD module for reports with verification, media, comments

**Complexity Analysis:**
- SQLAlchemy models and Alembic migration (2 hours)
- Repository layer (4 hours)
- Service layer with business logic (8 hours)
- Handler endpoints (4 hours)
- Pydantic schemas and validation (4 hours)
- Media upload handling (4 hours)
- Verification system (4 hours)
- Comment system (4 hours)
- Unit tests (8 hours)
- Integration tests (8 hours)
- Documentation (4 hours)
- Total base: ~54 hours

**Estimates:**
- **Effort**: XL
- **Junior**: 10-12 days (80-96 hours) - significant learning SQLAlchemy, FastAPI, debugging
- **Mid-level**: 7-9 days (56-72 hours) - some learning, better implementation
- **Senior**: 5-7 days (40-56 hours) - efficient implementation, good architecture

## Sprint Planning Usage

### For Team with Mixed Availability

**Scenario**: Team has:
- Junior dev: 2 hours/day (10 hours/week)
- Mid-level dev: 4 hours/day (20 hours/week)
- Senior dev: 6 hours/day (30 hours/week)

**Sprint**: 2 weeks (10 working days)

**Capacity:**
- Junior: 20 hours total
- Mid-level: 40 hours total
- Senior: 60 hours total

**Task Assignment:**
- Junior: 2-3 Small tasks (S) = 12-18 hours
- Mid-level: 1 Medium + 2 Small = 20-28 hours
- Senior: 1 Large + 1 Medium = 36-48 hours

### Sprint Planning Template

```markdown
## Sprint X - Capacity Planning

**Duration**: 2 weeks (10 working days)

### Team Capacity

| Developer | Level | Hours/Day | Total Hours |
|-----------|-------|-----------|-------------|
| @alice | Junior | 2h | 20h |
| @bob | Mid-level | 4h | 40h |
| @carol | Senior | 6h | 60h |

**Total Capacity**: 120 hours

### Planned Tasks

| Task | Assignee | Effort | Est. Time | Status |
|------|----------|--------|-----------|--------|
| #42 Add favicon | @alice | XS | 1h | Todo |
| #43 User profile endpoint | @alice | S | 6h | Todo |
| #44 Report filters | @bob | M | 16h | Todo |
| #45 Password reset | @carol | L | 16h | In Progress |

**Total Planned**: 39 hours
**Buffer**: 81 hours (67.5%)
```

## AI Prompt for Time Estimation

When AI creates or reviews an issue, use this prompt:

```
Please estimate the time required for this task:

Task: [Description]

Consider:
1. Code complexity (files, logic, algorithms)
2. Testing requirements (unit, integration)
3. Documentation needs
4. Dependencies and integrations
5. Learning curve for different developer levels

Provide estimates for:
- Effort level (XS/S/M/L/XL)
- Junior Developer (includes learning time)
- Mid-level Developer (some familiarity)
- Senior Developer (expert level)

Format as:
**Estimated Effort**: [XS/S/M/L/XL]
**Junior Dev**: X hours/days (rationale)
**Mid-level Dev**: X hours/days (rationale)
**Senior Dev**: X hours/days (rationale)
```

## Estimation Accuracy

### Track and Improve

After task completion, compare:
- **Estimated time** (from issue)
- **Actual time** (from time tracking)
- **Variance** (actual - estimated)

### Refinement Over Time

```markdown
## Time Tracking (Update after completion)

**Estimated**: 6 hours (Junior)
**Actual**: 8 hours
**Variance**: +2 hours (+33%)

**Reasons for variance:**
- Unexpected dependency issue (1 hour)
- Additional edge cases discovered (1 hour)

**Lessons learned:**
- Always add buffer for dependencies
- Consider edge cases during estimation
```

## Common Estimation Mistakes

### ❌ Don't

1. **Ignore learning time** for juniors
2. **Forget testing time** (often 40-50% of coding time)
3. **Underestimate documentation** (often 10-20% of total time)
4. **Ignore review cycles** (add 10-20% for junior devs)
5. **Assume perfect conditions** (always add buffer)

### ✅ Do

1. **Break down large tasks** into smaller estimable pieces
2. **Add buffers** (×1.2-1.5 for uncertainty)
3. **Consider dependencies** (blocked tasks take longer)
4. **Review past estimates** (improve over time)
5. **Update estimates** if scope changes

## Quick Reference Table

| Task Type | Junior | Mid-level | Senior |
|-----------|--------|-----------|--------|
| Simple config change | 1h | 30min | 15min |
| Add utility function | 4h | 2h | 1h |
| Create Pydantic schema | 4h | 2h | 1h |
| Simple CRUD endpoint | 8h | 4h | 2h |
| Service with business logic | 16h | 8h | 4h |
| Complete feature module | 40h | 24h | 16h |
| External API integration | 32h | 20h | 12h |
| Major refactoring | 48h | 32h | 20h |
| New subsystem | 80h | 56h | 40h |

## Related Documents

- [GitHub Workflow](./github-workflow.md)
- [Issue Templates](./issue-templates.md)
- [Sprint Planning](./sprint-planning.md) (to be created)

---

**Last Updated**: 2025-12-16  
**Version**: 1.0.0
