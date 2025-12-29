# Core Libraries (Example)

**IMPORTANT**: This directory contains **example code** only. These files are not part of your active project and won't interfere with template syncing.

Copy these modules to your project (e.g., `libs/` or `src/`) and adapt as needed.

---

## Modules

### `observability/`

Observability module providing logging, metrics, and graceful shutdown handling.

**Features:**
- Structured logging with loguru
- Prometheus metrics with automatic server management
- Correlation ID tracking for request tracing
- Graceful shutdown handling with signal handlers
- Decorators for automatic error logging and metrics

**Example Usage:**

```python
# Copy to your project first: cp -r libs-example/observability libs/
from libs.observability import setup_logger, setup_metrics, log_errors

# Setup logging
setup_logger("my-service")

# Setup metrics (starts Prometheus server)
metrics = setup_metrics("my-service", port=9090)

# Use decorator for automatic error logging
@log_errors
def process_data(data):
    # Your code here
    pass
```

**Key Components:**

- [`observability/logging.py`](observability/logging.py) - Structured logging with correlation IDs
- [`observability/metrics.py`](observability/metrics.py) - Prometheus metrics registry
- [`observability/decorators.py`](observability/decorators.py) - Convenience decorators
- [`observability/shutdown.py`](observability/shutdown.py) - Graceful shutdown handling

### `db/`

Database utilities and base repository patterns.

**Features:**
- Abstract base repository pattern
- Example ClickHouse repository implementation
- SQL query builders with sanitization
- Support for multiple SQL dialects

**Example Usage:**

```python
# Copy to your project first: cp -r libs-example/db libs/
from libs.db import ClickHouseRepository, sanitize_identifier

# Create repository
repo = ClickHouseRepository(client, "my_table")

# Insert data
repo.insert({"id": 1, "name": "test"})

# Query data
results = repo.query({"id": 1})

# Count records
count = repo.count({"status": "active"})
```

**Key Components:**

- [`db/base.py`](db/base.py) - Abstract repository pattern and ClickHouse implementation
- [`db/utils.py`](db/utils.py) - SQL builders and sanitization utilities

---

## Getting Started

### 1. Copy to Your Project

```bash
# Copy entire libs-example to libs/
cp -r libs-example libs

# Or copy individual modules
cp -r libs-example/observability libs/
cp -r libs-example/db libs/
```

### 2. Install Dependencies

```bash
# Observability module
uv add loguru prometheus-client

# Database module
uv add clickhouse-driver  # Or your database driver
```

### 3. Import and Use

```python
from libs.observability import setup_logger
from libs.db import ClickHouseRepository

setup_logger("my-app")
```

---

##  Extending the Libraries

### Adding New Database Support

To add support for a new database (e.g., MongoDB, PostgreSQL):

1. Create a new repository class inheriting from `BaseRepository`
2. Implement all abstract methods
3. Add to `db/__init__.py`

Example:

```python
from libs.db.base import BaseRepository

class PostgresRepository(BaseRepository):
    def insert(self, data):
        # PostgreSQL-specific implementation
        pass
    
    # Implement other methods...
```

### Adding Custom Metrics

To add custom metrics to your service:

```python
from libs.observability import setup_metrics, DURATION_BUCKETS

metrics = setup_metrics("my-service")

# Create custom counter
requests_total = metrics.create_counter(
    "requests_total",
    "Total HTTP requests",
    labelnames=["method", "endpoint"]
)

# Create custom histogram
request_duration = metrics.create_histogram(
    "request_duration_seconds",
    "Request duration",
    labelnames=["endpoint"],
    buckets=DURATION_BUCKETS
)

# Use metrics
requests_total.labels(method="GET", endpoint="/api/data").inc()
request_duration.labels(endpoint="/api/data").observe(0.234)
```

### Using Correlation IDs

Correlation IDs help track requests across multiple services:

```python
from libs.observability import (
    generate_correlation_id,
    set_correlation_id,
    get_correlation_id
)

# Generate and set correlation ID
corr_id = generate_correlation_id()
set_correlation_id(corr_id)

# Correlation ID is automatically included in logs
logger.info("Processing request")  # Includes correlation_id in extra

# Get correlation ID
current_id = get_correlation_id()
```

---

## Best Practices

### Logging

1. **Use structured logging** - Always include key-value pairs
2. **No emoticons** - Keep logs machine-readable
3. **Include context** - Add relevant fields to every log statement

```python
# ✓ Good
logger.info(
    "Transfer processed",
    transfer_id=transfer_id,
    amount=amount,
    from_address=from_addr,
    to_address=to_addr,
    duration_ms=duration
)

# ❌ Bad
logger.info(f"✅ Processed transfer {transfer_id}")
```

### Metrics

1. **Use appropriate buckets** - Use predefined buckets or create custom ones
2. **Label carefully** - Don't create high-cardinality labels
3. **Start metrics server** - Metrics are only useful if exposed

```python
# ✓ Good - low cardinality labels
requests.labels(method="GET", endpoint="/api/users").inc()

# ❌ Bad - high cardinality (user_id has millions of values)
requests.labels(user_id=user_id).inc()
```

### Error Handling

1. **Use @log_errors** - Automatically log exceptions with context
2. **Let exceptions propagate** - Don't swallow errors
3. **Add context** - Wrap exceptions with meaningful messages

```python
# ✓ Good
@log_errors
def process_batch(batch_id):
    try:
        data = fetch_data(batch_id)
    except DataNotFoundError as e:
        raise ProcessingError(f"Failed to process batch {batch_id}") from e
```

---

## Integration with Infrastructure

These libraries work seamlessly with the infrastructure services:

- **Prometheus** - Scrapes metrics from `/metrics` endpoint
- **Loki** - Collects logs from log files
- **Grafana** - Visualizes metrics and logs

See [`../infrastructure/README.md`](../infrastructure/README.md) for infrastructure setup.

---

## License

Adapted from ChainSwarm Core libraries for general use in agentic AI development.
