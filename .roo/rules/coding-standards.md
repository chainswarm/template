# Coding Standards

**Last Updated:** 2025-12-29
**Purpose:** Define comprehensive coding practices for agentic AI development

---

## Core Principles

### NEVER

- ❌ Use emoticons in logs (🚀, ✅, ❌, etc.)
- ❌ Silently catch exceptions without logging or re-raising
- ❌ Return `None` without explicit documentation
- ❌ Use magic numbers or strings without constants
- ❌ Write clever code that requires comments to understand
- ❌ Mix business logic with infrastructure concerns
- ❌ Skip input validation
- ❌ Assume external data is valid

### ALWAYS

- ✓ Validate inputs at boundaries
- ✓ Log structured data (use key-value pairs)
- ✓ Use type hints
- ✓ Raise specific exceptions
- ✓ Write self-descriptive code
- ✓ Separate concerns (business logic, data access, presentation)
- ✓ Make failures explicit and debuggable
- ✓ Document why, not what

---

## Error Handling

### Fail-Fast Philosophy

Validate early, fail explicitly:

```python
def process_transfer(transfer_id: str, amount: float) -> Transfer:
    # Validate inputs immediately
    if not transfer_id:
        raise ValueError("transfer_id cannot be empty")
    
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}. Must be positive")
    
    # Proceed with confidence
    transfer = fetch_transfer(transfer_id)
    
    if not transfer:
        raise TransferNotFoundError(f"Transfer {transfer_id} not found")
    
    return process(transfer, amount)
```

### Exception Hierarchy

Create specific exception types:

```python
class ChainSwarmError(Exception):
    """Base exception for all chain swarm errors"""
    pass


class ValidationError(ChainSwarmError):
    """Raised when input validation fails"""
    pass


class TransferNotFoundError(ChainSwarmError):
    """Raised when transfer is not found"""
    pass


class InsufficientDataError(ChainSwarmError):
    """Raised when not enough data for analysis"""
    pass
```

### Error Context

Always provide actionable context:

```python
# ❌ Bad
raise Exception("Failed")

# ❌ Still bad
raise ValueError("Invalid input")

# ✓ Good
raise ValueError(
    f"Invalid block range: start={start_block}, end={end_block}. "
    f"Start must be less than end"
)

# ✓ Better
raise ValidationError(
    f"Invalid block range for network '{network}': "
    f"start={start_block}, end={end_block}. "
    f"Expected: start < end <= {max_block}"
)
```

### Try-Catch Guidelines

Only catch exceptions you can handle:

```python
# ❌ Bad - swallowing errors
try:
    result = process_data()
except Exception:
    return None

# ❌ Bad - catching too broadly
try:
    result = fetch_and_process()
except Exception as e:
    logger.error(f"Error: {e}")
    return None

# ✓ Good - catch specific, handle properly
try:
    result = fetch_from_api()
except APIConnectionError as e:
    logger.error(
        "API connection failed",
        error=str(e),
        endpoint=e.endpoint,
        retry_count=e.retry_count
    )
    raise

# ✓ Good - transform exceptions
try:
    data = external_api.fetch()
except ExternalAPIError as e:
    raise DataFetchError(
        f"Failed to fetch data from {external_api.name}: {str(e)}"
    ) from e
```

---

## Logging Standards

### Structured Logging

Use loguru with structured fields:

```python
from loguru import logger

# ❌ Bad - unstructured
logger.info(f"Processing block {block_number} for {network}")

# ❌ Bad - emoticons
logger.info(f"✅ Successfully processed block {block_number}")

# ✓ Good - structured
logger.info(
    "Processing block",
    block_number=block_number,
    network=network
)

# ✓ Good - with context
logger.info(
    "Block processing complete",
    block_number=block_number,
    network=network,
    transactions_count=len(transactions),
    duration_ms=duration,
    status="success"
)
```

### Log Levels

Use appropriate log levels:

