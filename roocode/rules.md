# Roocode Rules

This document defines the rules and guidelines for interacting with AI agents (roocode) in this project.

## Rule #1: Session Documentation

**All conversations with AI agents must be documented in the `docs/sessions/{YYYYMMDD}/` folder.**

### Requirements:

1. **Folder Structure**: Create a new folder for each day using the `YYYYMMDD` format
   - Example: `20251229` for December 29, 2025
   - Example: `20260115` for January 15, 2026

2. **File Format**: Save conversation logs as markdown files (`.md`)
   - Naming options:
     - `session-{number}.md` (e.g., `session-01.md`, `session-02.md`)
     - `{topic}.md` (e.g., `api-refactoring.md`, `database-design.md`)

3. **Content Guidelines**: Each session file should include:
   - Date and time of the conversation
   - Context or goal of the session
   - Key decisions made
   - Actions taken
   - Outcomes or next steps

### Example Structure:

```
docs/sessions/
├── 20251229/
│   ├── session-01.md
│   └── initial-setup.md
├── 20251230/
│   └── feature-planning.md
└── 20260102/
    ├── session-01.md
    └── bug-fixes.md
```

### Session File Template:

```markdown
# Session: [Topic/Title]

**Date**: YYYY-MM-DD
**Time**: HH:MM (Timezone)
**Agent**: roocode

## Context
Brief description of what you're trying to accomplish in this session.

## Conversation Summary
Key points discussed and decisions made.

## Actions Taken
- Action item 1
- Action item 2

## Outcomes
What was accomplished or learned.

## Next Steps
- [ ] Follow-up task 1
- [ ] Follow-up task 2
```

---

## Rule #2: Development Principles

**Follow greenfield development philosophy with fail-fast approach and comprehensive testing.**

### Greenfield Philosophy:
- Write code as if starting fresh, unburdened by legacy constraints
- Favor simple, elegant solutions over complex workarounds
- Build for the future, not just the immediate need
- Design with extensibility in mind

### Fail-Fast Approach:
- Validate inputs early and explicitly
- Raise exceptions immediately when assumptions are violated
- Never silently ignore errors or return None without clear documentation
- Make failures obvious and debuggable

### Testing Philosophy:
- Tests are executable documentation
- Write tests for integration points and critical business logic
- Skip tests for simple CRUD operations and one-time scripts
- See [`testing.md`](testing.md) for comprehensive testing guidelines

### Code Quality:
- Self-descriptive code > comments
- Clear naming > clever shortcuts
- Explicit > implicit
- See [`coding-standards.md`](coding-standards.md) for detailed standards

---

## Rule #3: Git Awareness

**Always check the last 3 commits before making changes to understand code evolution.**

### Context from History:
```bash
# Check recent commits
git log -3 --oneline --decorate

# See what changed recently
git log -3 --stat

# Understand specific changes
git show HEAD~2
```

### Why This Matters:
- Understand the trajectory of development
- Avoid reverting recent bug fixes
- Learn from the evolution of the codebase
- See patterns in how the team approaches problems

### When Making Changes:
1. Check recent commits in the area you're modifying
2. Read commit messages for context
3. Understand why previous changes were made
4. Ensure your changes align with the direction

See [`git-usage.md`](git-usage.md) for complete git workflows for AI agents.

---

## Rule #4: Shell Environment

**All scripts and commands must be compatible with bash shell.**

### Requirements:
- Use bash for all shell scripts
- Avoid bash-specific features when possible for portability
- Test scripts in the actual execution environment (Docker/dev container)

### Script Template:
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Script logic here
```

### Command Execution:
- Use `docker compose run --rm dev` for Python scripts
- Use `bash scripts/script-name.sh` for shell scripts
- See [`automode.md`](automode.md) for execution patterns

---

## Future Rules

Additional rules will be added here as the project evolves.
