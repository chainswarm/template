# Autonomous Mode Execution Guide

**Last Updated:** 2025-12-29
**Purpose:** Define execution patterns for running scripts and managing infrastructure in agentic development

---

## Container-Based Development

All scripts and services run in Docker containers for environment consistency and proper dependency management.

### Quick Start

**Build the development container:**
```bash
docker compose -f docker-compose.dev.yml build dev
```

**Run a Python script:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev python scripts/your_script.py
```

**Interactive shell:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev bash
# Inside container:
python scripts/analyze_data.py
ls -la data/
exit
```

---

## Execution Patterns

### Python Scripts

**Template:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev python {script_path} {args}
```

**Examples:**
```bash
# Run analysis script
docker compose -f docker-compose.dev.yml run --rm dev python scripts/analysis/run_analysis.py

# Run with arguments
docker compose -f docker-compose.dev.yml run --rm dev python scripts/process.py --batch-size 100 --output data/results

# Run with environment override
ENVIRONMENT=staging docker compose -f docker-compose.dev.yml run --rm dev python scripts/migrate.py
```

### Bash Scripts

**Template:**
```bash
bash scripts/{category}/{script_name}.sh
```

**Examples:**
```bash
# Start infrastructure
bash scripts/dev/start-infra.sh

# Stop infrastructure
bash scripts/dev/stop-infra.sh

# Run utility script
bash scripts/utils/cleanup.sh
```

### Infrastructure Services

**Start all infrastructure:**
```bash
cd infrastructure
docker compose up -d
```

**Start specific service:**
```bash
cd infrastructure
docker compose up -d postgres redis
```

**Start observability stack:**
```bash
cd infrastructure/observability
docker compose up -d
```

**Check service status:**
```bash
cd infrastructure
docker compose ps
```

**View logs:**
```bash
cd infrastructure
docker compose logs -f postgres
```

---

## Python Script Template

### Basic Script

Scripts using Docker don't need `sys.path` manipulation:

```python
#!/usr/bin/env python3
"""
Script description: What this script does and when to use it
"""
from dotenv import load_dotenv
from loguru import logger

from libs.observability import setup_logger
from libs.db import create_client


def main():
    """Main execution function"""
    load_dotenv()
    
    # Setup logging
    setup_logger("script-name")
    logger.info("Script starting")
    
    # Your logic here
    logger.info("Processing data")
    
    logger.info("Script complete")


if __name__ == "__main__":
    main()
```

### Script with Database

```python
#!/usr/bin/env python3
"""
Database interaction script template
"""
import os
from dotenv import load_dotenv
from loguru import logger

from libs.observability import setup_logger
from libs.db import create_client


def main():
    load_dotenv()
    setup_logger("db-script")
    
    # Get connection parameters from environment
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "5432"))
    db_name = os.getenv("DB_NAME", "mydb")
    
    logger.info(
        "Connecting to database",
        host=db_host,
        port=db_port,
        database=db_name
    )
    
    # Create client
    client = create_client(
        host=db_host,
        port=db_port,
        database=db_name
    )
    
    try:
        # Work with database
        logger.info("Executing query")
        results = client.query("SELECT * FROM table LIMIT 10")
        
        logger.info(
            "Query complete",
            rows_returned=len(results)
        )
        
    finally:
        client.close()
        logger.info("Connection closed")


if __name__ == "__main__":
    main()
```

### Script with Argument Parsing

```python
#!/usr/bin/env python3
"""
Script with command-line arguments
"""
import argparse
from dotenv import load_dotenv
from loguru import logger

