---
created: 2025-12-16T12:00:00Z
created_timestamp: 1765886400
updated: 2025-12-16T12:00:00Z
updated_timestamp: 1765886400
---

# GitHub Issue Templates

Copy-paste templates for creating GitHub issues following Pulse project management standards.

## Feature Request Template

```markdown
---
name: Feature Request
about: Propose a new feature
title: '[FEATURE] '
labels: feature, status:todo
assignees: ''
---

## Feature Description
<!-- Brief description of the feature -->

## User Story
**As a** [type of user]  
**I want** [goal]  
**So that** [reason]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Considerations
<!-- List technical details -->
- Dependencies:
- API changes:
- Database changes:
- Security implications:

## Implementation Approach
<!-- Optional: Suggest how this could be implemented -->

## Specifications Required
- [ ] `requirements.md` - User stories and requirements
- [ ] `design.md` - Technical design
- [ ] `tasks.md` - Task breakdown

## Related Issues
<!-- Link related issues -->
- Related to: #
- Depends on: #
- Blocks: #

## Priority
- [ ] Critical (blocking)
- [ ] High (important)
- [ ] Medium (normal)
- [ ] Low (nice to have)

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
| **Junior** | ___ hours/days | Includes learning time |
| **Mid-level** | ___ hours/days | Familiar with patterns |
| **Senior** | ___ hours/days | Expert level |

**Complexity Factors:**
- [ ] New technology/library
- [ ] Complex business logic
- [ ] Multiple integrations
- [ ] Extensive testing required
- [ ] Documentation heavy

**AI Estimation:** (To be filled by AI assistant)
<!-- AI: Please analyze the task and provide time estimates for each developer level -->

## Additional Context
<!-- Add any other context, screenshots, or examples -->
```

---

## Bug Report Template

```markdown
---
name: Bug Report
about: Report a bug or issue
title: '[BUG] '
labels: bug, status:todo
assignees: ''
---

## Bug Description
<!-- Clear and concise description of the bug -->

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- **OS**: [e.g., Ubuntu 22.04, macOS 14, Windows 11]
- **Python version**: [e.g., 3.11.5]
- **Poetry version**: [e.g., 1.7.0]
- **Database**: [e.g., PostgreSQL 15.2]
- **Branch**: [e.g., main, feature/issue-123-xyz]
- **Commit**: [e.g., abc123]

## Error Messages
<!-- Paste error messages or logs -->
```
[Paste error logs here]
```

## Screenshots
<!-- If applicable, add screenshots to help explain the problem -->

## Possible Cause
<!-- Optional: Your analysis of what might be causing this -->

## Suggested Fix
<!-- Optional: How you think this could be fixed -->

## Severity
- [ ] Critical (system down, data loss)
- [ ] High (major functionality broken)
- [ ] Medium (workaround available)
- [ ] Low (minor issue, cosmetic)

## Impact
- [ ] Blocks other work
- [ ] Affects production
- [ ] Affects development
- [ ] Security vulnerability

## Related Issues
- Related to: #
- Duplicate of: #

## Additional Context
<!-- Any other relevant information -->
```

---

## Task Template

```markdown
---
name: Task
about: Create a development task
title: '[TASK] '
labels: task, status:todo
assignees: ''
---

## Task Description
<!-- Clear description of what needs to be done -->

## Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Context
<!-- Why this task is needed -->

## Implementation Details
### Technical Approach
<!-- How this will be implemented -->

### Files to Modify/Create
- `src/fastapi_service/modules/feature_name/handler.py`
- `src/fastapi_service/modules/feature_name/services.py`

### Dependencies
- Requires: #
- Blocks: #

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests added/updated
- [ ] Documentation updated

## Time Estimation

### Estimated Effort
- [ ] XS (< 2 hours)
- [ ] S (< 1 day)
- [ ] M (1-3 days)

### Estimated Time by Developer Level

| Developer Level | Estimated Time | Notes |
|----------------|----------------|-------|
| **Junior** | ___ hours/days | Includes learning time |
| **Mid-level** | ___ hours/days | Familiar with patterns |
| **Senior** | ___ hours/days | Expert level |

**AI Estimation:** (To be filled by AI assistant)

## Related
- Feature: #
- Related tasks: #

## Checklist
- [ ] Code follows project conventions
- [ ] Tests added
- [ ] Documentation updated
- [ ] PR created
```

