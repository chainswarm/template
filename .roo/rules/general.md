# General Development Rules

These rules apply to ALL Flow modes (architect, code, debug, ask, orchestrator).

## Rule #1: Development Principles

### Greenfield Mindset
- Assume new system development
- No legacy migrations
- No backward compatibility layers
- No fallback code

### Fail-Fast Philosophy
- Raise exceptions immediately
- No default values
- No silent failures
- ValueError for invalid inputs
- Log errors at highest entry points

### Code Quality
- Self-descriptive naming
- No redundant documentation
- Domain-focused code

### Testing Approach
- Integration tests recommended
- TDD for bug fixes
- Tests only when valuable
- User-driven validation

## Rule #2: Git Awareness

Agents should check git history before making changes:

```bash
# Check last 3 commits
git log --oneline -3

# See what changed
git diff HEAD~3..HEAD path/to/file.py
```

## Rule #3: Shell Environment

**Use bash for all scripts and commands** (not PowerShell, cmd).

---

See also:
- [`coding-standards.md`](.roo/rules/coding-standards.md) - NEVER/ALWAYS principles
- [`testing.md`](.roo/rules/testing.md) - Testing philosophy
- [`automode.md`](.roo/rules/automode.md) - Execution patterns
- [`git-usage.md`](.roo/rules/git-usage.md) - Git workflows
