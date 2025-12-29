# Debug Mode Rules

**Mode Purpose:** Troubleshooting issues, investigating errors, and diagnosing problems.

---

## Systematic Debugging Process

### 1. Reproduce the Bug

**Always start by reproducing the issue:**

```python
# Write a failing test FIRST
def test_reproduce_bug():
    """
    Reproduce bug: Transfer validation fails for valid transfers.
    Expected: Should accept valid transfer
    Actual: Raises ValidationError incorrectly
    """
    transfer = Transfer(id="valid-123", amount=100.50)
    # This should NOT raise but currently does:
    result = process_transfer(transfer)
    assert result.status == TransferStatus.CONFIRMED
```

Run the test to confirm it fails as expected.

---

### 2. Use Observability Stack

Leverage infrastructure for debugging:

**Check Logs (Loki):**
```bash
# View recent logs
docker compose logs -f service_name

# Search structured logs in Grafana
# Navigate to Grafana → Explore → Loki
```

**Check Metrics (Prometheus/Grafana):**
- Error rates
- Request latency
- System resources
- Custom metrics

See [`infrastructure/observability/`](../../infrastructure/observability/) for setup.

---

### 3. Git Blame and History

**Find when bug was introduced:**

```bash
# See who last modified the problematic code
git blame path/to/file.py

# View history of specific function
git log -p --follow -S "function_name" path/to/file.py

# Compare current with last known good version
git diff abc123 HEAD -- path/to/file.py
```

**Why this matters:**
- Understand what changed
- Find related commits
- Check if bug fix was reverted
- Learn from previous attempts

---

### 4. Add Targeted Logging

**Instrument code with debug logging:**

```python
from loguru import logger

def problematic_function(data: dict) -> Result:
    logger.debug(
        "Function entry",
        input_data=data,
        data_type=type(data).__name__
    )
    
    # Add logging at decision points
    if not validate(data):
        logger.warning(
            "Validation failed",
            data=data,
            validation_errors=get_validation_errors(data)
        )
        raise ValidationError("Invalid data")
    
    result = process(data)
    
    logger.debug(
        "Function exit",
        result=result,
        processing_time_ms=elapsed_time
    )
    
    return result
```

---

### 5. Isolate the Problem

**Binary search approach:**

```python
# Test each component in isolation
def test_validation_alone():
    """Test validation logic independently."""
    data = {"id": "123", "amount": 100}
    assert validate(data) == True

def test_processing_alone():
    """Test processing logic independently."""
    valid_data = create_valid_data()
    result = process(valid_data)
    assert result is not None

def test_full_pipeline():
    """Test complete flow."""
    result = full_process({"id": "123", "amount": 100})
    assert result.status == "success"
```

---

## Test-Driven Debugging

### Write Reproduction Test First

**ALWAYS:**
1. Write test that reproduces the bug
2. Verify test fails
3. Fix the code
4. Verify test passes
5. **Commit test + fix together**

```python
# tests/test_bug_fixes.py

def test_bug_transfer_empty_string_not_validated():
    """
    Bug: Empty string transfer_id passes validation.
    
    Steps to reproduce:
    1. Create transfer with empty string ID
    2. Process transfer
    
    Expected: ValidationError raised
    Actual: Transfer processes successfully (BUG)
    """
    with pytest.raises(ValidationError, match="transfer_id cannot be empty"):
        process_transfer(transfer_id="", amount=100)
```

---

## Investigation Techniques

### Check Environment Variables

```python
import os
from loguru import logger

# Log environment at startup
logger.info(
    "Environment configuration",
    database_url=os.getenv("DATABASE_URL", "NOT_SET"),
    redis_url=os.getenv("REDIS_URL", "NOT_SET"),
    log_level=os.getenv("LOG_LEVEL", "INFO")
)
```

### Verify External Dependencies

```bash
# Check database connectivity
docker compose exec postgres psql -U user -d database -c "SELECT 1;"

# Check Redis
docker compose exec redis redis-cli ping

# Check API endpoints
curl -i http://localhost:8000/health
```

### Memory/Performance Issues

```python
import tracemalloc
import time
from loguru import logger

# Track memory allocation
tracemalloc.start()

def debug_memory_usage():
    """Debug memory-intensive operations."""
    snapshot_before = tracemalloc.take_snapshot()
    
    # Perform operation
    result = expensive_operation()
    
    snapshot_after = tracemalloc.take_snapshot()
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
    
    logger.info("Memory usage top 10:")
    for stat in top_stats[:10]:
        logger.info(f"{stat}")
    
    return result
```

---

## Common Bug Patterns

### Document in systemPatterns.md

When you discover a bug pattern, add it to [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md):

```markdown
## Bug Patterns

### Pattern: Empty String Validation

**Problem:** Empty strings pass validation because `if value:` check treats empty string as falsy.

**Solution:**
```python
# ❌ Bad - fails for empty string
if value:
    process(value)

# ✓ Good - explicit check
if value is not None and value != "":
    process(value)
```

**When discovered:** 2025-12-29
**Related test:** test_bug_transfer_empty_string_not_validated
```

---

## Integration with Other Modes

### For Code Mode

After finding the fix:
1. Ensure test coverage
2. Update systemPatterns.md with bug pattern
3. Check for similar bugs elsewhere
4. Switch to Code mode for implementation

### For Architect Mode

If bug reveals architectural issue:
1. Document in [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md)
2. Create design for proper fix
3. Switch to Architect mode for redesign

---

## Debugging Checklist

Before concluding debugging:

- [ ] Bug reproduced with failing test
- [ ] Root cause identified
- [ ] Git history reviewed
- [ ] Observability stack checked (logs, metrics)
- [ ] Fix implemented with test
- [ ] Test passes
- [ ] Similar bugs checked in codebase
- [ ] Bug pattern documented in systemPatterns.md
- [ ] Logs and debug code removed/cleaned
- [ ] Committed test + fix together

---

## Observability Best Practices

### Use Structured Logging for Debugging

```python
# Include context for every log
logger.debug(
    "Processing item",
    item_id=item.id,
    item_type=type(item).__name__,
    step="validation",
    state=item.__dict__
)
```

### Create Debug Dashboards

In Grafana, create dashboard for:
- Error rates by endpoint
- Request latency percentiles (p50, p95, p99)
- Queue depths
- Database query times

See [`infrastructure/observability/grafana/`](../../infrastructure/observability/grafana/) for configuration.

---

## Related Documentation

- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) - Bug patterns and solutions
- [`infrastructure/observability/`](../../infrastructure/observability/) - Observability stack
- [`libs/observability/`](../../libs/observability/) - Logging and metrics utilities