---

## Documentation Template

```markdown
---
name: Documentation
about: Documentation update or creation
title: '[DOCS] '
labels: docs, status:todo
assignees: ''
---

## Documentation Needed
<!-- What documentation needs to be created or updated -->

## Scope
- [ ] API documentation
- [ ] User guides
- [ ] Technical specifications
- [ ] README updates
- [ ] Code comments
- [ ] Architecture docs
- [ ] Deployment guides

## Target Audience
- [ ] Developers
- [ ] End users
- [ ] System administrators
- [ ] DevOps engineers

## Related Code/Features
<!-- What code or features are being documented -->
- Files: 
- Features: #
- Related issues: #

## Documentation Structure
<!-- Outline of the documentation -->
1. Section 1
2. Section 2
3. Section 3

## Acceptance Criteria
- [ ] Documentation written
- [ ] Examples included
- [ ] Screenshots/diagrams added (if applicable)
- [ ] Reviewed for accuracy
- [ ] Reviewed for clarity
- [ ] Links updated

## References
<!-- Existing docs or resources to reference -->
- 

## Estimated Effort
- [ ] XS (< 2 hours)
- [ ] S (< 1 day)
- [ ] M (1-3 days)
```

---

## Refactoring Template

```markdown
---
name: Refactoring
about: Code improvement without changing functionality
title: '[REFACTOR] '
labels: refactor, status:todo
assignees: ''
---

## Refactoring Scope
<!-- What code needs to be refactored -->

## Current Issues
<!-- What problems exist with the current code -->
- [ ] Technical debt
- [ ] Performance problems
- [ ] Maintainability issues
- [ ] Code duplication
- [ ] Complexity
- [ ] Outdated patterns

## Proposed Approach
<!-- How the refactoring will be done -->

### Before
```typescript
// Current code example
```

### After
```typescript
// Proposed code example
```

## Benefits
- Improved performance
- Better maintainability
- Reduced complexity
- Better type safety
- Clearer code

## Risks
<!-- Potential issues -->
- Breaking changes?
- Performance regression?
- Side effects?

## Testing Strategy
<!-- How to ensure nothing breaks -->
- [ ] Unit tests updated
- [ ] Integration tests added
- [ ] Manual testing checklist

## Acceptance Criteria
- [ ] Code refactored
- [ ] All tests passing
- [ ] No functional changes
- [ ] Performance maintained or improved
- [ ] Documentation updated

## Related Issues
- Technical debt: #
- Related refactorings: #

## Time Estimation

### Estimated Effort
- [ ] S (< 1 day)
- [ ] M (1-3 days)
- [ ] L (1 week)

### Estimated Time by Developer Level

| Developer Level | Estimated Time | Notes |
|----------------|----------------|-------|
| **Junior** | ___ hours/days | Includes learning time |
| **Mid-level** | ___ hours/days | Familiar with patterns |
| **Senior** | ___ hours/days | Expert level |

**AI Estimation:** (To be filled by AI assistant)
```

---

## Performance Improvement Template

```markdown
---
name: Performance Improvement
about: Optimize performance
title: '[PERF] '
labels: enhancement, performance, status:todo
assignees: ''
---

## Performance Issue
<!-- Describe the performance problem -->

## Current Metrics
<!-- Baseline measurements -->
- Response time: 
- Memory usage: 
- CPU usage: 
- Database queries: 

## Target Metrics
<!-- Desired improvements -->
- Response time: 
- Memory usage: 
- CPU usage: 
- Database queries: 

## Bottleneck Analysis
<!-- What's causing the slowdown -->
- 

## Proposed Optimization
<!-- How to improve performance -->

## Implementation Plan
1. Step 1
2. Step 2
3. Step 3

## Testing Strategy
<!-- How to measure improvements -->
- [ ] Benchmark before
- [ ] Implement optimization
- [ ] Benchmark after
- [ ] Load testing

## Risks
<!-- Potential issues -->
- Code complexity increase?
- Breaking changes?
- Memory trade-offs?

## Acceptance Criteria
- [ ] Performance improved by X%
- [ ] No functional regressions
- [ ] Tests passing
- [ ] Benchmarks documented

## Related Issues
- Performance: #

## Time Estimation

### Estimated Effort
- [ ] M (1-3 days)
- [ ] L (1 week)

### Estimated Time by Developer Level

| Developer Level | Estimated Time | Notes |
|----------------|----------------|-------|
| **Junior** | ___ hours/days | Includes learning time |
| **Mid-level** | ___ hours/days | Familiar with patterns |
| **Senior** | ___ hours/days | Expert level |

**AI Estimation:** (To be filled by AI assistant)
```

