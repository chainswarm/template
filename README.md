# AI Coding Baseline Template

A language-agnostic GitHub template for AI-assisted coding projects using roocode and other AI agents.

## 📋 Overview

This template provides a standardized structure for projects that utilize AI coding assistants. It focuses on documentation, session tracking, and maintaining a clear history of AI-human collaboration.

## 🎯 Purpose

- **Organized Documentation**: Keep track of all AI agent conversations and decisions
- **Session Management**: Structured approach to logging development sessions
- **Language Agnostic**: Works with any programming language or framework
- **Collaboration Ready**: Clear guidelines for team members working with AI agents

## 📁 Project Structure

```
.
├── roocode/                    # AI agent rules and guidelines
│   ├── rules.md               # Core development rules
│   ├── coding-standards.md    # Code quality standards
│   ├── testing.md             # Testing guidelines
│   ├── automode.md            # Execution patterns
│   └── git-usage.md           # Git workflows for AI agents
├── infrastructure/             # Production-ready infrastructure
│   ├── docker-compose.yml     # Core services (Postgres, Redis, ClickHouse)
│   ├── .env.example           # Environment variables template
│   ├── README.md              # Infrastructure documentation
│   └── observability/         # Observability stack
│       ├── docker-compose.yml # Prometheus, Loki, Grafana
│       ├── prometheus/        # Metrics configuration
│       ├── loki/              # Log aggregation config
│       ├── promtail/          # Log shipper config
│       └── grafana/           # Visualization config
├── libs/                       # Core library modules
│   ├── observability/         # Logging, metrics, shutdown
│   ├── db/                    # Database patterns
│   └── README.md              # Library documentation
├── scripts/                    # Helper scripts
│   ├── dev/                   # Development scripts
│   │   ├── start-infra.sh    # Start infrastructure
│   │   └── stop-infra.sh     # Stop infrastructure
│   └── README.md              # Scripts documentation
├── docs/
│   ├── sessions/              # AI conversation logs (organized by date)
│   │   ├── README.md         # Session documentation guide
│   │   └── YYYYMMDD/         # Daily session folders
│   ├── architecture/          # Architecture decisions and diagrams
│   └── guides/               # Project-specific guides
├── .devcontainer/             # VSCode dev container config
├── docker-compose.dev.yml     # Development container
├── Dockerfile.dev             # Development image
├── .env.example               # Root environment template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Using This Template

1. **Click "Use this template"** on GitHub to create a new repository
2. **Clone your new repository**:
   ```bash
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```
3. **Setup environment**:
   ```bash
   # Copy environment template
   cp .env.example .env
   cp infrastructure/.env.example infrastructure/.env
   
   # Review and update .env files with your configuration
   ```

4. **Start infrastructure**:
   ```bash
   # Option 1: Use helper script
   bash scripts/dev/start-infra.sh
   
   # Option 2: Manual
   cd infrastructure && docker compose up -d
   ```

5. **Build development container**:
   ```bash
   docker compose -f docker-compose.dev.yml build dev
   ```

6. **Review the roocode rules**: Check [`roocode/rules.md`](roocode/rules.md) for AI interaction guidelines

### Daily Workflow with Infrastructure

1. **Start infrastructure** (if not running):
   ```bash
   bash scripts/dev/start-infra.sh
   ```

2. **Run Python scripts**:
   ```bash
   docker compose -f docker-compose.dev.yml run --rm dev python scripts/your_script.py
   ```

3. **Interactive development shell**:
   ```bash
   docker compose -f docker-compose.dev.yml run --rm dev bash
   ```

4. **Document the session**: Save conversation summaries in `docs/sessions/YYYYMMDD/`
   - Use the template provided in [`docs/sessions/README.md`](docs/sessions/README.md)

5. **Monitor with observability** (optional):
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001
   - View logs in Loki via Grafana

### Quick Access to Services

Once infrastructure is running:

| Service | URL | Credentials |
|---------|-----|-------------|
| PostgreSQL | `localhost:5432` | dev / dev_password |
| Redis | `localhost:6379` | (no auth) |
| ClickHouse HTTP | http://localhost:8123 | default / (no auth) |
| ClickHouse Native | `localhost:9000` | default / (no auth) |
| Prometheus | http://localhost:9090 | (no auth) |
| Grafana | http://localhost:3001 | admin / admin |
| Loki | http://localhost:3100 | (no auth) |

## 📝 Documentation Rules

### Session Documentation (Rule #1)

**All conversations with AI agents must be documented in `docs/sessions/{YYYYMMDD}/`**

- Create a new folder for each day using `YYYYMMDD` format
- Save conversation logs as markdown files
- Include context, decisions, and outcomes

See [`roocode/rules.md`](roocode/rules.md) for complete guidelines.

## 🤖 AI Agent Guidelines

This template is designed to work with:
- **roocode** (primary)
- GitHub Copilot
- ChatGPT / Claude / other LLM interfaces
- Custom AI agents

## 🏗️ Infrastructure

### Core Services

- **PostgreSQL** - Relational database for structured data
- **Redis** - Cache and message broker
- **ClickHouse** - Analytics database for time-series and large-scale data

### Observability Stack

- **Prometheus** - Metrics collection and alerting
- **Loki** - Log aggregation
- **Grafana** - Unified visualization for metrics and logs
- **Promtail** - Log shipping to Loki

See [`infrastructure/README.md`](infrastructure/README.md) for complete documentation.

## 🤖 Agentic Development

This template includes comprehensive guidelines for AI-assisted development in the [`roocode/`](roocode/) directory:

- [`rules.md`](roocode/rules.md) - Core development rules and principles
- [`coding-standards.md`](roocode/coding-standards.md) - Code quality standards
- [`testing.md`](roocode/testing.md) - Testing philosophy and practices
- [`automode.md`](roocode/automode.md) - Script execution patterns
- [`git-usage.md`](roocode/git-usage.md) - Git workflows for AI agents

### Key Principles

**1. Check Last 3 Commits** - Always understand code evolution:
```bash
git log -3 --oneline --stat
```

**2. Fail-Fast Validation** - Validate inputs early:
```python
if not transfer_id:
    raise ValueError("transfer_id cannot be empty")
