# Orchestrator Mode Rules

**Mode Purpose:** Coordinate complex, multi-step projects that require delegation across different specialties.

---

## When to Use Orchestrator Mode

Use Orchestrator when:
- Task spans multiple domains (architecture + code + devops)
- Need to coordinate work across mode switches
- Complex project with many phases
- Requires tracking progress across sub-tasks

**Don't use for:**
- Simple, single-mode tasks
- Quick fixes or one-off changes
- Tasks that fit cleanly in one mode

---

## Orchestration Process

### 1. Break Down the Work

Decompose complex tasks into mode-specific subtasks:

```markdown
## Project: New Payment API

### Phase 1: Design (Architect Mode)
- Design API architecture
- Create data models
- Document in Memory Bank

### Phase 2: Infrastructure (DevOps Mode)
- Set up database
- Configure observability
- Create deployment pipeline

### Phase 3: Implementation (Code Mode)
- Implement API endpoints
- Add tests
- Update systemPatterns.md

### Phase 4: Validation (Debug Mode)
- Integration testing
- Performance testing
- Bug fixes
```

---

### 2. Delegate to Specialized Modes

**Switch to appropriate modes:**

```markdown
**Switching to Architect mode** to design the API architecture.

[After Architect mode completes...]

**Switching to Code mode** to implement the API based on the design in 
`memory-bank/decisionLog.md`.

[After Code mode completes...]

**Switching to DevOps mode** to deploy the API to staging environment.
```

---

### 3. Track Progress

**Maintain progress in Memory Bank:**

Update [`memory-bank/progress.md`](../../memory-bank/progress.md):

```markdown
# Payment API Project Progress

## Completed
- [x] API architecture designed (2025-12-29)
- [x] Database schema created (2025-12-29)
- [x] Core endpoints implemented (2025-12-30)

## In Progress
- [ ] Integration tests (50% complete)

## Blocked
- [ ] Deployment (waiting for infrastructure approval)

## Next Steps
1. Complete integration tests (Debug mode)
2. Performance testing (Debug mode)
3. Deploy to staging (DevOps mode)
```

---

### 4. Maintain Consistent Decisions

**Ensure decisions align across phases:**

Before switching modes, document context in Memory Bank:
- What was decided
- Why it was decided
- Constraints for next phase

```markdown
## Context for Code Mode

Based on architecture in `decisionLog.md`:
- Use REST API (not GraphQL) for simplicity
- PostgreSQL for transactional data
- Redis for caching (TTL: 5 minutes)
- Follow patterns from `libs/db/base.py`

Constraints:
- Must support 1000 req/sec
- Response time < 100ms (p95)
- Must integrate with existing auth system
```

---

## Delegation Patterns

### For Architecture Tasks

```markdown
**Switching to Architect mode** to:
- Design [component/feature]
- Create architecture diagram
- Document in decisionLog.md

Expected output: Design in Memory Bank, ready for implementation.
```

### For Implementation Tasks

```markdown
**Switching to Code mode** to:
- Implement [feature] per design in Memory Bank
- Add integration tests
- Update systemPatterns.md with new patterns

Requirements: Follow patterns from `libs/` and `memory-bank/systemPatterns.md`.
```

### For Debugging Tasks

```markdown
**Switching to Debug mode** to:
- Investigate [issue]
- Reproduce with failing test
- Fix and document pattern

Context: [Provide error logs, steps to reproduce].
```

### For DevOps Tasks

```markdown
**Switching to DevOps mode** to:
- Deploy [service] to [environment]
- Configure monitoring
- Verify deployment

Requirements: [List infrastructure requirements].
```

---

## Memory Bank Coordination

### Central Knowledge Hub

Use Memory Bank as coordination point:

**Before delegating:**
- Update [`memory-bank/activeContext.md`](../../memory-bank/activeContext.md) with current work
- Ensure previous decisions documented in [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md)
- Check [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) for relevant patterns

**After mode switch:**
- Verify Memory Bank was updated
- Extract key decisions for next phase
- Update progress tracking

