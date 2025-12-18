---
created: 2025-12-16T12:00:00Z
created_timestamp: 1765886400
updated: 2025-12-16T12:00:00Z
updated_timestamp: 1765886400
---

# Pull Request Template

Standard pull request template for FastAPI Service. Copy this template when creating PRs.

## Default PR Template

Save as `.github/pull_request_template.md`:

```markdown
## Description
<!-- Brief description of the changes in this PR -->

## Related Issue
<!-- Link to the issue this PR addresses -->
Closes #

## Type of Change
<!-- Check all that apply -->
- [ ] 🚀 Feature (new functionality)
- [ ] 🐛 Bug fix
- [ ] 📋 Task (development work)
- [ ] 📚 Documentation
- [ ] ♻️ Refactoring
- [ ] ⚡ Performance improvement
- [ ] ✨ Enhancement
- [ ] 🧪 Test addition
- [ ] 🔧 Configuration change

## Changes Made
<!-- List the main changes in bullet points -->
- Change 1
- Change 2
- Change 3

## Implementation Details

### Architecture Changes
<!-- Describe any architectural changes -->
- Component changes:
- New patterns introduced:
- Dependencies added:

### Database Changes
- [ ] Schema changes
- [ ] Migrations included (list files)
- [ ] Seeders updated

### API Changes
- [ ] New endpoints
- [ ] Modified endpoints
- [ ] Breaking changes (describe)
- [ ] API documentation updated

## Testing

### Manual Testing
- [ ] Tested locally
- [ ] Tested all user flows
- [ ] Tested edge cases
- [ ] Verified error handling
- [ ] Tested with different user roles (if applicable)

### Test Cases Covered
<!-- List specific scenarios tested -->
1. Test case 1
2. Test case 2
3. Test case 3

### Automated Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing locally
- [ ] Test coverage maintained/improved

## Code Quality

### Linting & Type Checking
- [ ] `make lint-all` passes (black, isort, flake8)
- [ ] `make format` applied (black + isort)
- [ ] `mypy` passes (if type checking enabled)
- [ ] No new warnings introduced

### Code Review Self-Check
- [ ] Code follows project conventions
- [ ] Self-review completed
- [ ] Complex logic documented
- [ ] No commented-out code
- [ ] No console.log/debug statements
- [ ] No hardcoded values (use env vars)

## Documentation

- [ ] Code comments added for complex logic
- [ ] API documentation updated (`docs/api/`)
- [ ] README updated (if needed)
- [ ] Specifications updated (`specs/`)
- [ ] Migration guide provided (for breaking changes)

## Security

- [ ] No sensitive data exposed
- [ ] Input validation added
- [ ] Authentication/authorization checked
- [ ] SQL injection prevented
- [ ] XSS prevention implemented
- [ ] No new security vulnerabilities

## Performance

- [ ] No performance regressions
- [ ] Database queries optimized
- [ ] Indexes added (if needed)
- [ ] Caching considered
- [ ] Large operations paginated

## Deployment

### Environment Variables
<!-- List any new or changed environment variables -->
```env
# None
# OR
NEW_VAR=default_value  # Description
```

### Database Migrations
<!-- Migration commands needed -->
```bash
# None
# OR
make db-upgrade  # Apply Alembic migrations
```

### Special Deployment Steps
<!-- Any special steps needed for deployment -->
1. Step 1
2. Step 2

### Rollback Plan
<!-- How to rollback if something goes wrong -->
- Rollback steps:

## Screenshots/Demos
<!-- Add screenshots or demo videos if applicable -->
<!-- Use drag-and-drop to add images -->

## Breaking Changes
<!-- List any breaking changes and migration path -->
- [ ] No breaking changes
- [ ] Breaking changes (describe below)

**Breaking changes:**
- 

**Migration guide:**
- 

## Dependencies
<!-- List PRs or issues this depends on -->
- Depends on: #
- Blocks: #
- Related: #

## Checklist

### Before Requesting Review
- [ ] Branch is up to date with target branch
- [ ] All commits follow commit message conventions
- [ ] Code is self-documenting
- [ ] Tests cover new functionality
- [ ] Documentation is updated
- [ ] No merge conflicts

### Reviewer Focus Areas
<!-- Guide reviewers on what to focus on -->
- Please review: [specific areas]
- Pay attention to: [specific concerns]

## Additional Notes
<!-- Any additional context or notes for reviewers -->

---

## Reviewers
<!-- Tag relevant reviewers -->
@reviewer1 @reviewer2

<!-- Auto-closes the linked issue when PR is merged -->
```

---

## PR Title Format

Use this format for PR titles:

```
[TYPE] Brief description (closes #issue)
```

**Examples:**
- `[FEATURE] Add user password reset flow (closes #42)`
- `[BUG] Fix report coordinate validation (closes #56)`
- `[TASK] Create database migration for sessions (closes #67)`
- `[DOCS] Document OAuth integration (closes #33)`
- `[REFACTOR] Optimize report query performance (closes #78)`

---

## Specialized PR Templates

### Feature PR Template

For major features with extensive changes:

