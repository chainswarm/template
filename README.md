# RooFlow Extended Template

Production-ready RooFlow template with complete infrastructure, observability, and development tooling.

---

## What is RooFlow?

RooFlow is an AI-assisted development framework with specialized **Flow modes** that work together through a **Memory Bank** knowledge system. Each mode has specific responsibilities and shares context through structured documentation.

### Flow Modes

- 🏗️ **Architect** - System design, architecture decisions, documentation
- 💻 **Code** - Implementation, refactoring, code quality
- 🪲 **Debug** - Troubleshooting, bug fixes, test-driven debugging
- ❓ **Ask** - Questions, explanations, knowledge queries
- 🪃 **Orchestrator** - Multi-phase project coordination

---

## Features

### 🧠 Memory Bank System

Central knowledge management replacing traditional docs/agent/ approach:
- **systemPatterns.md** - Development patterns and conventions
- **decisionLog.md** - Architecture Decision Records (ADRs)
- **productContext.md** - Product requirements and domain knowledge
- **progress.md** - Project tracking and milestones
- **activeContext.md** - Current work and priorities

### 🏗️ Complete Infrastructure

- **Docker Compose** - Development environment
- **Observability Stack** - Prometheus, Grafana, Loki, Promtail
- **Container Devtools** - Python 3.13+, uv package manager
- **Database Support** - PostgreSQL, ClickHouse, Redis ready

### 📚 Reusable Libraries

