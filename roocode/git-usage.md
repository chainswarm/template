# Git Usage Guide for AI Agents

**Last Updated:** 2025-12-29
**Purpose:** Define git workflows and practices for AI agents working with code

---

## Core Philosophy

**Git history is the story of your codebase.** Before making changes, read the story to understand where you are and where you're going.

---

## Rule: Check Last 3 Commits

**ALWAYS check the last 3 commits before making changes.**

### Quick Commands

```bash
# Quick overview
git log -3 --oneline --decorate

# With file changes
git log -3 --stat

# With full diff
git log -3 -p
```

### Example Output Analysis

```bash
$ git log -3 --oneline
a1b2c3d (HEAD -> main) Fix: Prevent decimal precision loss in transfers
e4f5g6h Refactor: Extract transfer validation to separate function
i7j8k9l Feature: Add support for ClickHouse transfers repository
```

**What this tells you:**
- Most recent work involved decimal precision (don't reintroduce bugs)
- Validation logic was recently refactored (use the new pattern)
- ClickHouse repository is newly added (it's the current pattern)

---

## Understanding Code Evolution

### See What Changed Recently

```bash
# Last 3 commits with file changes
git log -3 --stat

# Last 3 commits with full diff
git log -3 -p

# Changes to specific file
git log -3 --oneline -- path/to/file.py

# Changes in specific directory
git log -3 --oneline -- src/analyzers/
```

### Example: Understanding Intent

```bash
# See full context of a change
git show HEAD~1

# Output shows:
commit e4f5g6h
Author: Developer <dev@example.com>
Date:   Mon Dec 28 14:30:00 2025

    Refactor: Extract transfer validation to separate function
    
    Moved validation logic out of repository to improve testability.
    Validation now happens before database operations.

diff --git a/src/repository.py b/src/repository.py
-    def insert_transfer(self, transfer):
-        if not transfer.id:
-            raise ValueError("Transfer ID required")
+    def insert_transfer(self, validated_transfer):
```

**What you learn:**
- Validation moved out of repository layer (architectural decision)
- Database now expects pre-validated data
- Your new code should follow this pattern

---

## Context from History

### Check Recent Activity in Module

Before modifying a module, see its recent history:

```bash
# Recent commits touching this module
git log -5 --oneline -- src/analyzers/pattern_detector.py

# Who changed it and when
git log -5 --format="%h %an %ar: %s" -- src/analyzers/pattern_detector.py
```

### Understand Related Changes

```bash
# See commits that touched multiple related files
git log -3 --oneline -- src/analyzers/ src/storage/

# Find when a function was added
git log --all -S "detect_layering_pattern" --oneline

# Find commits mentioning a topic
git log -10 --grep="layering" --oneline
```

---

## Before Making Changes

### Pre-Change Checklist

```bash
# 1. Check recent commits
git log -3 --oneline

# 2. Check current branch
git branch --show-current

# 3. Check file status
git status

# 4. See uncommitted changes
git diff

# 5. Check for conflicts with recent changes
git log -5 --stat -- path/to/files/youre/modifying/
```

### Understand the Trajectory

```bash
# See the progression of a feature
git log --oneline --grep="pattern detection"

# See recent refactorings
git log -10 --oneline --grep="refactor" --grep="extract" --grep="move"

# Identify recent bug fixes
git log -10 --oneline --grep="fix" --grep="bug"
```

**Why this matters:**
- Avoid reverting recent bug fixes
- Follow established refactoring patterns
- Understand the direction of the codebase
- See what problems were recently solved

---

## Commit Message Guidelines

### Format

```
Type: Short description (50 chars max)

Longer explanation if needed (72 chars per line max):
- Why this change was made
- What problem it solves
- Any important context

Refs: #issue-number (if applicable)
```

### Types

- `Feature:` New functionality
- `Fix:` Bug fix
- `Refactor:` Code restructuring without behavior change
- `Docs:` Documentation changes
- `Test:` Test additions or modifications
- `Chore:` Maintenance tasks

### Examples

**Good commit messages:**

```
Fix: Prevent decimal precision loss in transfer amounts

ClickHouse was truncating decimal values to 2 places.
Changed column type from Decimal(18,2) to Decimal(38,18)
to preserve full precision.

Refs: #123
```

```
Feature: Add cycle detection to pattern analyzers

Implements Floyd's cycle detection algorithm for finding
circular patterns in transfer graphs. Used for detecting
wash trading and round-tripping schemes.

- Handles graphs up to 10,000 nodes
- Time complexity: O(n)
- Space complexity: O(1)
```

```
Refactor: Extract validation logic from repository layer

Moved validation to service layer for better separation
of concerns and testability. Repositories now expect
pre-validated data.

- Created TransferValidator class
- Updated all repository callers
- Added validation tests
```

**Bad commit messages:**

```
# ❌ Too vague
Fix bug

# ❌ What, not why
Changed decimal precision

# ❌ Multiple unrelated changes
Fix bug, add feature, refactor code, update docs
```

---

## Working with Branches

### Before Creating a Branch

```bash
# Make sure you're up to date
git fetch origin
git status

# Check current branch
git branch --show-current

# See all branches
git branch -a
```

### Branch Naming

```
{type}/{short-description}
```

**Examples:**
- `feature/cycle-detection`
- `fix/decimal-precision-loss`
- `refactor/extract-validation`
- `docs/update-testing-guide`

### Creating and Switching

```bash
# Create and switch to new branch
git checkout -b feature/new-pattern-detector

# Switch back to main
git checkout main

# Delete local branch
git branch -d feature/old-branch
```

---

## Useful Git Patterns for Agents

### 1. Check if File Was Recently Modified

```bash
# Was this file changed in last 3 commits?
git log -3 --oneline -- src/analyzer.py

# If output is empty, file wasn't touched recently
# If output exists, read those commits before modifying
```

### 2. Find When a Bug Was Introduced

```bash
# Search for when a function was added/changed
git log --all -S "problematic_function" --oneline

# See the full change
git show <commit-hash>
```

### 3. See What's Different from Main

```bash
# What changed in your branch vs main
git diff main..HEAD

# Just the file names
git diff --name-only main..HEAD

# Statistics
git diff --stat main..HEAD
```

### 4. Understand a Complex Change

```bash
# Show individual file changes
git show HEAD -- src/specific_file.py

# Show change with more context lines
git show HEAD --unified=10
```

### 5. Find Related Changes

```bash
# All commits touching a directory
git log --oneline -- src/analyzers/

# All commits by keyword
git log --grep="validation" --oneline

# All commits in date range
git log --since="2 weeks ago" --oneline
```

---

## Common Workflows

### Starting New Work

```bash
# 1. Update main branch
git checkout main
git pull origin main

# 2. Check recent changes
git log -3 --stat

# 3. Create feature branch
git checkout -b feature/my-feature

# 4. Make changes
# ... edit files ...

# 5. Review changes
git diff

# 6. Stage changes
git add src/

# 7. Commit
git commit -m "Feature: Add new pattern detector"
```

### Understanding Existing Code

```bash
# 1. Who last modified this file?
git log -1 --oneline -- src/analyzer.py

# 2. What was changed?
git show HEAD -- src/analyzer.py

# 3. Why was it changed?
git log -1 --format="%B" -- src/analyzer.py

# 4. When was this function added?
git log -S "def detect_pattern" --oneline -- src/analyzer.py
```

### Before Modifying Code

```bash
# 1. Check recent commits in this area
git log -5 --oneline -- src/analyzers/

# 2. See what changed
git log -3 --stat -- src/analyzers/

# 3. Understand why
git log -3 -p -- src/analyzers/

# 4. Now make your changes with context
```

---

## Advanced Patterns

### Search Commit Messages

```bash
# Find commits mentioning specific topics
git log --grep="performance" --oneline
git log --grep="refactor" --grep="validation" --oneline --all-match

# Case-insensitive search
git log --grep="bug" -i --oneline
```

### Search Code Changes

```bash
# Find when string was added/removed
git log -S "search_string" --oneline

# Find when regex pattern was added/removed  
git log -G "pattern.*regex" --oneline

# Show the actual changes
git log -S "search_string" -p
```

### Blame (Understand Line Origins)

```bash
# See who last modified each line
git blame src/analyzer.py

# Blame specific line range
git blame -L 10,20 src/analyzer.py

# Show commit details
git blame -L 10,20 -s src/analyzer.py
```

---

## Anti-Patterns

### ❌ Don't

**Ignore recent history:**
```bash
# ❌ Bad - making changes without context
vim src/analyzer.py
git commit -am "Update analyzer"
```

**Make massive unfocused commits:**
```bash
# ❌ Bad - committing everything at once
git add .
git commit -m "Various changes"
```

**Write vague commit messages:**
```bash
# ❌ Bad
git commit -m "Fix"
git commit -m "Update"
git commit -m "Changes"
```

### ✓ Do

**Understand context first:**
```bash
# ✓ Good - understand before changing
git log -3 --stat -- src/analyzer.py
git show HEAD -- src/analyzer.py
# Now make informed changes
```

**Make focused commits:**
```bash
# ✓ Good - one logical change per commit
git add src/analyzer.py
git commit -m "Refactor: Extract validation to separate method"

git add tests/test_analyzer.py  
git commit -m "Test: Add validation tests"
```

**Write descriptive commit messages:**
```bash
# ✓ Good
git commit -m "Fix: Prevent null pointer in pattern detection

Pattern detector crashed when analyzing empty transfer list.
Added null check and early return with empty result.

Fixes: #456"
```

---

## Troubleshooting

### Merge Conflicts

```bash
# See what conflicts exist
git status

# Abort merge if needed
git merge --abort

# After resolving conflicts
git add resolved_file.py
git commit
```

### Undo Changes

```bash
# Undo uncommitted changes to file
git checkout -- src/analyzer.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - BE CAREFUL
git reset --hard HEAD~1

# Undo specific commit
git revert <commit-hash>
```

### Check Remote State

```bash
# See remote branches
git branch -r

# See what's on remote vs local
git fetch origin
git log HEAD..origin/main --oneline

# See remote changes
git log origin/main -3 --oneline
```

---

## Best Practices for AI Agents

1. **Always check last 3 commits** before making changes
2. **Understand the why** from commit messages
3. **Follow established patterns** you see in recent commits
4. **Don't revert recent bug fixes** unknowingly
5. **Write descriptive commit messages** for the next agent
6. **Check file-specific history** before modifying critical files
7. **Look for recent refactorings** to follow new patterns
8. **Search for related changes** when working on a feature

---

## Quick Reference

```bash
# Most useful commands for agents
git log -3 --oneline              # Quick overview
git log -3 --stat                 # With file changes
git log -3 -p                     # With full diff
git show HEAD                     # Last commit details
git diff                          # Uncommitted changes
git status                        # Current state
git log --grep="keyword"          # Search commits
git log -S "string"               # Search code changes
git blame file.py                 # Line-by-line history
```

---

## Related Documentation

- [`rules.md`](rules.md) - Rule #3: Git Awareness
- [`coding-standards.md`](coding-standards.md) - Code quality standards
- [`automode.md`](automode.md) - Execution patterns
