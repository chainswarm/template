# Memory Bank

The Memory Bank is RooFlow's knowledge management system. It serves as the central source of truth for context, decisions, patterns, and progress.

---

## Purpose

Memory Bank replaces traditional `docs/agent/` directories with a structured system that:
- Provides consistent context across Flow mode switches
- Documents decisions and patterns as they emerge
- Tracks project progress and active work
- Serves as queryable knowledge for Ask mode

---

## Structure

### Core Files

1. **systemPatterns.md** - Development patterns and conventions
   - Code quality standards
   - Testing philosophy
   - Error handling patterns
   - Common bug patterns
   - Infrastructure patterns

2. **decisionLog.md** - Architecture Decision Records (ADRs)
   - Major technical decisions
   - Technology choices
   - Design trade-offs
   - Abandoned approaches

3. **productContext.md** - Product requirements and domain knowledge
   - Business rules
   - User workflows
   - Domain terminology
   - Feature specifications

4. **progress.md** - Project progress tracking
   - Current milestones
   - Completed work
   - Blockers and risks
   - Next steps

5. **activeContext.md** - Current work context
   - Active tasks
   - Recent changes
   - Immediate priorities
   - Temporary notes

---

## Usage

### When to Update

**systemPatterns.md:**
- After establishing new code pattern
- After discovering bug pattern
- When defining new convention
- After infrastructure changes

**decisionLog.md:**
-After making architecture decisions
- After evaluating technology options
- When choosing design approach
- When documenting trade-offs

**productContext.md:**
- After clarifying requirements
- When adding new features
- After domain discovery
- When business rules change

**progress.md:**
- After completing milestones
- When tasks change status
- After discovering blockers
- At project checkpoints

**activeContext.md:**
- When starting new work
- After mode switches
- When context changes
- For temporary notes

---

## Flow Mode Integration

### Architect Mode
- Reads: productContext, decisionLog, systemPatterns
- Writes: decisionLog (ADRs), systemPatterns (new patterns)

### Code Mode
- Reads: systemPatterns, decisionLog  
- Writes: systemPatterns (new patterns, bug fixes)

### Debug Mode
- Reads: systemPatterns, progress
- Writes: systemPatterns (bug patterns)

### Ask Mode
- Reads: ALL files
- Writes: None (read-only)

### Orchestrator Mode
- Reads: ALL files
- Writes: progress, activeContext, decisionLog

---

## Best Practices

**DO:**
- ✓ Update Memory Bank immediately after decisions
- ✓ Reference Memory Bank in mode rules
- ✓ Keep systemPatterns current
- ✓ Document "why" not "what"
- ✓ Cross-reference related sections

**DON'T:**
- ❌ Let Memory Bank get stale
- ❌ Duplicate information across files
- ❌ Write implementation details (use code comments)
- ❌ Leave undocumented decisions
- ❌ Forget to update after pattern changes

---

## Template Usage

When initializing a new project:

1. Copy `memory-bank-template/` to `memory-bank/`
2. Rename `.template` files (remove extension)
3. Fill in project-specific information
4. Update systemPatterns.md with project conventions
5. Start documenting decisions as you make them

---

## Example Workflow

### Making an Architecture Decision

1. **Research** - Gather options
2. **Document in decisionLog.md**:
   ```markdown
   # ADR-001: Choose PostgreSQL for Transactional Data
   
   **Status:** Accepted
   **Date:** 2025-12-29
   **Context:** Need ACID guarantees for financial transactions
   
   ## Decision
   Use PostgreSQL for core transactional data
   
   ## Rationale
   - ACID compliance required
   - Strong consistency model
   - Mature ecosystem
   
   ## Consequences
   **Positive:**
   - Reliable transactions
   - SQL query power
   
   **Negative:**
   - Vertical scaling limits
   - More complex sharding
   ```

3. **Update systemPatterns.md** if establishing new pattern:
   ```markdown
   ## Database Patterns
   
   ### Transactional Data
   
   Use PostgreSQL with connection pooling from `libs/db/base.py`:
   
   \`\`\`python
   from libs.db.base import get_session
   
   with get_session() as session:
       result = session.execute(query)
   \`\`\`
   ```

### Discovering a Bug Pattern

1. **Fix the bug** (with test)
2. **Document in systemPatterns.md**:
   ```markdown
   ## Bug Patterns
   
   ### Empty String Validation
   
   **Problem:** `if value:` treats empty string as falsy
   
   **Solution:**
   \`\`\`python
   # ✓ Explicit check
   if value is not None and value != "":
       process(value)
   \`\`\`
   
   **When discovered:** 2025-12-29
   **Related test:** test_empty_string_validation
   ```

---

## Related Documentation

- [`.roo/rules-flow-*/`](../.roo/) - Mode-specific rules that reference Memory Bank
- [`libs/`](../libs/) - Implementation patterns documented here
- [`infrastructure/`](../infrastructure/) - Infrastructure patterns documented here
