# Template Usage Guide

## Important: Example Files

This template includes **example files** that won't interfere with template syncing:

-  **`pyproject.toml.example`** - Example Python project configuration
- **`libs-example/`** - Example core library modules

### Why Example Files?

Since this template repository is updated regularly and projects created from it will sync changes, we cannot include actual project files. Instead, we provide examples that you copy and customize.

##  Getting Started

### 1. Create Project Configuration

**Option A: Using pyproject.toml (recommended)**
```bash
# Copy example and customize
cp pyproject.toml.example pyproject.toml

# Edit pyproject.toml
# - Update project name
# - Add your dependencies
# - Customize settings
```

**Option B: Using requirements.txt**
```bash
# Create requirements.txt
cat > requirements.txt <<EOF
loguru>=0.7.0
python-dotenv>=1.0.0
# Add your dependencies here
EOF
```

### 2. Copy Core Libraries (Optional)

If you want to use the example libraries:

```bash
# Copy entire libs-example to libs/
cp -r libs-example libs

# Or copy individual modules
cp -r libs-example/observability libs/
cp -r libs-example/db libs/
```

Then install their dependencies:
```bash
# For observability
uv add loguru prometheus-client

# For database
uv add clickhouse-driver  # Or your database driver
```

### 3. Create Your Project Structure

```bash
# Create your source directory
mkdir -p src/your_project

# Or organize however you prefer
mkdir -p packages/
mkdir -p scripts/
```

---

## Working with the Development Container

### Build Container (First Time)

```bash
docker compose -f docker-compose.dev.yml build
```

### Run Scripts

```bash
# Interactive shell
docker compose -f docker-compose.dev.yml run --rm dev bash

# Run a Python script
docker compose -f docker-compose.dev.yml run --rm dev python src/your_script.py
```

### Install Packages Freely

Agents and developers can install packages as needed:

```bash
# Inside container
uv pip install requests pandas numpy

# Add as permanent dependency
uv add requests pandas
```

---

## Template Sync

When the template is updated, you can sync changes:

```bash
# Add template as remote (one time)
git remote add template https://github.com/your-org/template

# Fetch template updates
git fetch template main

# Merge template changes
git merge template/main --allow-unrelated-histories

# Resolve conflicts if any
# ... edit conflicting files ...
git add .
git commit
```

**Safe to sync** because:
- `pyproject.toml` is in `.gitignore` (you use `pyproject.toml`, template has `pyproject.toml.example`)
- `libs/` is in `.gitignore` (you use `libs/`, template has `libs-example/`)
- Infrastructure and docs can be safely updated

---

##  Example Workflows

### New Python Project

```bash
# 1. Copy pyproject.toml
cp pyproject.toml.example pyproject.toml
# Edit and set name = "my-project"

# 2. Create source structure
mkdir -p src/my_project
touch src/my_project/__init__.py

# 3. Build dev container
docker compose -f docker-compose.dev.yml build

# 4. Start developing
docker compose -f docker-compose.dev.yml run --rm dev bash
```

### Using Example Libraries

```bash
# 1. Copy libraries you need
cp -r libs-example/observability libs/

# 2. Install dependencies
uv add loguru prometheus-client

# 3. Use in your code
# src/my_project/main.py
from libs.observability import setup_logger
setup_logger("my-app")
```

---

## File Organization

```
your-project/           # Created from template
├── pyproject.toml     # Created from pyproject.toml.example (gitignored)
├── src/               # Your code (gitignored by default)
│   └── your_project/
├── libs/              # Copied from libs-example (git ignored by default)
│   ├── observability/
│   └── db/
├── scripts/           # Your scripts
├── infrastructure/    # From template (safe to sync)
├── roocode/          # From template (safe to sync)
└── docs/             # From template (safe to sync)
```

---

## Questions?

See the full documentation:
- [`README.md`](README.md) - Main project README
- [`roocode/automode.md`](roocode/automode.md) - Execution patterns
- [`infrastructure/README.md`](infrastructure/README.md) - Infrastructure setup
- [`libs-example/README.md`](libs-example/README.md) - Library usage