---

## Project Planning

### High-Level Plans in Memory Bank

Document project structure in [`memory-bank/activeContext.md`](../../memory-bank/activeContext.md):

```markdown
# Active Project: Payment System Integration

## Goal
Integrate payment processing into existing platform

## Phases
1. **Design** (Architect) - API design, data models
2. **Infrastructure** (DevOps) - Database, caching, monitoring
3. **Implementation** (Code) - Core logic, validation, testing
4. **Integration** (Code) - Connect to existing services
5. **Debugging** (Debug) - Performance, edge cases
6. **Deployment** (DevOps) - Staging, then production

## Current Phase
Phase 3: Implementation (in Code mode)

## Decisions Made
- See `decisionLog.md` ADR-042: REST API design
- See `decisionLog.md` ADR-043: PostgreSQL schema

## Blockers
None currently
```

---

## Handoff Between Modes

### Clean Context Switching

**Before switching:**
1. Summarize what was accomplished
2. Document decisions in Memory Bank
3. State clear objective for next mode
4. Provide necessary context

Example handoff:

```markdown
## Architecture Phase Complete

**Accomplished:**
- Designed payment API (see `decisionLog.md` ADR-042)
- Created database schema
- Defined integration points

**Decisions:**
- REST API with JSON payload validation
- PostgreSQL with connection pooling
- Redis cache (5-minute TTL)

**Next: Switch to Code Mode**

**Objective**: Implement payment API per design

**Context**:
- Follow patterns from `libs/db/base.py` for database
- Use `libs/observability/` for logging/metrics
- See `memory-bank/decisionLog.md` ADR-042 for API spec
- Write integration tests (per `systemPatterns.md` testing section)

**Success Criteria**:
- API endpoints functional
- Integration tests passing
- Logged with structured logging
- Metrics exposed for Prometheus
```

---

## Progress Tracking

### Update Memory Bank Progress

Keep [`memory-bank/progress.md`](../../memory-bank/progress.md) current:

```markdown
# Project Progress

## Overall Status
60% complete - Implementation phase

## Milestones
- [x] Architecture designed (Dec 29)
- [x] Infrastructure provisioned (Dec 29)
- [ ] Core implementation (Dec 30) - IN PROGRESS
- [ ] Integration complete (Dec 31)
- [ ] Deployed to staging (Jan 2)

## Current Work
Implementing payment validation logic (Code mode)

## Risks
- Redis cache configuration needs verification
- Integration with auth service timing

## Next Steps
1. Complete validation logic
2. Add integration tests
3. Performance testing (Debug mode)
```

---

## Anti-Patterns

**Don't:**
- ❌ Switch modes without documenting context
- ❌ Make decisions without updating Memory Bank
- ❌ Lose track of progress across switches
- ❌ Forget to align with previous decisions
- ❌ Skip updating systemPatterns.md for new patterns

**Do:**
- ✓ Document thoroughly in Memory Bank
- ✓ Maintain progress tracking
- ✓ Ensure consistency across phases
- ✓ Clear handoffs between modes
- ✓ Update systemPatterns.md with patterns

---

## Orchestrator Checklist

Before completing orchestration:

- [ ] All phases completed successfully
- [ ] Memory Bank fully updated:
  - [ ] decisionLog.md has all ADRs
  - [ ] systemPatterns.md has new patterns
  - [ ] progress.md reflects completion
  - [ ] activeContext.md cleared
- [ ] All modes' work validated
- [ ] Integration tested
- [ ] Documentation complete
- [ ] No orphaned decisions or undocumented choices

---

## Related Documentation

- [`memory-bank/decisionLog.md`](../../memory-bank/decisionLog.md) - Track decisions across phases
- [`memory-bank/systemPatterns.md`](../../memory-bank/systemPatterns.md) - Patterns to follow
- [`memory-bank/progress.md`](../../memory-bank/progress.md) - Track project progress
- [`memory-bank/activeContext.md`](../../memory-bank/activeContext.md) - Current work context
