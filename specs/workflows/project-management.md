---
created: 2025-12-16T07:45:00Z
created_timestamp: 1765887900
updated: 2025-12-16T07:45:00Z
updated_timestamp: 1765887900
---

# Project Management - FastAPI Service GitHub Project

## Overview

All tasks, issues, and epics in this repository **SHOULD** be added to a GitHub Project board for tracking and organization.

## GitHub Project Details

**Project Name:** FastAPI Service (or your project name)
**Repository:** [Your repository path]
**Board Type:** Kanban with Sprint tracking

## Board Structure

### Columns

1. **Backlog** - All new issues
2. **Todo** - Ready to be worked on (current sprint)
3. **In Progress** - Currently being worked on
4. **Review** - In code review
5. **Testing** - Being tested
6. **Done** - Completed

## Issue Management Rules

### Rule 1: All Issues Must Be in Project

**Every issue created must be added to the Pulse project board.**

- Epics → Backlog
- Tasks → Backlog (then move to Todo when ready)
- Bugs → Todo (if urgent) or Backlog
- Documentation → Backlog

### Rule 2: Update Status Regularly

Move cards through the board as work progresses:
- Assigned → Todo
- Start work → In Progress
- Create PR → Review
- PR approved → Testing
- Merged → Done

### Rule 3: Link Issues and PRs

- Every PR must reference its issue: `Closes #123`
- Every sub-issue must reference its epic: `Parent Epic: #21`

## Adding Issues to Project

### Via GitHub Web UI

1. Open issue page
2. Click "Projects" in right sidebar
3. Select "Pulse" project
4. Choose column (usually "Backlog")

### Via GitHub CLI

```bash
# Add single issue to project
gh project item-add <PROJECT_NUMBER> \
  --owner <YOUR_ORG> \
  --url https://github.com/<YOUR_ORG>/<REPO_NAME>/issues/<ISSUE_NUMBER>

# Add multiple issues (example for #21-#26)
for i in {21..26}; do
  gh project item-add <PROJECT_NUMBER> \
    --owner <YOUR_ORG> \
    --url https://github.com/<YOUR_ORG>/<REPO_NAME>/issues/$i
done
```

### Via GitHub API

```bash
# Get project ID first
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/<YOUR_ORG>/<REPO_NAME>/projects

# Add issue to project
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/projects/columns/<COLUMN_ID>/cards \
  -d '{"content_id":<ISSUE_ID>,"content_type":"Issue"}'
```

## Current Issues to Add

### Recently Created (Pending Project Addition)

**Epic #21: [Feature Name]**
- [x] Created on GitHub
- [ ] Added to project board
- [ ] Status: Backlog

**Sub-Issues:**
- [x] #22: [Sub-task 1]
- [x] #23: [Sub-task 2]
- [x] #24: [Sub-task 3]

**Action Required:** Add issues to project board as needed.

## Automation

### GitHub Actions for Project Management

Consider setting up automation:

```yaml
# .github/workflows/add-to-project.yml
name: Add to Pulse Project

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/<YOUR_ORG>/projects/<PROJECT_NUMBER>
          github-token: ${{ secrets.ADD_TO_PROJECT_PAT }}
```

## Best Practices

### For Issue Creators

1. **Always specify** which project when creating issues
2. **Set appropriate labels** (epic, task, bug, etc.)
3. **Link to parent epic** for sub-issues
4. **Estimate effort** (XS, S, M, L, XL)
5. **Set priority** (P0, P1, P2, P3)

### For Project Managers

1. **Review Backlog** weekly
2. **Prioritize Todo** column for upcoming sprint
3. **Close Done** items after verification
4. **Archive old** completed items monthly
5. **Update milestones** for releases

### For Developers

1. **Move to In Progress** when starting work
2. **Update regularly** (daily if possible)
3. **Comment on issues** with progress updates
4. **Link PRs** to issues using "Closes #123"
5. **Request review** by moving to Review column

## Milestones

Link issues to milestones for release tracking:

- **v1.0.0 - MVP** (Auth + Basic Features)
- **v1.1.0 - Email Integration** (Email Service + Password Reset)
- **v1.2.0 - Security** (2FA + Rate Limiting)
- **v2.0.0 - Advanced Features** (Magic Link + Account Management)

## Sprint Planning

### Sprint Cycle (2 weeks)

**Week 1:**
- Monday: Sprint planning
- Tuesday-Friday: Development

**Week 2:**
- Monday-Thursday: Development + Testing
- Friday: Sprint review + Retrospective

### Sprint Board Usage

1. **Planning**: Move selected issues from Backlog → Sprint Backlog
2. **Daily**: Update In Progress items
3. **Review**: Demo completed items
4. **Retrospective**: Archive sprint, plan next

## Reporting

### Weekly Status Update

Generate weekly reports:

```bash
# Issues completed this week
gh issue list --state closed --search "closed:>$(date -d '7 days ago' +%Y-%m-%d)"

# Issues in progress
gh issue list --label "status:in-progress"

# Issues blocked
gh issue list --label "status:blocked"
```

## Integration with AI Tools

**For Cursor AI / GitHub Copilot:**

When creating issues via AI tools:
1. Always mention "add to Pulse project"
2. Include project board column in issue metadata
3. Link to relevant epics and milestones

**Example prompt:**
```
Create a task for implementing password reset.
Add to project board (Backlog column).
Link to Epic #21.
Set labels: task, authentication, priority:high.
```

## Checklist for New Issues

- [ ] Issue created on GitHub
- [ ] Added to Pulse project board
- [ ] Correct column selected (usually Backlog)
- [ ] Labels applied (type, priority, effort)
- [ ] Parent epic linked (for sub-issues)
- [ ] Milestone assigned (if applicable)
- [ ] Time estimates added
- [ ] Assigned to team member (if known)

---

## Quick Reference

**Add to Project:** Right sidebar → Projects → Select "Pulse"
**Move Card:** Drag and drop on board
**Link to Epic:** Issue description: `Parent Epic: #21`
**Close Issue:** PR description: `Closes #123`
**View Board:** https://github.com/orgs/<YOUR_ORG>/projects/<PROJECT_NUMBER>