from libs.observability import setup_logger


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process data with configurable options"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input file path"
    )
    parser.add_argument(
        "--output",
        default="data/output",
        help="Output directory (default: data/output)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Batch size for processing (default: 100)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    load_dotenv()
    args = parse_args()
    
    # Setup logging with appropriate level
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logger("data-processor", log_level=log_level)
    
    logger.info(
        "Starting processing",
        input=args.input,
        output=args.output,
        batch_size=args.batch_size
    )
    
    # Process data
    process_data(
        input_path=args.input,
        output_dir=args.output,
        batch_size=args.batch_size
    )
    
    logger.info("Processing complete")


def process_data(input_path: str, output_dir: str, batch_size: int):
    """Process data in batches"""
    logger.info("Processing data batches")
    # Implementation here
    pass


if __name__ == "__main__":
    main()
```

---

## Bash Script Template

### Basic Script

```bash
#!/usr/bin/env bash
#
# Script description: What this script does
#

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Color output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Main function
main() {
    log_info "Script starting"
    
    # Your logic here
    
    log_info "Script complete"
}

# Run main function
main "$@"
```

### Infrastructure Control Script

```bash
#!/usr/bin/env bash
#
# Start infrastructure services
#

set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
readonly INFRA_DIR="$PROJECT_ROOT/infrastructure"

log_info() {
    echo -e "\033[0;32m[INFO]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

start_infrastructure() {
    log_info "Starting infrastructure services..."
    
    cd "$INFRA_DIR"
    
    # Check if .env exists
    if [ ! -f .env ]; then
        log_error ".env file not found in $INFRA_DIR"
        log_info "Copy .env.example to .env and configure it"
        exit 1
    fi
    
    # Start services
    docker compose up -d
    
    log_info "Infrastructure services started"
    log_info "PostgreSQL: localhost:5432"
    log_info "Redis: localhost:6379"
    log_info "ClickHouse: localhost:8123 (HTTP), localhost:9000 (Native)"
}

main() {
    start_infrastructure
}

main "$@"
```

---

## Environment Variables

### .env File Structure

Create `.env` file in project root (copy from `.env.example`):

```bash
# Application
ENVIRONMENT=development
LOG_LEVEL=INFO
LOGS_DIR=./logs

# PostgreSQL
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=myapp
POSTGRES_USER=dev
POSTGRES_PASSWORD=dev_password

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# ClickHouse
CLICKHOUSE_HOST=localhost
CLICKHOUSE_PORT=9000
CLICKHOUSE_DB=myapp
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=

# Observability
PROMETHEUS_PORT=9090
GRAFANA_PORT=3001
LOKI_PORT=3100

# API Keys (if needed)
# API_KEY=your_api_key_here
```

### Loading Environment Variables

```python
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

# Access variables
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = int(os.getenv("POSTGRES_PORT", "5432"))

# Required variables
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY environment variable required")
```

---

## Package Management with uv

This template uses **uv** for fast, reliable Python package management. Agents can freely install packages as needed.

### Installing Packages

**Quick install (inside dev container):**
```bash
# Install a package
uv pip install requests

# Install multiple packages
uv pip install httpx pandas numpy

# Install from requirements.txt
uv pip install -r requirements.txt

# Install project in editable mode
uv pip install -e .
```

**Add to project dependencies:**
```bash
# Add permanent dependency
uv add requests httpx

# Add dev dependency
uv add --dev pytest-mock ruff
```

### Package Workflow for AI Agents

**When you need a new package:**

1. **Install it immediately** for the task:
   ```bash
   uv pip install package-name
   ```

2. **Write and test your code** using the package

3. **If it's a permanent dependency**, add to `pyproject.toml`:
   ```bash
   uv add package-name
   ```

4. **Commit both code and dependencies**:
   ```bash
   git add pyproject.toml uv.lock your_code.py
   git commit -m "feat: Add feature using package-name"
   ```

### Agent Guidelines

**✅  Agents SHOULD:**
- Install packages freely as needed for tasks
- Test that code works after adding packages
- Document new permanent dependencies in `pyproject.toml`
- Use `uv pip install` for quick/temporary needs
- Use `uv add` for permanent dependencies
- Commit dependency changes with code changes

**❌ Agents should NOT:**
- Ask permission to install standard packages
- Skip testing after adding packages
- Leave dependencies undocumented
- Install packages globally (use uv venv)

### Example: Agent Workflow

```bash
# Task: Process JSON data with validation

# 1. Agent realizes pydantic is needed
uv pip install pydantic

# 2. Write code
cat > scripts/process_data.py <<EOF
from pydantic import BaseModel
from typing import List

class DataItem(BaseModel):
    id: int
    name: str
    value: float

def process_json(data: List[dict]) -> List[DataItem]:
    return [DataItem(**item) for item in data]
EOF

# 3. Test the code
python scripts/process_data.py

# 4. Add as permanent dependency
uv add pydantic

# 5. Commit everything
git add pyproject.toml uv.lock scripts/process_data.py
git commit -m "feat: Add JSON processing with Pydantic validation"
```

### Common Packages for AI Agents

**Data processing:**
- `pandas`, `numpy`, `polars`

**Web requests:**
- `requests`, `httpx`, `aiohttp`

**Data validation:**
- `pydantic`, `marshmallow`

**Database:**
- `psycopg2`, `clickhouse-driver`, `redis`

**Async:**
- `asyncio`, `aiofiles`, `anyio`

**Testing:**
- `pytest`, `pytest-asyncio`, `pytest-mock`

---

## Infrastructure Access

### Service Ports

When infrastructure is running, access services at:

| Service | Port | URL | Credentials |
|---------|------|-----|-------------|
| PostgreSQL | 5432 | `postgresql://localhost:5432` | dev / dev_password |
| Redis | 6379 | `redis://localhost:6379` | (no password) |
| ClickHouse HTTP | 8123 | `http://localhost:8123` | default / (no password) |
| ClickHouse Native | 9000 | `localhost:9000` | default / (no password) |
| Prometheus | 9090 | `http://localhost:9090` | (no auth) |
| Grafana | 3001 | `http://localhost:3001` | admin / admin |
| Loki | 3100 | `http://localhost:3100` | (no auth) |

### Connecting from Scripts

**PostgreSQL:**
```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
```

**Redis:**
```python
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)
```

**ClickHouse:**
```python
from clickhouse_driver import Client

client = Client(
    host="localhost",
    port=9000,
    database=os.getenv("CLICKHOUSE_DB")
)
```

---

## Docker Compose Patterns

### Development Container

**docker-compose.dev.yml:**
```yaml
services:
  dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/workspace
    environment:
      - PYTHONPATH=/workspace
    env_file:
      - .env
    network_mode: host
    stdin_open: true
    tty: true
```

### Running Commands

```bash
# One-off command
docker compose -f docker-compose.dev.yml run --rm dev python script.py

# Interactive shell
docker compose -f docker-compose.dev.yml run --rm dev bash

# With custom environment
CUSTOM_VAR=value docker compose -f docker-compose.dev.yml run --rm dev python script.py
```

---

## Common Workflows

### Data Processing

```bash
# 1. Start infrastructure
bash scripts/dev/start-infra.sh

# 2. Run data ingestion
docker compose -f docker-compose.dev.yml run --rm dev \
  python scripts/data/ingest.py --source data/raw

# 3. Run processing
docker compose -f docker-compose.dev.yml run --rm dev \
  python scripts/data/process.py --batch-size 1000

# 4. Verify results
docker compose -f docker-compose.dev.yml run --rm dev \
  python scripts/data/verify.py
```

### Analysis

```bash
# Run analysis script
docker compose -f docker-compose.dev.yml run --rm dev \
  python scripts/analysis/run_analysis.py \
  --input-db myapp \
  --output-dir data/analysis/results

# Generate report
docker compose -f docker-compose.dev.yml run --rm dev \
  python scripts/analysis/generate_report.py \
  --input data/analysis/results \
  --format html
```

### Debugging

```bash
# Interactive shell with full environment
docker compose -f docker-compose.dev.yml run --rm dev bash

# Inside container:
python
>>> from libs.db import create_client
>>> client = create_client(host="localhost", port=9000)
>>> result = client.execute("SHOW DATABASES")
>>> print(result)
```

---

## Troubleshooting

### Container Issues

**Cannot connect to services:**
```bash
# Check if infrastructure is running
cd infrastructure
docker compose ps

# Check logs
docker compose logs -f postgres

# Restart services
docker compose restart
```

**Permission errors:**
```bash
# Fix volume permissions
docker compose -f docker-compose.dev.yml run --rm dev \
  chown -R $(id -u):$(id -g) /workspace/data
```

### Script Execution Issues

**Module not found:**
```bash
# Verify PYTHONPATH in container
docker compose -f docker-compose.dev.yml run --rm dev \
  python -c "import sys; print(sys.path)"

# Check docker-compose.dev.yml has PYTHONPATH set correctly
```

**Environment variables not loaded:**
```bash
# Verify .env file exists
ls -la .env

# Check variables in container
docker compose -f docker-compose.dev.yml run --rm dev \
  python -c "import os; print(os.getenv('POSTGRES_HOST'))"
```

---

## Related Documentation

- [`../infrastructure/README.md`](../infrastructure/README.md) - Infrastructure setup and management
- [`coding-standards.md`](coding-standards.md) - Code quality standards
- [`testing.md`](testing.md) - Testing guidelines
- [`rules.md`](rules.md) - General development rules