```python
# DEBUG - detailed diagnostic info
logger.debug(
    "Cache lookup",
    key=cache_key,
    hit=cache_hit,
    ttl_remaining=ttl
)

# INFO - normal operations
logger.info(
    "Transfer indexed",
    transfer_id=transfer_id,
    from_address=from_addr,
    to_address=to_addr,
    amount=amount
)

# WARNING - unexpected but handled
logger.warning(
    "Retry attempt",
    attempt=retry_count,
    max_attempts=max_retries,
    error=str(last_error)
)

# ERROR - errors that need attention
logger.error(
    "Failed to process block",
    block_number=block_number,
    error=str(e),
    traceback=traceback.format_exc()
)
```

### No Emoticons in Logs

Logs are for machines and humans debugging production issues:

```python
# ❌ NEVER
logger.info("🚀 Starting indexer")
logger.info("✅ Success")
logger.error("❌ Failed")

# ✓ ALWAYS
logger.info("Indexer starting", service="block-indexer", version="1.0.0")
logger.info("Operation completed", operation="index_block", status="success")
logger.error("Operation failed", operation="index_block", status="error")
```

---

## Code Organization

### Function Design

Keep functions focused and testable:

```python
# ❌ Bad - doing too much
def process_everything(data):
    validated = validate(data)
    transformed = transform(validated)
    enriched = enrich(transformed)
    stored = store(enriched)
    notified = notify(stored)
    return notified

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


def store_transfer(transfer: EnrichedTransfer) -> None:
    """Persist transfer to database."""
    repository.insert(transfer)
```

### Type Hints

Always use type hints:

```python
from typing import Optional, List, Dict, Any

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

# ✓ Better - with models
def fetch_transfers(
    network: NetworkType,
    block_range: BlockRange
) -> List[Transfer]:
    pass
```

### Constants

Use constants for magic values:

```python
# ❌ Bad
if status == 1:
    process()

if amount > 1000000:
    flag_large_transfer()

# ✓ Good
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0
LARGE_TRANSFER_THRESHOLD = 1_000_000

if status == STATUS_ACTIVE:
    process()

if amount > LARGE_TRANSFER_THRESHOLD:
    flag_large_transfer()

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

## Documentation

### Docstrings

Write docstrings for public APIs:

```python
def detect_layering_pattern(
    transfers: List[Transfer],
    min_layers: int = 3,
    time_window_hours: int = 24
) -> List[LayeringPattern]:
    """
    Detect layering patterns in transfer sequences.
    
    Layering involves moving funds through multiple addresses in rapid
    succession to obscure the original source.
    
    Args:
        transfers: List of transfers to analyze
        min_layers: Minimum number of hops to constitute layering
        time_window_hours: Maximum time between hops
    
    Returns:
        List of detected layering patterns, each containing the transfer
        chain and confidence score
    
    Raises:
        ValidationError: If transfers list is empty
        InsufficientDataError: If fewer than min_layers transfers
    """
    if not transfers:
        raise ValidationError("Transfers list cannot be empty")
    
    # Implementation
    pass
```

### Comments

Comments explain WHY, not WHAT:

```python
# ❌ Bad - explaining what code does
# Loop through transfers
for transfer in transfers:
    # Calculate amount
    amount = transfer.amount * transfer.price

# ✓ Good - explaining why
# We multiply by price here rather than in the repository layer
# because prices can change, and we want the exact price at query time
for transfer in transfers:
    amount = transfer.amount * transfer.price

# ✓ Good - explaining non-obvious decisions
# Using exponential backoff here because the upstream API
# has rate limiting that resets every 60 seconds
retry_strategy = ExponentialBackoff(base=2, max_wait=60)
```

---

## Testing

See [`testing.md`](testing.md) for comprehensive testing guidelines.

### Quick Reference

**Write tests for:**
- Integration points (APIs, databases, external services)
- Critical business logic (risk detection, pattern analysis)
- Complex algorithms
- Bug fixes (regression tests)

**Skip tests for:**
- Simple CRUD operations
- One-time migration scripts
- Prototype/exploratory code

---

## Related Documentation

- [`testing.md`](testing.md) - Testing philosophy and practices
- [`automode.md`](automode.md) - Execution patterns and script templates
- [`git-usage.md`](git-usage.md) - Git workflows for AI agents
- [`rules.md`](rules.md) - General development rules
