# RooFlow Template Usage Guide

Complete guide to using the RooFlow Extended Template.

---

## Table of Contents

1. [Installation](#installation)
2. [First-Time Setup](#first-time-setup)
3. [Memory Bank](#memory-bank)
4. [Flow Modes](#flow-modes)
5. [Infrastructure](#infrastructure)
6. [Development Workflow](#development-workflow)
7. [Best Practices](#best-practices)

---

## Installation

### Run the Installer

```bash
bash install_rooflow_conport.sh
```

The installer will:
1. Clone RooFlow repository
2. Copy Flow mode configurations
3. Install generation scripts
4. **Initialize Memory Bank** from templates
5. Offer to create `pyproject.toml`
6. Optionally start infrastructure

### Post-Installation

If you skipped any of the optional steps:

**Create pyproject.toml:**
```bash
cp pyproject.toml.example pyproject.toml
# Edit: Update project name, dependencies
```

**Initialize Memory Bank:**
```bash
cp -r memory-bank-template memory-bank
cd memory-bank
for f in *.template; do mv "$f" "${f%.template}"; done
```

**Start infrastructure:**
```bash
bash scripts/dev/start-infra.sh
```

---

## First-Time Setup

### 1. Configure Environment

```bash
# Copy environment example
cp .env.example .env

# Edit with your values
nano .env
```

**Key variables:**
- `POSTGRES_*` - PostgreSQL credentials
- `CLICKHOUSE_*` - ClickHouse settings
- `LOG_LEVEL` - Logging verbosity

### 2. Customize Memory Bank

Edit [`memory-bank/systemPatterns.md`](./memory-bank/systemPatterns.md):

```markdown
# System Patterns

## Development Principles
[Add your team's coding standards...]

## Infrastructure Patterns
[Document your specific infrastructure...]
```

### 3. Install Dependencies

```bash
# Install base and dev dependencies
uv pip install -e ".[dev]"

# Add project-specific packages
uv add requests httpx  # Example
```

### 4. Verify Setup

```bash
# Check infrastructure
cd infrastructure && docker compose ps

# Run tests
docker compose run --rm dev pytest

# Check Python environment
docker compose run --rm dev python --version
```

---

## Memory Bank

The Memory Bank is RooFlow's central knowledge management system.

### Structure

**systemPatterns.md** - Reusable patterns
- Code patterns
- Testing approach
- Error handling
- Bug pattern catalog

**decisionLog.md** - Architecture decisions
- ADRs (Architecture Decision Records)
- Technology choices
- Design trade-offs

**productContext.md** - Product knowledge
- Business rules
- Domain terminology
- User workflows

**progress.md** - Project tracking
- Milestones
- Current work
- Blockers

**activeContext.md** - Current state
- Active tasks
- Recent changes
- Handoff context

### When to Update

**After making decisions:**
```markdown
# In decisionLog.md
# ADR-003: Choose FastAPI for REST API

**Status:** Accepted
**Date:** 2025-12-30

## Decision
Use FastAPI for REST API implementation

## Rationale
- Async support
- Automatic OpenAPI docs
- Type safety with Pydantic
```

**After discovering patterns:**
```markdown
# In systemPatterns.md
## Database Patterns

### Connection Pooling

```python
from libs.db.base import get_session

with get_session() as session:
    result = session.execute(query)
```
```

**After fixing bugs:**
```markdown
# In systemPatterns.md
## Bug Patterns

### Empty String Validation

**Problem:** `if value:` treats empty string as falsy

**Solution:**
```python
if value is not None and value != "":
    process(value)
```

**When discovered:** 2025-12-30
**Test:** test_empty_string_validation()
```

---

## Flow Modes

### Architect Mode

**Use for:**
- System design
- Technology evaluation
- Creating ADRs
- Planning refactorings

**Outputs:**
- Design documents
- Architecture diagrams (mermaid)
- ADRs in decisionLog.md
- Patterns in systemPatterns.md

**Example:**
```
"Switch to Architect mode. Design a caching layer for the API."
```

### Code Mode

**Use for:**
- Feature implementation
- Writing tests
- Refactoring
- Code reviews

**Follows:**
- systemPatterns.md conventions
- TDD for critical logic
- Type hints required
- Structured logging

**Example:**
```
"Switch to Code mode. Implement the user authentication service per the design in decisionLog.md ADR-005."
```

### Debug Mode

**Use for:**
- Bug investigation
- Performance issues
- Test-driven debugging
- Pattern documentation

**Process:**
1. Write failing test
2. Investigate with observability
3. Fix code
4. Verify test passes
5. Document bug pattern

**Example:**
```
"Switch to Debug mode. Investigate why transfers table query is slow."
```

### Ask Mode

**Use for:**
- Querying Memory Bank
- Understanding code
- Getting recommendations
- Learning patterns

**Always:**
- Checks Memory Bank first
- References systemPatterns.md
- Provides code examples
- Suggests appropriate mode for actions

**Example:**
```
"Switch to Ask mode. How should I handle database connections in this project?"
```

### Orchestrator Mode

**Use for:**
- Multi-phase projects
- Cross-mode coordination
- Complex refactorings
- Long-running features

**Maintains:**
- progress.md tracking
- activeContext.md handoffs
- Consistent decisions across phases

**Example:**
```
"Switch to Orchestrator mode. Coordinate the migration from PostgreSQL to ClickHouse."
```

---

## Infrastructure

### Services

**Core services** ([`infrastructure/docker-compose.yml`](./infrastructure/docker-compose.yml)):
- PostgreSQL (transactional data)
- Redis (caching)
- ClickHouse (analytics)

**Observability stack** ([`infrastructure/observability/`](./infrastructure/observability/)):
- Prometheus (metrics)
- Grafana (dashboards)
- Loki (log aggregation)
- Promtail (log shipper)

### Start/Stop

```bash
# Start all
bash scripts/dev/start-infra.sh

# Start specific service
cd infrastructure
docker compose up -d postgres redis

# Check status
docker compose ps

# View logs
docker compose logs -f postgres

# Stop all
bash scripts/dev/stop-infra.sh
```

### Access Services

**Grafana:**
- URL: `http://localhost:3001`
- Login: admin / admin

**Prometheus:**
- URL: `http://localhost:9090`

**Databases:**
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- ClickHouse: `localhost:9000` (native)

### Using Observability

**Structured logging:**
```python
from libs.observability.logging import get_logger

logger = get_logger(__name__)

logger.info(
    "Processing started",
    item_id=item.id,
    user_id=user.id,
    action="process"
)
```

**Metrics:**
```python
from libs.observability.metrics import record_metric

record_metric(
    "items_processed",
    1,
    labels={"status": "success", "type": "payment"}
)
```

**Timing decorator:**
```python
from libs.observability.decorators import with_timing

@with_timing("process_payment")
def process_payment(payment_id: str):
    # ... processing
    pass
```

---

## Development Workflow

### Daily Workflow

1. **Check activeContext.md** - See what's in progress
2. **Choose appropriate mode** - Architect, Code, Debug, etc.
3. **Work on task** - Follow mode-specific patterns
4. **Update Memory Bank** - Document decisions/patterns
5. **Update progress.md** - Track completion

### Adding Features

1. **Architect mode** - Design the feature
   - Create ADR in decisionLog.md
   - Design data models
   - Plan integration

2. **Code mode** - Implement
   - Follow systemPatterns.md
   - Write tests (TDD for critical logic)
   - Use libs/ patterns

3. **Debug mode** - Test and refine
   - Integration testing
   - Performance verification
   - Bug pattern documentation

4. **Update Memory Bank**
   - New patterns → systemPatterns.md
   - Decisions → decisionLog.md
   - Progress → progress.md

### Fixing Bugs

1. **Debug mode** - TDD approach
   ```python
   # Write failing test FIRST
   def test_bug_empty_string_validation():
       """Reproduce bug: empty strings pass validation"""
       with pytest.raises(ValidationError):
           validate_input("")  # Should fail but doesn't
   ```

2. **Run test** - Confirm it fails

3. **Fix code** - Implement fix

4. **Run test** - Confirm it passes

5. **Document pattern** in systemPatterns.md:
   ```markdown
   ## Bug Patterns
   
   ### Empty String Validation
   **Problem:** ...
   **Solution:** ...
   **Test:** test_bug_empty_string_validation()
   ```

6. **Commit test + fix together**

### Package Management

**Installing packages:**
```bash
# Quick install for experimentation
uv pip install pandas

# Production dependency
uv add pandas

# Development dependency
uv add --dev pytest-mock

# Update all
uv pip install -e ".[dev]"
```

**Agents can:**
- ✅ Install packages freely
- ✅ Test immediately
- ✅ Add to pyproject.toml with `uv add`
- ✅ Commit with code changes

**Agents should NOT:**
- ❌ Ask permission for standard packages
- ❌ Leave dependencies undocumented
- ❌ Use pip instead of uv

---

## Best Practices

### Code Quality

**Always:**
- ✓ Use type hints
- ✓ Validate inputs
- ✓ Structured logging
- ✓ Fail-fast errors
- ✓ Follow systemPatterns.md

**Never:**
- ❌ Emoticons in logs
- ❌ Silent exception catching
- ❌ Magic numbers/strings
- ❌ Default values for invalid inputs

### Testing

**Write tests for:**
- Bug fixes (TDD - test first!)
- Critical business logic
- External integrations
- Complex algorithms

**Skip tests for:**
- Simple CRUD
- One-time scripts
- Prototypes

### Git

**Check last 3 commits before changes:**
```bash
git log -3 --oneline --stat
```

**Commit messages:**
```
Type: Short description

Longer explanation:
- Why this change
- What problem it solves

Refs: #123
```

**Types:** Feature, Fix, Refactor, Docs, Test, Chore

### Memory Bank Maintenance

**Keep current:**
- Update systemPatterns.md when establishing patterns
- Create ADRs for significant decisions
- Track progress regularly
- Clean up activeContext.md

**Cross-reference:**
- Link related sections
- Reference from mode rules
- Keep DRY (Don't Repeat Yourself)

---

## Troubleshooting

### Infrastructure Won't Start

```bash
# Check Docker
docker --version
docker compose --version

# View errors
cd infrastructure
docker compose up  # Without -d to see output

# Check ports
netstat -an | grep 5432  # PostgreSQL
netstat -an | grep 6379  # Redis
```

### Container Issues

```bash
# Rebuild dev container
docker compose -f docker-compose.dev.yml build dev

# Reset infrastructure
bash scripts/dev/stop-infra.sh
docker compose down -v  # Removes volumes!
bash scripts/dev/start-infra.sh
```

### Package Installation Fails

```bash
# Update uv
pip install --upgrade uv

# Clear cache
rm -rf .venv
uv venv
uv pip install -e ".[dev]"
```

### Memory Bank Not Working

```bash
# Verify structure
ls -la memory-bank/
# Should see: systemPatterns.md, decisionLog.md, etc.

# Re-initialize if needed
rm -rf memory-bank
cp -r memory-bank-template memory-bank
cd memory-bank && for f in *.template; do mv "$f" "${f%.template}"; done
```

---

## Next Steps

1. ✅ Run installer
2. ✅ Configure environment (.env)
3. ✅ Customize Memory Bank
4. ✅ Install dependencies
5. ✅ Start infrastructure
6. 🚀 Start building!

**Helpful commands:**
```bash
# Quick reference
docker compose run --rm dev pytest          # Run tests
docker compose run --rm dev python script.py  # Run script
bash scripts/dev/start-infra.sh              # Start infra
git log -3 --oneline                         # Recent commits
```

**Documentation:**
- [README.md](./README.md) - Overview
- [memory-bank/README.md](./memory-bank-template/README.md) - Memory Bank guide
- [infrastructure/README.md](./infrastructure/README.md) - Infrastructure details
- [libs/README.md](./libs/README.md) - Library documentation

---

Happy coding with RooFlow! 🚀
