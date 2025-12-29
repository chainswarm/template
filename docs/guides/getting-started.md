# Getting Started Guide

**Last Updated:** 2025-12-29  
**Purpose:** Comprehensive guide for setting up and using the agentic AI development template

---

## Prerequisites

### Required Software

- **Docker** 20.10 or later ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** V2 ([Included with Docker Desktop](https://docs.docker.com/compose/install/))
- **Git** ([Install Git](https://git-scm.com/downloads))

### Optional but Recommended

- **VSCode** with Remote - Containers extension
- **Python** 3.13+ (for local development without containers)

### Verify Installation

```bash
# Check Docker
docker --version
# Expected: Docker version 20.10.0 or later

# Check Docker Compose
docker compose version
# Expected: Docker Compose version v2.0.0 or later

# Check Git
git --version
# Expected: git version 2.0.0 or later
```

---

## Initial Setup

### 1. Create Repository from Template

**On GitHub:**
1. Navigate to the template repository
2. Click "Use this template" button
3. Name your new repository
4. Clone your repository:

   ```bash
   git clone https://github.com/your-username/your-project.git
   cd your-project
   ```

### 2. Configure Environment

**Create environment files:**

```bash
# Root environment file
cp .env.example .env

# Infrastructure environment file
cp infrastructure/.env.example infrastructure/.env
```

**Edit `.env`** (root):
```bash
# Application settings
ENVIRONMENT=development
LOG_LEVEL=INFO
LOGS_DIR=./logs

# Database connections (matching infrastructure)
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=myapp
# ... etc
```

**Edit `infrastructure/.env`:**
```bash
# Database credentials
POSTGRES_DB=myapp
POSTGRES_USER=dev
POSTGRES_PASSWORD=your_secure_password_here  # Change this!

# ClickHouse
CLICKHOUSE_DB=myapp

# Observability
GRAFANA_ADMIN_PASSWORD=your_secure_password_here  # Change this!
```

### 3. Start Infrastructure

**Using the helper script (recommended):**
```bash
bash scripts/dev/start-infra.sh
```

**Or manually:**
```bash
cd infrastructure
docker compose up -d
cd ..
```

**Verify services are running:**
```bash
cd infrastructure
docker compose ps
```

Expected output: All services should show "Up" status.

### 4. Build Development Container

```bash
docker compose -f docker-compose.dev.yml build dev
```

This creates the development environment with all dependencies.

---

## Verify Setup

### Test Infrastructure Services

**PostgreSQL:**
```bash
docker exec -it infra-postgres psql -U dev -d myapp -c "SELECT version();"
```

**Redis:**
```bash
docker exec -it infra-redis redis-cli ping
# Expected: PONG
```

**ClickHouse:**
```bash
curl http://localhost:8123/ping
# Expected: Ok.
```

### Test Development Container

```bash
docker compose -f docker-compose.dev.yml run --rm dev python --version
# Expected: Python 3.13.x
```

### Access Web UIs

- **ClickHouse Play:** http://localhost:8123/play
- **Prometheus:** http://localhost:9090 (if observability started)
- **Grafana:** http://localhost:3001 (if observability started)

---

## First Steps

### 1. Review AI Agent Guidelines

Read the core documentation:

```bash
# Core rules
cat roocode/rules.md

# Coding standards
cat roocode/coding-standards.md

# Testing philosophy
cat roocode/testing.md
```

**Key Takeaways:**
- Always check last 3 commits before making changes
- Use structured logging (no emoticons)
- Write tests for integration points and critical logic
- Run everything in Docker containers

### 2. Create Your First Script

Create `scripts/hello.py`:

```python
#!/usr/bin/env python3
"""
Hello World script demonstrating the template structure
"""
from dotenv import load_dotenv
from loguru import logger

from libs.observability import setup_logger


def main():
    load_dotenv()
    setup_logger("hello-world")
    
    logger.info(
        "Hello from agentic template!",
        environment="development",
        version="1.0.0"
    )
    
    logger.info("Script complete")


if __name__ == "__main__":
    main()
```

**Run it:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev python scripts/hello.py
```

**Check the logs:**
```bash
cat logs/hello-world.log
```

### 3. Work with Databases

**Create a test table in PostgreSQL:**

```bash
docker exec -it infra-postgres psql -U dev -d myapp
```

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username) VALUES ('alice'), ('bob');

SELECT * FROM users;

\q
```

**Create a script to query it (`scripts/query_users.py`):**

```python
#!/usr/bin/env python3
import os
import psycopg2
from dotenv import load_dotenv
from loguru import logger

from libs.observability import setup_logger


def main():
    load_dotenv()
    setup_logger("query-users")
    
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=int(os.getenv("POSTGRES_PORT")),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    logger.info("Found users", count=len(users))
    for user in users:
        logger.info("User", id=user[0], username=user[1], created_at=user[2])
    
    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
```

**Run it:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev python scripts/query_users.py
```

### 4. Document Your Session

Create today's session folder:

```bash
# Linux/Mac
mkdir -p docs/sessions/$(date +%Y%m%d)

# Windows
mkdir docs/sessions/20251229
```

Create `docs/sessions/20251229/initial-setup.md`:

```markdown
# Session: Initial Setup

**Date**: 2025-12-29  
**Time**: 14:30 UTC  
**Agent**: roocode

## Context

Setting up the agentic AI development template for the first time.

## Actions Taken

- Configured environment variables
- Started infrastructure services (PostgreSQL, Redis, ClickHouse)
- Created and tested first Python script
- Created users table in PostgreSQL
- Verified logging and observability setup

## Outcomes

- Infrastructure running successfully
- Can execute scripts in Docker container
- Logging works with JSON output
- Database accessible from scripts

## Next Steps

- [ ] Set up observability stack (Prometheus, Grafana)
- [ ] Create first real feature
- [ ] Write tests for the feature
```

---

## Development Workflows

### Working with Python Scripts

**Always use the development container:**

```bash
# One-off script
docker compose -f docker-compose.dev.yml run --rm dev python scripts/my_script.py

# With arguments
docker compose -f docker-compose.dev.yml run --rm dev python scripts/process.py --input data/file.csv

# Interactive shell for experimentation
docker compose -f docker-compose.dev.yml run --rm dev bash

# Inside the container:
python
>>> from libs.observability import setup_logger
>>> setup_logger("test")
>>> exit()
exit
```

### Using Core Libraries

**Observability:**

```python
from libs.observability import (
    setup_logger,
    setup_metrics,
    log_errors,
    manage_metrics
)

# Setup logging
setup_logger("my-service")

# Setup Prometheus metrics
metrics = setup_metrics("my-service", port=9091)

# Use decorators
@log_errors
def process_data(data):
    # Automatically logs errors with full context
    pass

@manage_metrics("processing_success", "processing_failure")
def process_batch(service_name, batch):
    # Automatically tracks success/failure metrics
    pass
```

**Database:**

```python
from libs.db import ClickHouseRepository
from clickhouse_driver import Client

client = Client(
    host="localhost",
    port=9000,
    database="myapp"
)

repo = ClickHouseRepository(client, "events")

# Insert data
repo.insert({"id": 1, "event_type": "click", "timestamp": "2024-01-01 00:00:00"})

# Query data
results = repo.query({"event_type": "click"})
```

### Git Workflow with AI Agents

**Before making changes:**

```bash
# Check last 3 commits
git log -3 --oneline --stat

# See what changed in the area you're modifying
git log -5 --oneline -- src/module_youre_changing.py

# Understand why changes were made
git show HEAD
```

**After making changes:**

```bash
# Review your changes
git diff

# Stage and commit with descriptive message
git add src/new_feature.py
git commit -m "Feature: Add pattern detection for cycles

Implements Floyd's cycle detection algorithm for finding
circular patterns in transfer graphs.

- Handles graphs up to 10,000 nodes
- Time complexity: O(n)
- Space complexity: O(1)"
```

See [`../../roocode/git-usage.md`](../../roocode/git-usage.md) for complete git workflows.

---

## Advanced Setup

### Enable Observability Stack

```bash
cd infrastructure/observability
docker compose up -d
cd ../..
```

**Access dashboards:**
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin / admin)
- Loki: http://localhost:3100

**Configure your app to export metrics:**

```python
from libs.observability import setup_metrics

# Start metrics server
metrics = setup_metrics("my-app", port=9091)

# Register with Prometheus
# Edit infrastructure/observability/prometheus/prometheus.yml
# Add:
# - job_name: 'my-app'
#   static_configs:
#     - targets: ['host.docker.internal:9091']
```

### VSCode Dev Container

**Open project in VSCode:**

1. Install "Remote - Containers" extension
2. Open project folder
3. Press F1 → "Remote-Containers: Reopen in Container"
4. VSCode will build and connect to the dev container

**Benefits:**
- Full IDE features inside container
- Extensions automatically installed
- Debugger configured
- Integrated terminal starts in container

---

## Troubleshooting

### Infrastructure Won't Start

**Check if ports are in use:**
```bash
# Linux/Mac
lsof -i :5432
lsof -i :6379

# Windows
netstat -ano | findstr :5432
netstat -ano | findstr :6379
```

**View service logs:**
```bash
cd infrastructure
docker compose logs postgres
docker compose logs redis
docker compose logs clickhouse
```

**Restart services:**
```bash
cd infrastructure
docker compose restart
```

### Can't Connect to Services

**Verify services are running:**
```bash
cd infrastructure
docker compose ps
```

**Test connectivity:**
```bash
# PostgreSQL
docker exec -it infra-postgres pg_isready

# Redis
docker exec -it infra-redis redis-cli ping

# ClickHouse
curl http://localhost:8123/ping
```

### Python Import Errors

**Verify PYTHONPATH:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev \
  python -c "import sys; print(sys.path)"
```

Should include `/workspace`.

**Rebuild container:**
```bash
docker compose -f docker-compose.dev.yml build dev --no-cache
```

---

## Next Steps

1. **Read the guidelines:**
   - [`../../roocode/rules.md`](../../roocode/rules.md)
   - [`../../roocode/coding-standards.md`](../../roocode/coding-standards.md)
   - [`../../roocode/testing.md`](../../roocode/testing.md)

2. **Explore infrastructure:**
   - [`../../infrastructure/README.md`](../../infrastructure/README.md)

3. **Explore libraries:**
   - [`../../libs/README.md`](../../libs/README.md)

4. **Start building:**
   - Create your first feature
   - Write integration tests
   - Add metrics and logging
   - Document your session

---

## Getting Help

- **Infrastructure issues:** See [`../../infrastructure/README.md`](../../infrastructure/README.md#troubleshooting)
- **Script execution:** See [`../../roocode/automode.md`](../../roocode/automode.md)
- **Git workflows:** See [`../../roocode/git-usage.md`](../../roocode/git-usage.md)
- **Testing:** See [`../../roocode/testing.md`](../../roocode/testing.md)

---

**Happy coding with AI! 🚀**
