# Code Mode Rules

**Mode Purpose:** Implementation, testing, refactoring, and code quality.

---

## Code Quality Standards

### Follow systemPatterns.md

All code must adhere to [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md):

**NEVER:**
- ❌ Use emoticons in logs (🚀, ✅, ❌)
- ❌ Silently catch exceptions
- ❌ Return `None` without documentation
- ❌ Use magic numbers or strings
- ❌ Skip input validation

**ALWAYS:**
- ✓ Use type hints
- ✓ Validate inputs at boundaries
- ✓ Raise specific exceptions
- ✓ Log with structured data
- ✓ Write self-descriptive code

### Reference Example Patterns

Before writing new code, check [`libs/`](../../libs/) for patterns:

- [`libs/db/`](../../libs/db/) - Database patterns
- [`libs/observability/`](../../libs/observability/) - Logging, metrics, tracing

**Reuse existing patterns from systemPatterns.md rather than inventing new ones.**

---

## Development Workflow

### 1. Check Git History

Before making changes, understand the context:

```bash
# Check last 3 commits
git log -3 --oneline --stat

# See what changed in specific files
git log -3 --follow -- path/to/file.py

# Understand recent changes
git show HEAD~1
```

**Why this matters:**
- Avoid reverting recent bug fixes
- Understand code evolution
- Learn from past decisions
- Maintain consistency

See [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) for git workflows.

### 2. Test-Driven Development for Bugs

**When fixing bugs, write the integration test FIRST:**

```python
# 1. Write failing test that reproduces the bug
def test_transfer_validation_bug():
    """Test that invalid transfers are rejected."""
    with pytest.raises(ValidationError):
        process_transfer(transfer_id="", amount=100)  # Should fail

# 2. Run test - it should fail
# 3. Fix the code
# 4. Run test - it should pass
# 5. Commit test + fix together
```

See [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) testing section.

### 3. Package Management with uv

Use `uv` for all Python package management:

```bash
# Add dependency
uv pip install package-name

# Add dev dependency
uv pip install --dev package-name

# Update pyproject.toml
# Add to dependencies or optional-dependencies
```

**Never use pip directly. Always use uv.**

---

## Error Handling

### Fail-Fast Philosophy

Validate early, fail explicitly:

```python
def process_transfer(transfer_id: str, amount: float) -> Transfer:
    # Validate immediately
    if not transfer_id:
        raise ValueError("transfer_id cannot be empty")
    
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}. Must be positive")
    
    # NO default values for invalid inputs
    # NO silent failures
    # NO returning None without raising
    
    transfer = fetch_transfer(transfer_id)
    if not transfer:
        raise TransferNotFoundError(f"Transfer {transfer_id} not found")
    
    return process(transfer, amount)
```

### No Default Values for Invalid Inputs

```python
# ❌ NEVER do this
def get_config(key: str) -> str:
    value = config.get(key)
    if not value:
        return "default"  # Hiding the problem!
    return value

# ✓ ALWAYS do this
def get_config(key: str) -> str:
    value = config.get(key)
    if not value:
        raise ConfigurationError(f"Required config key '{key}' not found")
    return value
```

---

## Logging Standards

### Structured Logging Only

Use loguru with structured fields:

```python
from loguru import logger

# ❌ NEVER
logger.info("Processing block 12345 for ethereum")
logger.info("✅ Success!")  # NO EMOTICONS

# ✓ ALWAYS
logger.info(
    "Processing block",
    block_number=12345,
    network="ethereum",
    status="started"
)

logger.info(
    "Block processing complete",
    block_number=12345,
    network="ethereum",
    transactions_count=42,
    duration_ms=156,
    status="success"
)
```

### No Emoticons Ever

Logs are for production debugging, not user interfaces:

```python
# ❌ FORBIDDEN
logger.info("🚀 Starting service")
logger.info("✅ Operation successful")
logger.error("❌ Operation failed")

# ✓ REQUIRED
logger.info("Service starting", service="indexer", version="1.0.0")
logger.info("Operation completed", operation="index_block", status="success")
logger.error("Operation failed", operation="index_block", error=str(e))
```

---

## Testing Strategy

See [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) testing section.

### Write Integration Tests For:

- ✓ Bug fixes (TDD: test first!)
- ✓ Critical business logic
- ✓ External integrations (API, database)
- ✓ Complex algorithms
- ✓ Edge cases and error paths

### Skip Tests For:

- ⊘ Simple CRUD operations
- ⊘ One-time migration scripts
- ⊘ Prototype/exploratory code
- ⊘ Trivial getters/setters

### Test Structure

```python
def test_feature_name():
    """
    Test description: what behavior is being verified.
    """
    # Arrange: set up test data
    transfer = Transfer(id="123", amount=100)
    
    # Act: perform the operation
    result = process_transfer(transfer)
    
    # Assert: verify expected outcome
    assert result.status == TransferStatus.CONFIRMED
    assert result.amount == 100
```

---

## Code Organization

### Function Design

Keep functions focused:

```python
# ❌ Bad - doing too much
def process_everything(data):
    validated = validate(data)
    transformed = transform(validated)
    enriched = enrich(transformed)
    stored = store(enriched)
    return stored

# ✓ Good - single responsibility
def validate_transfer_data(data: dict) -> TransferData:
    """Validate and parse raw transfer data."""
    if not data.get("id"):
        raise ValidationError("Transfer ID required")
    return TransferData(**data)

def enrich_transfer(transfer: TransferData) -> EnrichedTransfer:
    """Add labels and metadata to transfer."""
    labels = fetch_labels(transfer.from_address, transfer.to_address)
    return EnrichedTransfer(transfer, labels)
```

### Type Hints Required

```python
from typing import Optional, List, Dict

# ❌ Bad
def fetch_transfers(network, start_block, end_block):
    pass

# ✓ Good
def fetch_transfers(
    network: str,
    start_block: int,
    end_block: int
) -> List[Transfer]:
    pass
```

### Constants for Magic Values

```python
# ❌ Bad
if status == 1:
    process()

# ✓ Good
STATUS_ACTIVE = 1
if status == STATUS_ACTIVE:
    process()

# ✓ Better - use enums
from enum import Enum

class TransferStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"

if status == TransferStatus.CONFIRMED:
    process()
```

---

## Observability Integration

### Use Template Patterns

Follow patterns from [`libs/observability/`](../../libs/observability/):

```python
from libs.observability.logging import get_logger
from libs.observability.metrics import record_metric
from libs.observability.decorators import with_timing

logger = get_logger(__name__)

@with_timing("process_transfer")
def process_transfer(transfer: Transfer) -> Result:
    logger.info(
        "Processing transfer",
        transfer_id=transfer.id,
        amount=transfer.amount
    )
    
    result = do_processing(transfer)
    
    record_metric(
        "transfers_processed",
        1,
        labels={"status": result.status, "network": transfer.network}
    )
    
    return result
```

### Prometheus Metrics

Follow conventions from [`infrastructure/observability/prometheus/prometheus.yml`](../../infrastructure/observability/prometheus/prometheus.yml):

- Use counters for events (requests, errors)
- Use gauges for current values (queue size, active connections)
- Use histograms for durations (request latency, processing time)
- Add meaningful labels (status, method, endpoint)

---

## Development Environment

### Use Docker for Consistency

Run all code in the development container:

```bash
# Start infrastructure
bash scripts/dev/start-infra.sh

# Run Python scripts
docker compose run --rm dev python scripts/my_script.py

# Run tests
docker compose run --rm dev pytest

# Stop infrastructure
bash scripts/dev/stop-infra.sh
```

See [`scripts/README.md`](../../scripts/README.md) for script conventions.

### Configuration Management

Follow patterns from [`.env.example`](../../.env.example):

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

# Usage
settings = Settings()
```

**Never hardcode secrets or configuration.**

---

## Code Review Checklist

Before committing, verify:

- [ ] Follows [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md)
- [ ] Type hints on all functions
- [ ] Input validation at boundaries
- [ ] Structured logging (no emoticons)
- [ ] Fail-fast error handling
- [ ] No magic numbers/strings
- [ ] No default values for invalid inputs
- [ ] Integration tests for new features
- [ ] Integration tests for bug fixes (TDD)
- [ ] Uses existing patterns from [`libs/`](../../libs/)
- [ ] Git history reviewed (last 3 commits)
- [ ] Documentation updated if needed
- [ ] Observability included (logs, metrics)

---

## Common Patterns

### Database Access

Use patterns from [`libs/db/`](../../libs/db/):

```python
from libs.db.base import get_session
from libs.db.utils import execute_with_retry

def fetch_transfers(network: str) -> List[Transfer]:
    with get_session() as session:
        result = session.execute(
            select(Transfer).where(Transfer.network == network)
        )
        return result.scalars().all()
```

### Async Operations

```python
import asyncio
from typing import List

async def fetch_multiple_networks(networks: List[str]) -> List[Transfer]:
    tasks = [fetch_transfers_async(network) for network in networks]
    results = await asyncio.gather(*tasks)
    return [t for result in results for t in result]
```

### Configuration-Driven Code

```python
# ❌ Bad - hardcoded
NETWORKS = ["ethereum", "polygon", "arbitrum"]

# ✓ Good - configurable
from config import settings

def get_active_networks() -> List[str]:
    return settings.active_networks
```

---

## Updating systemPatterns.md

### When to Update

Update [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) when:
- Implementing new architectural pattern
- Discovering bug pattern worth documenting
- Creating reusable code pattern
- Establishing new convention

### How to Update

```markdown
## [Category Name]

### Pattern Name

**When to use:** [Describe the scenario]

**Implementation:**
```python
# Code example
```

**Don't use when:** [Anti-patterns or exceptions]
```

---

## Related Documentation

- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) - Development patterns and standards
- [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md) - Architecture decisions
- [`libs/README.md`](../../libs/README.md) - Code pattern examples
- [`infrastructure/README.md`](../../infrastructure/README.md) - Infrastructure patterns
