---
created: 2025-12-16T12:00:00Z
created_timestamp: 1765886400
updated: 2025-12-16T12:00:00Z
updated_timestamp: 1765886400
---

# GitHub Workflow - FastAPI Service

Complete specification for GitHub workflows, task creation, pull requests, and project management for the FastAPI Service boilerplate.

## Overview

The FastAPI Service project management approach emphasizes:
- **Spec-driven development**: Specifications before implementation
- **Feature-based organization**: Work organized by business domain (modules)
- **Clean architecture**: Handler → UseCase → Service → Repository layers
- **Clear branching strategy**: Feature branches with issue numbers (`feature/issue-123-description`)
- **Structured PRs**: Comprehensive pull request descriptions
- **Issue tracking**: Detailed issue templates and labels

## Table of Contents

1. [Issue Creation](#issue-creation)
2. [Branch Strategy](#branch-strategy)
3. [Task Breakdown](#task-breakdown)
4. [Pull Request Workflow](#pull-request-workflow)
5. [Code Review Process](#code-review-process)
6. [Labels and Milestones](#labels-and-milestones)
7. [Project Boards](#project-boards)

---

## Issue Creation

### Issue Types

#### 1. Feature Request (`[FEATURE]`)
New functionality or capability.

**Template:**
```markdown
## Feature Description
Brief description of the feature

## User Story
As a [type of user]
I want [goal]
So that [reason]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Considerations
- Dependencies
- API changes
- Database changes
- Security implications

## Related Issues
- #issue_number

## Priority
[ ] Critical
[ ] High
[ ] Medium
[ ] Low

## Estimated Effort
[ ] XS (< 2 hours)
[ ] S (< 1 day)
[ ] M (1-3 days)
[ ] L (1 week)
[ ] XL (> 1 week)
```

#### 2. Bug Report (`[BUG]`)
Something isn't working as expected.

**Template:**
```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04, macOS 14, Windows 11]
- Python version: [e.g., 3.11.5]
- Poetry version: [e.g., 1.7.0]
- Database: [e.g., PostgreSQL 15]
- Branch: [e.g., main]

## Screenshots/Logs
```
[Attach relevant screenshots or logs]
```

## Severity
[ ] Critical (system down)
[ ] High (major functionality broken)
[ ] Medium (workaround available)
[ ] Low (minor issue)

## Related Issues
- #issue_number
```

#### 3. Task (`[TASK]`)
Discrete work item (development, documentation, deployment).

**Template:**
```markdown
## Task Description
Clear description of the task

## Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Context
Why this task is needed

## Implementation Notes
- Technical approach
- Files to modify
- Dependencies

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Related
- Feature: #feature_issue
- Related tasks: #task_issues
```

#### 4. Documentation (`[DOCS]`)
Documentation updates or creation.

**Template:**
```markdown
## Documentation Needed
What documentation needs to be created/updated

## Scope
- [ ] API documentation
- [ ] User guides
- [ ] Technical specifications
- [ ] README updates
- [ ] Code comments

## Target Audience
- Developers
- End users
- System administrators

## Related Code
- Files/features being documented
```

#### 5. Refactoring (`[REFACTOR]`)
Code improvement without changing functionality.

**Template:**
```markdown
## Refactoring Scope
What code needs to be refactored

## Current Issues
- Technical debt
- Performance problems
- Maintainability issues

## Proposed Approach
How the refactoring will be done

## Benefits
- Improved performance
- Better maintainability
- Reduced complexity

## Risks
- Potential side effects
- Testing requirements

## Related Issues
- #issue_number
```

### Issue Naming Conventions

**Format:** `[TYPE] Brief descriptive title`

**Examples:**
- `[FEATURE] Add user password reset flow`
- `[BUG] Report creation fails with invalid coordinates`
- `[TASK] Create database migration for user sessions`
- `[DOCS] Document OAuth integration flow`
- `[REFACTOR] Optimize report query performance`

### Issue Labels

Use GitHub labels to categorize issues:

**Type Labels:**
- `feature` - New functionality
- `bug` - Something broken
- `task` - Work item
- `docs` - Documentation
- `refactor` - Code improvement
- `enhancement` - Improvement to existing feature

**Priority Labels:**
- `priority:critical` - Immediate attention required
- `priority:high` - Important, schedule soon
- `priority:medium` - Normal priority
- `priority:low` - Nice to have

**Status Labels:**
- `status:todo` - Not started
- `status:in-progress` - Currently being worked on
- `status:review` - In code review
- `status:blocked` - Blocked by dependencies
- `status:done` - Completed

**Domain Labels:**
- `domain:auth` - Authentication/authorization
- `domain:reports` - Report management
- `domain:users` - User management
- `domain:api` - API-related
- `domain:database` - Database changes
- `domain:deployment` - Deployment/infrastructure

**Effort Labels:**
- `effort:xs` - < 2 hours
- `effort:s` - < 1 day
- `effort:m` - 1-3 days
- `effort:l` - 1 week
- `effort:xl` - > 1 week

---

## Branch Strategy

### Branch Types

#### 1. Main Branch (`main`)
- Production-ready code
- Always deployable
- Protected (requires PR + reviews)

#### 2. Development Branch (`develop`)
- Integration branch
- Latest development changes
- All features merge here first

#### 3. Feature Branches (`feature/`)
- New features
- Format: `feature/issue-<number>-<short-description>` (matches existing convention)
- Examples:
  - `feature/issue-14-optimize-ai-documentation`
  - `feature/issue-42-user-password-reset`
  - `feature/issue-123-weather-module`

#### 4. Bug Fix Branches (`fix/`)
- Bug fixes
- Format: `fix/issue-<number>-<short-description>` (matches existing convention)
- Examples:
  - `fix/issue-56-fix-coordinate-validation`
  - `fix/issue-78-session-expiration-issue`

#### 5. Hotfix Branches (`hotfix/`)
- Critical production fixes
- Branch from `main`, merge to both `main` and `develop`
- Format: `hotfix/issue-<number>-<short-description>`
- Examples:
  - `hotfix/issue-91-security-vulnerability`
  - `hotfix/issue-102-database-connection-leak`

#### 6. Task Branches (`task/` or `chore/`)
- General tasks (documentation, refactoring)
- Format: `task/issue-<number>-<short-description>` or `chore/issue-<number>-<short-description>`
- Examples:
  - `task/issue-15-update-api-documentation`
  - `chore/issue-67-refactor-auth-service`

#### 7. Documentation Branches (`docs/`)
- Documentation-only changes
- Format: `docs/issue-<number>-<short-description>` (matches existing convention)
- Examples:
  - `docs/issue-33-authentication-guide`
  - `docs/issue-89-deployment-procedures`

### Branch Creation Workflow

1. **Create Issue First**
   - Always create an issue before starting work
   - Get issue number (e.g., #14)

2. **Create Branch from Latest**
   ```bash
   # Update main branch (or develop if using git-flow)
   git checkout main
   git pull origin main
   
   # Create feature branch with issue number
   git checkout -b feature/issue-14-optimize-ai-documentation
   ```

3. **Work on Branch**
   - Commit regularly with clear messages
   - Reference issue number in commits

4. **Keep Branch Updated**
   ```bash
   # Regularly sync with main (or develop if using git-flow)
   git checkout main
   git pull origin main
   git checkout feature/issue-14-optimize-ai-documentation
   git rebase main
   ```

5. **Push Branch**
   ```bash
   git push origin feature/issue-14-optimize-ai-documentation
   ```

### Branch Naming Rules

- **Use kebab-case**: `feature/my-feature-name`
- **Include issue number**: `feature/issue-123-feature-name` (matches existing convention)
- **Be descriptive but brief**: Max 50 characters
- **Use imperative mood**: `add-password-reset` not `adding-password-reset`

**Good Examples:**
- `feature/issue-42-add-oauth-providers`
- `fix/issue-56-fix-report-validation`
- `task/issue-67-refactor-user-service`
- `docs/issue-789-update-readme`

**Bad Examples:**
- `feature/new-stuff` (no issue number, vague)
- `my_feature_branch` (wrong format)
- `feature/implementing-the-new-user-authentication-system-with-oauth` (too long)
- `feature/123-feature-name` (missing "issue-" prefix)

---

## Task Breakdown

### Creating Tasks from Features

When implementing a feature, break it down into tasks following this structure:

1. **Create Feature Specification**
   - Location: `specs/features/<feature-name>/`
   - Files:
     - `requirements.md` - User stories, acceptance criteria
     - `design.md` - Technical architecture
     - `tasks.md` - Implementation tasks

2. **Define Tasks in `tasks.md`**
   - Group tasks by phase
   - Assign status: ✅ Complete, 🚧 In Progress, ⏸️ Blocked, 📋 Not Started
   - Estimate effort
   - List dependencies

3. **Create GitHub Issues for Each Task**
   - One issue per major task
   - Reference feature issue in description
   - Apply appropriate labels

### Task Format in Specifications

```markdown
## Phase 1: Database Setup

### Task 1.1: Create Users Table
**Status:** 📋 Not Started  
**Effort:** 2 hours  
**Dependencies:** None  
**Issue:** #45

- Create SQLAlchemy model for users table
- Add indexes
- Generate Alembic migration
- Apply migration

**Files:**
- `src/fastapi_service/dbase/sql/models/user.py`
- `alembic/versions/XXXX_create_users_table.py`
```

### Task Dependencies

Track dependencies clearly:

```markdown
### Task 2.3: Create Auth Service
**Status:** 📋 Not Started
**Effort:** 4 hours
**Dependencies:** Task 2.1 (Password Hashing), Task 2.2 (User Repository)
**Issue:** #48

Cannot start until password hashing and user repository are complete.
```

---

## Pull Request Workflow

### Creating Pull Requests

#### 1. Before Creating PR

**Checklist:**
- [ ] All commits follow commit message conventions
- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No linter errors
- [ ] Types check passes (`npm run check:types`)
- [ ] Branch is up to date with target branch

**Run checks:**
```bash
make lint-all          # Run all linting checks
make format            # Format code (black + isort)
make test              # Run all tests
make test-coverage     # Run tests with coverage
```

#### 2. PR Title Format

**Format:** `[TYPE] Brief description (closes #issue)`

**Examples:**
- `[FEATURE] Add user password reset flow (closes #42)`
- `[BUG] Fix report coordinate validation (closes #56)`
- `[TASK] Create database migration for sessions (closes #67)`
- `[DOCS] Document OAuth integration (closes #33)`

#### 3. PR Description Template

```markdown
## Description
Brief description of changes

## Related Issue
Closes #issue_number

## Type of Change
- [ ] Feature (new functionality)
- [ ] Bug fix
- [ ] Task (development work)
- [ ] Documentation
- [ ] Refactoring
- [ ] Performance improvement
- [ ] Test addition

## Changes Made
- Change 1
- Change 2
- Change 3

## Implementation Details
### Architecture
- Component changes
- New patterns introduced

### Database Changes
- [ ] Schema changes
- [ ] Alembic migrations included
- [ ] Migration files listed

### API Changes
- [ ] New endpoints
- [ ] Modified endpoints
- [ ] Breaking changes

## Testing
### Manual Testing
- [ ] Tested locally
- [ ] Tested all edge cases
- [ ] Verified error handling

### Automated Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Documentation
- [ ] Code comments added
- [ ] API docs updated
- [ ] README updated (if needed)
- [ ] Specifications updated

## Screenshots/Demos
<!-- Add screenshots or demo videos if applicable -->

## Deployment Notes
- Environment variables changed
- Database migrations needed
- Special deployment steps

## Checklist
- [ ] Code follows project conventions
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests passing
- [ ] Branch up to date with target

## Reviewers
@username1 @username2
```

#### 4. PR Labels

Apply same labels as issues:
- Type: `feature`, `bug`, `task`, `docs`, `refactor`
- Priority: `priority:high`, `priority:medium`, `priority:low`
- Domain: `domain:auth`, `domain:reports`, etc.

#### 5. Draft PRs

Use draft PRs for work in progress:
- Click "Create draft pull request"
- Mark as "Ready for review" when complete
- Use for early feedback

### PR Size Guidelines

**Ideal PR size:**
- **Small (< 200 lines)**: Preferred
- **Medium (200-500 lines)**: Acceptable
- **Large (500-1000 lines)**: Needs justification
- **Huge (> 1000 lines)**: Break into multiple PRs

**For large changes:**
1. Break into logical chunks
2. Create multiple PRs
3. Order PRs with dependencies
4. Reference related PRs

---

## Code Review Process

### Review Timeline

- **Initial review**: Within 24 hours
- **Follow-up reviews**: Within 12 hours
- **Urgent PRs**: Tag as `priority:critical` for same-day review

### Reviewer Responsibilities

#### 1. Code Quality
- [ ] Follows project conventions
- [ ] No code smells
- [ ] Proper error handling
- [ ] Efficient implementation
- [ ] No security vulnerabilities

#### 2. Testing
- [ ] Tests cover new code
- [ ] Tests are meaningful
- [ ] Edge cases considered
- [ ] All tests passing

#### 3. Documentation
- [ ] Code is self-documenting
- [ ] Complex logic commented
- [ ] API docs updated
- [ ] README updated if needed

#### 4. Architecture
- [ ] Follows clean architecture
- [ ] Proper separation of concerns
- [ ] No tight coupling
- [ ] Reusable components

### Review Comments

**Use constructive feedback:**

✅ **Good:**
- "Consider using `async/await` here for better readability"
- "This could be simplified using the existing `UserRepository` method"
- "Great error handling! Could we add a test for the edge case where...?"

❌ **Bad:**
- "This is wrong"
- "I don't like this"
- "Rewrite this"

**Comment types:**
- **Blocking**: Must be fixed before merge
- **Non-blocking**: Suggestions for improvement
- **Question**: Seeking clarification
- **Praise**: Acknowledging good work

**Use labels in comments:**
- `[BLOCKING]` - Must be addressed
- `[SUGGESTION]` - Nice to have
- `[QUESTION]` - Seeking clarification
- `[NITPICK]` - Minor style issue

### Approval Process

**Requirements for merge:**
1. **Code review**: At least 1 approval
2. **Tests**: All passing (`make test`)
3. **Linting**: No errors (`make lint-all`)
4. **Code formatting**: Applied (`make format`)
5. **Conflicts**: Resolved
6. **Documentation**: Updated

**For critical changes:**
- Require 2+ approvals
- Senior developer approval
- Extended testing period

---

## Labels and Milestones

### Label Structure

#### Type Labels
```
feature (🚀 blue)
bug (🐛 red)
task (📋 white)
docs (📚 green)
refactor (♻️ yellow)
enhancement (✨ purple)
```

#### Priority Labels
```
priority:critical (🔥 dark red)
priority:high (⚡ red)
priority:medium (⚠️ yellow)
priority:low (💡 blue)
```

#### Status Labels
```
status:todo (📝 light gray)
status:in-progress (🚧 yellow)
status:review (👀 purple)
status:blocked (🚫 red)
status:done (✅ green)
```

#### Domain Labels
```
domain:auth (🔐 blue)
domain:reports (📊 green)
domain:users (👤 purple)
domain:api (🔌 orange)
domain:database (💾 brown)
domain:deployment (🚀 cyan)
```

#### Effort Labels
```
effort:xs (⏱️ light green) - < 2 hours
effort:s (⏱️ green) - < 1 day
effort:m (⏱️ yellow) - 1-3 days
effort:l (⏱️ orange) - 1 week
effort:xl (⏱️ red) - > 1 week
```

### Milestones

Create milestones for:
- **Version releases**: v1.0.0, v1.1.0, etc.
- **Feature sets**: Authentication System, Report Management
- **Sprint cycles**: Sprint 1, Sprint 2, etc.

**Milestone format:**
```
Title: v1.0.0 - Initial Release
Due date: 2025-03-01
Description: 
Complete authentication system, report management, and basic API endpoints.

Goals:
- User authentication (local + OAuth)
- Report CRUD operations
- Basic API documentation
- Deployment setup
```

---

## Project Boards

**IMPORTANT:** All issues MUST be added to the **Pulse GitHub Project** for tracking.

See `specs/workflows/project-management.md` for detailed project management guidelines.

### Board Structure

#### 1. Kanban Board (Main Development)

**Columns:**
1. **Backlog** - All issues not yet started
2. **Todo** - Ready to be worked on
3. **In Progress** - Currently being worked on
4. **Review** - In code review
5. **Testing** - Being tested
6. **Done** - Completed

**Automation:**
- New issues → Backlog
- Issue assigned → Todo
- PR created → Review
- PR merged → Done

#### 2. Sprint Board

**Columns:**
1. **Sprint Backlog** - Selected for this sprint
2. **In Progress** - Being worked on
3. **Review** - In code review
4. **Done** - Completed this sprint

**Sprint cycle:**
- Duration: 2 weeks
- Planning: Monday
- Review: Friday (week 2)
- Retrospective: Friday (week 2)

#### 3. Feature Board

Track major features across sprints.

**Columns:**
1. **Planned** - Feature specifications created
2. **In Development** - Implementation in progress
3. **Testing** - Feature testing
4. **Released** - Feature deployed

### Project Board Best Practices

1. **Update regularly**: Move cards as work progresses
2. **One issue per task**: Don't duplicate work
3. **Link PRs to issues**: Automatic status updates
4. **Use milestones**: Track progress toward releases
5. **Close stale issues**: Review and close inactive issues monthly

---

## Commit Message Conventions

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Maintenance tasks
- `build`: Build system changes
- `ci`: CI/CD changes

### Examples

```
feat(auth): add password reset flow

Implement password reset using email tokens.
- Add password reset endpoint
- Create email service
- Add token validation

Closes #42
```

```
fix(reports): validate coordinates properly

Fix bug where invalid coordinates were accepted.
Latitude must be between -90 and 90.
Longitude must be between -180 and 180.

Fixes #56
```

```
docs(api): update authentication guide

Add OAuth provider setup instructions.
Update API examples with bearer token format.

Related to #33
```

---

## Workflow Summary

### Feature Development Flow

```
1. Create Feature Issue [FEATURE] → #42
2. Create Feature Specifications
   - specs/features/password-reset/requirements.md
   - specs/features/password-reset/design.md
   - specs/features/password-reset/tasks.md
3. Break Down Into Tasks → Issues #45, #46, #47
4. Create Feature Branch → feature/issue-42-user-password-reset
5. Implement Tasks → Commits (with "Closes #42" footer)
6. Create Pull Request → PR #48
7. Code Review → Reviewers approve
8. Merge to Main → Branch deleted
9. Test → QA
10. Deploy → Release
```

### Bug Fix Flow

```
1. Create Bug Issue [BUG] → #56
2. Reproduce Bug → Document steps
3. Create Bugfix Branch → fix/issue-56-coordinate-validation
4. Fix Bug → Commits (with "Fixes #56" footer)
5. Add Test → Prevent regression
6. Create Pull Request → PR #57
7. Code Review → Approve
8. Merge to Main → Test
9. Deploy → Release
```

### Hotfix Flow

```
1. Create Hotfix Issue [BUG] priority:critical → #91
2. Create Hotfix Branch from Main → hotfix/issue-91-security-patch
3. Fix Issue → Minimal changes
4. Create PR to Main → PR #92
5. Emergency Review → Fast-track
6. Merge to Main → Deploy immediately
7. Backport to Develop → Keep in sync (if using git-flow)
```

---

## Best Practices

### General Guidelines

1. **One issue, one branch** - Don't mix unrelated changes
2. **Small, focused PRs** - Easier to review and test
3. **Clear descriptions** - Save reviewers time
4. **Reference issues** - Link PRs to issues
5. **Keep branches updated** - Rebase regularly
6. **Delete merged branches** - Keep repository clean
7. **Use draft PRs** - For early feedback
8. **Automate checks** - Linting, tests, type checking
9. **Review promptly** - Don't block teammates
10. **Be respectful** - Constructive feedback only

### Anti-Patterns to Avoid

❌ **Creating branches without issues**
❌ **Working directly on main/develop**
❌ **Huge PRs (> 1000 lines)**
❌ **Vague commit messages**
❌ **Skipping code review**
❌ **Merging with failing tests**
❌ **Ignoring review comments**
❌ **Not updating documentation**
❌ **Not testing locally before PR**
❌ **Leaving stale branches**

---

## Tools and Automation

### GitHub Actions

Automate workflows with GitHub Actions:

1. **CI/CD Pipeline**
   - Run tests on PR (`make test`)
   - Lint code (`make lint-all`)
   - Format check (`make format`)
   - Build verification

2. **Auto-labeling**
   - Label PRs based on files changed
   - Label issues based on keywords

3. **Stale Issue Management**
   - Close inactive issues after 60 days
   - Warn after 45 days

4. **Deployment**
   - Auto-deploy to staging on merge to develop (if using git-flow)
   - Auto-deploy to production on merge to main

### GitHub CLI

Use GitHub CLI for faster workflows:

```bash
# Create issue
gh issue create --title "[FEATURE] Add user roles" --body "Description"

# Create PR
gh pr create --title "[FEATURE] Add user roles (closes #42)" --body-file specs/workflows/pr-template.md

# Review PR
gh pr review 48 --approve
gh pr review 48 --request-changes --body "Please fix..."

# Merge PR
gh pr merge 48 --squash --delete-branch
```

---

## Related Documents

- [Features Specifications](../features/README.md)
- [Conventions](../conventions/README.md)
- [Documentation Standards](../conventions/07-documentation-standards.md)
- [Testing Standards](../conventions/04-testing-standards.md)

---

## Changelog

All changes to this workflow should be documented in `specs/CHANGELOG.md`.