Production-ready [`libs/`](./libs/) package with:
- **observability/** - Structured logging, metrics, decorators
- **db/** - Database connection patterns, utilities

### 🛠️ Development Tooling

- **VSCode Integration** - Settings, tasks, launch configs (WSL default terminal)
- **Scripts** - Infrastructure management, utilities
- **DevContainer** - Complete containerized dev environment
- **.gitignore** - Comprehensive ignore patterns

---

## Quick Start

### 1. Install RooFlow

Run the installer (creates .roomodes, Flow prompts, Memory Bank):

```bash
bash install_rooflow_conport.sh
```

The installer will:
- Configure RooFlow modes
- Initialize Memory Bank from templates
- Optionally create pyproject.toml
- Optionally start infrastructure

### 2. Initialize Your Project

```bash
# Copy Memory Bank templates (if not done by installer)
cp -r memory-bank-template memory-bank
for f in memory-bank/*.template; do mv "$f" "${f%.template}"; done

# Create pyproject.toml from example
cp pyproject.toml.example pyproject.toml

# Customize for your project
nano pyproject.toml  # Update name, dependencies, etc.
```

### 3. Start Infrastructure

```bash
# Start all infrastructure services
bash scripts/dev/start-infra.sh

# Check services are running
cd infrastructure && docker compose ps
```

**Available services:**
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- ClickHouse: `localhost:9000` (native), `:8123` (HTTP)
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (admin/admin)
- Loki: `http://localhost:3100`

### 4. Set Up Python Environment

```bash
# Install dependencies with uv
uv pip install -e .
uv pip install -e ".[dev]"

# Run tests
pytest
```

### 5. Use Flow Modes

Interact with specia lized modes through your AI assistant:
- **"Switch to Architect mode"** - Design system architecture
- **"Switch to Code mode"** - Implement features
- **"Switch to Debug mode"** - Fix bugs with TDD approach
- **"Switch to Ask mode"** - Query Memory Bank
- **"Switch to Orchestrator mode"** - Coordinate complex projects

---

## Project Structure

```
.
├── .roo/
│   ├── rules-flow-architect/   # Architect mode rules
│   ├── rules-flow-code/         # Code mode rules
│   ├── rules-flow-debug/        # Debug mode rules
│   ├── rules-flow-ask/          # Ask mode rules
│   ├── rules-flow-orchestrator/ # Orchestrator mode rules
│   └── system-prompt-flow-*     # Mode system prompts
│
├── memory-bank/                 # Knowledge management
│   ├── systemPatterns.md        # Development patterns
│   ├── decisionLog.md           # ADRs
│   ├── productContext.md        # Product knowledge
│   ├── progress.md              # Project tracking
│   └── activeContext.md         # Current work
│
├── libs/                        # Reusable Python package
│   ├── observability/           # Logging, metrics
│   └── db/                      # Database utilities
│
├── infrastructure/              # Docker infrastructure
│   ├── docker-compose.yml       # Core services
│   └── observability/           # Monitoring stack
│
├── scripts/                     # Utility scripts
│   └── dev/                     # Development scripts
│
├── .vscode/                     # VSCode configuration
├── .devcontainer/               # DevContainer setup
├── docker-compose.dev.yml       # Development container
├── Dockerfile.dev               # Dev container image
├── pyproject.toml.example       # Python project config
└── .env.example                 # Environment variables
```

---

## Memory Bank Usage

### systemPatterns.md

Document reusable patterns:

```markdown
## Error Handling

### Fail-Fast Pattern

```python
def process(data: dict) -> Result:
    if not data.get("id"):
        raise ValidationError("ID required")
    # ... process
```
```

### decisionLog.md

Track architecture decisions:

```markdown
# ADR-001: Use PostgreSQL for Transactional Data

**Status:** Accepted
**Date:** 2025-12-29

##  Decision
Use PostgreSQL for core transactional data.

## Rationale
- ACID compliance required
- Proven at scale
- Strong ecosystem
```

### Update After Changes

**Code mode writes to:**
- systemPatterns.md (new patterns, bug fixes)

**Architect mode writes to:**
- decisionLog.md (ADRs)
- systemPatterns.md (architectural patterns)

**All modes read from:**
- All Memory Bank files for context

---

## Infrastructure

### Services

Start/stop infrastructure:

```bash
# Start
bash scripts/dev/start-infra.sh

# Stop
bash scripts/dev/stop-infra.sh
```

### Observability

**Access Grafana:**
```
http://localhost:3001
Username: admin
Password: admin
```

**Query logs in Loki:**
- Use Grafana Explore
- Select Loki datasource
- Query: `{job="your-app"}`

**View metrics:**
- Prometheus: `http://localhost:9090`
- Custom metrics exposed on your app

### Using libs Package

```python
from libs.observability.logging import get_logger
from libs.observability.decorators import with_timing
from libs.db.base import get_session

logger = get_logger(__name__)

@with_timing("process_transfer")
def process_transfer(transfer_id: str):
    logger.info("Processing transfer", transfer_id=transfer_id)
    
    with get_session() as session:
        # ... database operations
        pass
```

---

## Development Workflow

### Using Docker Dev Container

```bash
# Run Python script
docker compose run --rm dev python scripts/my_script.py

# Interactive Python
docker compose run --rm dev python

# Run tests
docker compose run --rm dev pytest

# Shell access
docker compose run --rm dev bash
```

### Package Management with uv

```bash
# Install package
uv pip install requests

# Add to permanent dependencies
uv add requests

# Install dev dependencies
uv add --dev pytest-mock

# Update dependencies
uv pip install -r pyproject.toml
```

---

## Flow Mode Guidelines

### When to Use Each Mode

**Architect:**
- Designing new systems
- Making technology choices
- Creating ADRs
- Planning large refactorings

**Code:**
- Implementing features
- Writing tests
- Refactoring code
- Updating systemPatterns.md

**Debug:**
- Investigating bugs
- Writing reproduction tests
- Performance troubleshooting
- Documenting bug patterns

**Ask:**
- Querying Memory Bank
- Understanding existing code
- Getting recommendations
- Learning about project patterns

**Orchestrator:**
- Multi-phase projects
- Coordinating across modes
- Long-running refactorings
- Complex feature implementations

---

## Customization

### Customize Memory Bank

Edit templates in [`memory-bank-template/`](./memory-bank-template/) before initialization, or update [`memory-bank/`](./memory-bank/) directly after setup.

### Add Dependencies

Update [`pyproject.toml`](./pyproject.toml.example):

```toml
dependencies = [
    "loguru>=0.7.0",
    "your-package>=1.0.0",  # Add here
]
```

### Add Infrastructure Services

Edit [`infrastructure/docker-compose.yml`](./infrastructure/docker-compose.yml):

```yaml
services:
  your-service:
    image: your-image:latest
    ports:
      - "8080:8080"
```

---

## Documentation

- [`TEMPLATE_USAGE.md`](./TEMPLATE_USAGE.md) - Complete template guide
- [`memory-bank/README.md`](./memory-bank-template/README.md) - Memory Bank system
- [`infrastructure/README.md`](./infrastructure/README.md) - Infrastructure setup
- [`libs/README.md`](./libs/README.md) - Library usage
- [`scripts/README.md`](./scripts/README.md) - Script documentation

---

## Related Projects

- [RooFlow](https://github.com/GreatScottyMac/RooFlow) - Core RooFlow framework
- [Roo Code](https://roo.codeium.com) - AI coding assistant

---

## License

This template is provided as-is for use in your projects.
