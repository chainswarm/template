# Ask Mode Rules

**Mode Purpose:** Explanations, documentation, and answers to technical questions.

---

## Query Process

### 1. Check Memory Bank First

Before answering, consult:
- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) - Development patterns
- [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md) - Past decisions
- [`memory-bank/productContext.md`](../../memory-bank/productContext.md) - Product context
- [`memory-bank/activeContext.md`](../../memory-bank/activeContext.md) - Current work

**Ground answers in project-specific knowledge.**

---

### 2. Reference systemPatterns.md

When explaining code patterns or best practices:

```markdown
## Question: How should I handle errors in this project?

According to [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md):

**Fail-fast philosophy:**
- Validate inputs immediately at boundaries
- Raise specific exceptions (never return None silently)
- No default values for invalid inputs

**Example:**
```python
def process_transfer(transfer_id: str, amount: float) -> Transfer:
    if not transfer_id:
        raise ValueError("transfer_id cannot be empty")
    if amount <= 0:
        raise ValueError(f"Invalid amount: {amount}")
    # ... rest of processing
```

See [`libs/`](../../libs/) for error handling patterns used in this project.
```

---

## Answer Guidelines

### Be Concise and Actionable

```markdown
# ❌ Too verbose
The question you're asking about database connections is interesting. There are many 
ways to handle this. You could use connection pooling, or you could create connections 
on demand. Some people prefer...

# ✓ Concise and actionable
Use connection pooling from [`libs/db/base.py`](../../libs/db/base.py):

```python
from libs.db.base import get_session

with get_session() as session:
    result = session.execute(query)
```

This reuses connections and handles cleanup automatically.
```

---

### Include Code Examples

```python
# Always show concrete examples from the project
from libs.observability.logging import get_logger

logger = get_logger(__name__)

logger.info(
    "Processing started",
    item_id=item.id,
    status="started"
)
```

---

### Reference Actual Files

Link to actual project files:
- [`libs/observability/logging.py`](../../libs/observability/logging.py) for logging
- [`infrastructure/docker-compose.yml`](../../infrastructure/docker-compose.yml) for infrastructure
- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) for patterns

---

## Suggest Appropriate Modes

### Route to Specialized Modes

When questions require action:

**For design questions:**
```markdown
This requires architectural design. I suggest switching to **Architect mode** to:
1. Create system design
2. Document in Memory Bank
3. Create implementation plan
```

**For implementation questions:**
```markdown
This requires code changes. I suggest switching to **Code mode** to:
1. Implement the feature
2. Add tests
3. Update systemPatterns.md
```

**For debugging:**
```markdown
This looks like a bug. I suggest switching to **Debug mode** to:
1. Reproduce with a test
2. Investigate using observability stack
3. Fix and document the pattern
```

**For deployments:**
```markdown
This requires infrastructure changes. I suggest switching to **DevOps mode** to:
1. Update infrastructure configuration
2. Deploy changes
3. Verify with monitoring
```

---

## Knowledge Sources

### Project Structure

Reference appropriate documentation:

**For infrastructure questions:**
- [`infrastructure/README.md`](../../infrastructure/README.md)
- [`infrastructure/observability/`](../../infrastructure/observability/)
- [`docker-compose.dev.yml`](../../docker-compose.dev.yml)

**For code patterns:**
- [`libs/`](../../libs/) - Reusable libraries
- [`scripts/`](../../scripts/) - Script examples
- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md)

**For development setup:**
- [`.devcontainer/`](../../.devcontainer/)
- [`.env.example`](../../.env.example)
- [`pyproject.toml.example`](../../pyproject.toml.example)

---

## Answer Structure

### Standard Format

```markdown
## [Question Topic]

**Short Answer:**
[One-sentence summary]

**Details:**
[2-3 paragraphs with specifics]

**Code Example:**
```python
# Concrete example from the project
```

**Related Resources:**
- [`file/path.py`](../../file/path.py) - Description
- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) - Pattern reference

**Next Steps:**
[What to do with this information]
```

---

## Common Question Types

### "How do I...?"

1. Check if pattern exists in [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md)
2. Reference existing code in [`libs/`](../../libs/)
3. Provide minimal working example
4. Suggest mode if implementation needed

### "Why does...?"

1. Check [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md) for decisions
2. Explain with code/log examples
3. Suggest Debug mode if it's a bug
4. Reference observability stack for investigation

### "What is...?"

1. Define concretely
2. Show where it's used in the project
3. Provide usage example
4. Link to relevant documentation

### "Should I...?"

1. Reference systemPatterns.md for conventions
2. Provide recommendation with rationale
3. Show pros/cons
4. Suggest Architect mode if design needed

---

## Don'ts

**Never:**
- ❌ Answer without checking Memory Bank
- ❌ Provide generic answers (use project specifics)
- ❌ Give long explanations without code examples
- ❌ Forget to suggest appropriate mode for actions
- ❌ Reference patterns that don't exist in the project

**Always:**
- ✓ Ground answers in Memory Bank
- ✓ Provide concrete code examples
- ✓ Reference actual project files
- ✓ Be concise and actionable
- ✓ Suggest mode switches when appropriate

---

## Examples

### Good Answer

```markdown
## How should I log structured data?

Use loguru with structured fields from [`libs/observability/logging.py`](../../libs/observability/logging.py):

```python
from libs.observability.logging import get_logger

logger = get_logger(__name__)

logger.info(
    "Processing transfer",
    transfer_id=transfer.id,
    amount=transfer.amount,
    status="started"
)
```

**Never use emoticons** (🚀, ✅, ❌) in logs per [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md).

See [`infrastructure/observability/loki/`](../../infrastructure/observability/loki/) for log aggregation setup.
```

### Bad Answer

```markdown
## How should I log?

You can use various logging libraries. Python has built-in logging or you could use 
loguru. Some people like structured logging, others prefer simple strings. It really 
depends on your use case and preferences. Here are some options you might consider...

[Too verbose, no project specifics, no code example]
```

---

## Related Documentation

- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) - Primary knowledge source
- [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md) - Past decisions
- [`libs/README.md`](../../libs/README.md) - Code patterns
- [`infrastructure/README.md`](../../infrastructure/README.md) - Infrastructure