---

## Security Issue Template

```markdown
---
name: Security Issue
about: Report a security vulnerability (PRIVATE)
title: '[SECURITY] '
labels: security, priority:critical
assignees: ''
---

⚠️ **MAKE THIS ISSUE PRIVATE** - Do not disclose security vulnerabilities publicly

## Vulnerability Description
<!-- Describe the security issue -->

## Severity
- [ ] Critical (remote code execution, authentication bypass)
- [ ] High (data exposure, privilege escalation)
- [ ] Medium (information disclosure)
- [ ] Low (minor security concern)

## Attack Vector
<!-- How can this be exploited -->

## Steps to Reproduce
<!-- How to demonstrate the vulnerability -->
1. Step 1
2. Step 2
3. Step 3

## Impact
<!-- What can an attacker do -->

## Affected Versions
<!-- Which versions are affected -->
- Versions: 

## Proposed Fix
<!-- How to fix this vulnerability -->

## Immediate Mitigation
<!-- Temporary workarounds while fixing -->

## References
<!-- CVEs, security advisories, etc. -->
- 

## Disclosure Timeline
- Reported: [Date]
- Fix target: [Date]
- Public disclosure: [Date + 90 days]
```

---

## Deployment Template

```markdown
---
name: Deployment
about: Plan a deployment
title: '[DEPLOY] '
labels: deployment, status:todo
assignees: ''
---

## Deployment Scope
<!-- What's being deployed -->
- Version: 
- Environment: [ ] Staging [ ] Production

## Changes Included
<!-- List features, bugs, tasks -->
- Features: #, #
- Bug fixes: #, #
- Tasks: #

## Pre-Deployment Checklist
- [ ] All tests passing
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Migrations prepared
- [ ] Environment variables updated
- [ ] Backup taken
- [ ] Rollback plan ready

## Deployment Steps
1. Step 1
2. Step 2
3. Step 3

## Database Migrations
- [ ] No migrations needed
- [ ] Migrations included
- [ ] Migration commands:
  ```bash
  npm run db:migrate
  ```

## Configuration Changes
<!-- New environment variables -->
```env
NEW_VAR=value
```

## Post-Deployment Verification
- [ ] Health check endpoint
- [ ] Critical paths tested
- [ ] Logs checked
- [ ] Metrics monitored

## Rollback Plan
<!-- If something goes wrong -->
1. Rollback step 1
2. Rollback step 2

## Monitoring
<!-- What to watch after deployment -->
- Metrics to monitor:
- Alert thresholds:

## Communication
- [ ] Team notified
- [ ] Users notified (if needed)
- [ ] Status page updated

## Estimated Downtime
- Duration: 
- Maintenance window: 

## Related Issues
- Deployed features: #
```

---

## Usage in `.github/ISSUE_TEMPLATE/`

To use these templates in GitHub, create files in `.github/ISSUE_TEMPLATE/`:

1. `feature_request.md`
2. `bug_report.md`
3. `task.md`
4. `documentation.md`
5. `refactoring.md`
6. `performance.md`
7. `security.md`
8. `deployment.md`

GitHub will automatically present these templates when users create issues.

---

## Related Documents

- [GitHub Workflow](./github-workflow.md) - Complete workflow guide
- [PR Template](./pr-template.md) - Pull request template