```markdown
## 🚀 Feature: [Feature Name]

### Overview
<!-- High-level description of the feature -->

### Specifications
- Requirements: `specs/features/[feature]/requirements.md`
- Design: `specs/features/[feature]/design.md`
- Tasks: `specs/features/[feature]/tasks.md`

### User Stories Implemented
- [ ] As a [user], I want [goal] so that [reason]
- [ ] As a [user], I want [goal] so that [reason]

### Components Changed
- **Handlers**: [list API handlers]
- **Use Cases**: [list use cases]
- **Services**: [list services]
- **Repositories**: [list repositories if any]
- **Schemas**: [list Pydantic models]

### API Endpoints
#### New Endpoints
- `POST /api/v1/[endpoint]` - Description
- `GET /api/v1/[endpoint]` - Description

#### Modified Endpoints
- `PUT /api/v1/[endpoint]` - Changes

### Database Changes
- Tables added/modified: [list]
- Alembic migrations: [files in alembic/versions/]
- Indexes added: [list]

### Testing Strategy
- Unit tests: [count] added, [count] updated
- Integration tests: [count] added
- Coverage: [percentage]

### Documentation
- [ ] API documentation
- [ ] User guide
- [ ] Technical specs
- [ ] Code examples

### Screenshots
[Add UI screenshots if applicable]

### Performance Impact
- Response time: [measurement]
- Database queries: [count]
- Memory usage: [measurement]

Closes #[issue]
```

### Bug Fix PR Template

For bug fixes:

```markdown
## 🐛 Bug Fix: [Bug Description]

### Bug Report
Issue: #[issue_number]

### Problem
<!-- What was broken -->

### Root Cause
<!-- Why it was broken -->

### Solution
<!-- How it's fixed -->

### Changes Made
- File 1: [changes]
- File 2: [changes]

### Test Added
<!-- Regression test to prevent this bug from reoccurring -->
- Test file: [path]
- Test description: [what it tests]

### Verification
- [ ] Bug reproduced before fix
- [ ] Bug no longer occurs after fix
- [ ] Regression test added
- [ ] No side effects

### Impact
- [ ] No breaking changes
- [ ] No database changes
- [ ] No API changes

Fixes #[issue]
```

### Documentation PR Template

For documentation-only changes:

```markdown
## 📚 Documentation: [Topic]

### What's Documented
<!-- What is being added/updated -->

### Scope
- [ ] API documentation
- [ ] User guides
- [ ] Technical specifications
- [ ] Code comments
- [ ] README
- [ ] Examples

### Files Changed
- `docs/[file]` - [description]
- `specs/[file]` - [description]

### Review Focus
Please review for:
- [ ] Accuracy
- [ ] Clarity
- [ ] Completeness
- [ ] Formatting
- [ ] Examples

### Screenshots
[If applicable]

Closes #[issue]
```

### Refactoring PR Template

For code refactoring:

```markdown
## ♻️ Refactoring: [Component/Area]

### Motivation
<!-- Why this refactoring is needed -->

### Changes
- [ ] Extract methods
- [ ] Simplify logic
- [ ] Remove duplication
- [ ] Improve naming
- [ ] Update patterns

### Before/After
**Before:**
```python
# Old code
```

**After:**
```python
# New code
```

### Benefits
- Improved maintainability
- Better performance
- Clearer code
- Reduced complexity

### Verification
- [ ] All existing tests still pass
- [ ] No functional changes
- [ ] Performance maintained or improved
- [ ] Code coverage maintained

### Risk Assessment
- Risk level: [ ] Low [ ] Medium [ ] High
- Mitigation: [if any risks]

Closes #[issue]
```

---

## PR Labels

Apply these labels to PRs:

**Type:**
- `feature`
- `bug`
- `task`
- `docs`
- `refactor`
- `performance`

**Priority:**
- `priority:critical`
- `priority:high`
- `priority:medium`
- `priority:low`

**Status:**
- `status:draft` (for draft PRs)
- `status:review` (ready for review)
- `status:changes-requested`
- `status:approved`

**Domain:**
- `domain:auth`
- `domain:reports`
- `domain:api`
- `domain:database`
- etc.

---

## PR Review Checklist

For reviewers, use this checklist:

```markdown
## Review Checklist

### Code Quality
- [ ] Code follows project conventions
- [ ] Naming is clear and consistent
- [ ] No code duplication
- [ ] Error handling is appropriate
- [ ] No commented-out code

### Architecture
- [ ] Follows clean architecture
- [ ] Proper separation of concerns
- [ ] No tight coupling
- [ ] Dependencies are appropriate

### Security
- [ ] Input validation present
- [ ] Authentication/authorization correct
- [ ] No sensitive data exposed
- [ ] SQL injection prevented

### Performance
- [ ] No obvious performance issues
- [ ] Database queries optimized
- [ ] Appropriate indexes used

### Testing
- [ ] Tests are comprehensive
- [ ] Tests are meaningful
- [ ] Edge cases covered
- [ ] All tests passing

### Documentation
- [ ] Code is documented
- [ ] API docs updated
- [ ] Complex logic explained
- [ ] Examples provided

### Overall
- [ ] PR description is clear
- [ ] Changes match issue requirements
- [ ] No scope creep
- [ ] Ready to merge
```

---

## Related Documents

- [GitHub Workflow](./github-workflow.md) - Complete workflow guide
- [Issue Templates](./issue-templates.md) - Issue templates
- [Code Review Guide](./code-review-guide.md) - Review best practices