```

**3. Structured Logging** - Use key-value pairs, no emoticons:
```python
logger.info("Transfer processed", transfer_id=transfer_id, amount=amount)
```

**4. Container-Based Execution** - Run all scripts in Docker:
```bash
docker compose -f docker-compose.dev.yml run --rm dev python script.py
```

### Core Libraries

The [`libs/`](libs/) directory provides production-ready modules - see [`libs/README.md`](libs/README.md):

- **observability** - Logging, metrics, shutdown handling
- **db** - Repository patterns and database utilities

## 📂 Directory Details

### `roocode/`
Comprehensive AI agent guidelines including rules,coding standards, testing philosophy, execution patterns, and git workflows.

### `infrastructure/`
Production-ready infrastructure with Docker Compose configurations for databases, caching, analytics, and full observability stack.

### `libs/`
Core library modules providing observability (logging, metrics) and database patterns for rapid development.

### `scripts/`
Helper scripts for infrastructure management and common development tasks.

### `docs/sessions/`
Organized logs of AI-assisted development sessions. Each day gets its own folder (YYYYMMDD format).

### `docs/architecture/`
Architecture decisions, system designs, and technical diagrams.

### `docs/guides/`
Project-specific guides, setup instructions, and best practices.

## 🔧 Customization

This template is meant to be adapted to your needs:

1. **Add your tech stack**: Include language-specific files (package.json, requirements.txt, etc.)
2. **Update rules**: Modify [`roocode/rules.md`](roocode/rules.md) with project-specific guidelines
3. **Extend documentation**: Add more folders under `docs/` as needed
4. **Configure git**: Update [`.gitignore`](.gitignore) for your project's needs

## 📖 Additional Resources

### AI Agent Guidelines
- [Rules](roocode/rules.md) - Core development rules
- [Coding Standards](roocode/coding-standards.md) - Code quality guidelines
- [Testing](roocode/testing.md) - Testing philosophy
- [Automode](roocode/automode.md) - Execution patterns
- [Git Usage](roocode/git-usage.md) - Git workflows

### Infrastructure & Libraries
- [Infrastructure Guide](infrastructure/README.md) - Complete infrastructure documentation
- [Core Libraries](libs/README.md) - Observability and database modules
- [Scripts](scripts/README.md) - Helper scripts documentation

### Documentation
- [Session Guide](docs/sessions/README.md) - How to document AI sessions
- [Session History](docs/sessions/) - Your conversation logs

## 🤝 Contributing

When contributing to projects using this template:

1. Follow the roocode rules in [`roocode/rules.md`](roocode/rules.md)
2. Document your AI-assisted sessions
3. Keep the session logs organized by date
4. Update architecture docs when making significant changes

## 📄 License

This template is provided as-is for use in your projects. Customize freely.

---

**Happy coding with AI! 🚀**
