# Scripts

Helper scripts for development and operations.

## Development Scripts (`dev/`)

### Infrastructure Management

**Start infrastructure services:**
```bash
bash scripts/dev/start-infra.sh
```

Starts PostgreSQL, Redis, and ClickHouse with Docker Compose.

**Stop infrastructure services:**
```bash
bash scripts/dev/stop-infra.sh
```

Stops all infrastructure services while preserving data volumes.

## Script Organization

```
scripts/
├── dev/                        # Development scripts
│   ├── start-infra.sh         # Start infrastructure
│   └── stop-infra.sh          # Stop infrastructure
├── data/                       # Data processing scripts (add as needed)
├── analysis/                   # Analysis scripts (add as needed)
└── README.md                   # This file
```

## Adding New Scripts

### Python Scripts

Create Python scripts in appropriate subdirectories:

```python
#!/usr/bin/env python3
"""
Script description
"""
from dotenv import load_dotenv
from loguru import logger

from libs.observability import setup_logger


def main():
    load_dotenv()
    setup_logger("script-name")
    
    logger.info("Script starting")
    # Your logic here
    logger.info("Script complete")


if __name__ == "__main__":
    main()
```

**Run with Docker:**
```bash
docker compose -f docker-compose.dev.yml run --rm dev python scripts/your_script.py
```

### Bash Scripts

Create bash scripts following the template:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Colors
readonly GREEN='\033[0;32m'
readonly NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

main() {
    log_info "Script starting"
    # Your logic here
}

main "$@"
```

**Make executable:**
```bash
chmod +x scripts/your_script.sh
```

## Best Practices

1. **Always set -euo pipefail** in bash scripts
2. **Include descriptive headers** explaining script purpose
3. **Use logging** from libs/observability in Python scripts
4. **Make scripts idempotent** where possible
5. **Check prerequisites** before execution
6. **Provide clear output** with colored messages
7. **Handle errors gracefully** with informative messages

## See Also

- [`../roocode/automode.md`](../roocode/automode.md) - Script execution patterns
- [`../infrastructure/README.md`](../infrastructure/README.md) - Infrastructure documentation
