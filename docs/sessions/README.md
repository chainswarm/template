# Session Documentation Guide

This directory contains logs of all AI agent conversations and development sessions.

## 📋 Purpose

Session documentation helps:
- Track development decisions and reasoning
- Maintain a history of AI-assisted work
- Share knowledge with team members
- Review past solutions and approaches
- Audit AI collaboration patterns

## 📁 Folder Organization

Sessions are organized by date using the `YYYYMMDD` format:

```
sessions/
├── 20251229/          # December 29, 2025
│   ├── session-01.md
│   └── api-design.md
├── 20251230/          # December 30, 2025
│   └── bugfix-auth.md
└── 20260102/          # January 2, 2026
    ├── session-01.md
    └── refactoring.md
```

## 📝 Naming Conventions

### Date Folders
- **Format**: `YYYYMMDD`
- **Examples**:
  - `20251229` - December 29, 2025
  - `20260115` - January 15, 2026
  - `20260301` - March 1, 2026

### Session Files
Two approaches for naming session files:

1. **Sequential numbering**: `session-{number}.md`
   - `session-01.md` - First session of the day
   - `session-02.md` - Second session of the day
   - Use when you have multiple general sessions

2. **Topic-based**: `{topic-name}.md`
   - `api-refactoring.md`
   - `database-migration.md`
   - `bug-fix-authentication.md`
   - Use when the session has a specific focus

## 📄 Session File Template

Use this template for documenting your sessions:

```markdown
# Session: [Topic/Title]

**Date**: YYYY-MM-DD
**Time**: HH:MM (Timezone)
**Agent**: roocode / GPT-4 / Claude / etc.
**Duration**: ~X minutes/hours

## 🎯 Context

Brief description of what you're trying to accomplish in this session.

### Prerequisites
- Any setup or prior work needed
- Related issues or previous sessions

## 💬 Conversation Summary

### Key Discussion Points
1. First major topic discussed
2. Second major topic discussed
3. Third major topic discussed

### Decisions Made
- **Decision 1**: Why it was chosen
- **Decision 2**: Rationale and alternatives considered
- **Decision 3**: Implementation approach

## 🔧 Actions Taken

- [ ] Action item 1 - Description
- [ ] Action item 2 - Description
- [ ] Action item 3 - Description

### Code Changes
- `path/to/file1.js` - What was changed and why
- `path/to/file2.py` - What was changed and why

### Files Created
- `path/to/new/file.md` - Purpose
- `path/to/another/file.ts` - Purpose

## 📊 Outcomes

### Successes
✅ What worked well

### Challenges
⚠️ Issues encountered and how they were resolved

### Learnings
💡 Key insights or lessons learned

## 🔄 Next Steps

- [ ] Follow-up task 1
- [ ] Follow-up task 2
- [ ] Future considerations

## 🔗 References

- Links to related documentation
- GitHub issues or PRs
- External resources consulted
- Related session files

## 📎 Attachments

- Screenshots (if any): `./screenshots/`
- Code snippets (if separate files)
- Diagrams or flowcharts

---

**Session Status**: ✅ Completed / ⏸️ Paused / 🔄 Ongoing
```

## 💡 Best Practices

### Do's ✅
- **Create folders daily**: Make a new `YYYYMMDD` folder for each day you work
- **Document as you go**: Write session logs during or immediately after the conversation
- **Be specific**: Include concrete details about decisions and outcomes
- **Link related sessions**: Reference previous sessions when relevant
- **Include context**: Future you (or team members) should understand why decisions were made

### Don'ts ❌
- **Don't skip documentation**: Even quick sessions should be logged
- **Don't use vague titles**: "session-misc" is less helpful than "api-authentication-setup"
- **Don't forget outcomes**: Always note what was accomplished or learned
- **Don't omit failed approaches**: Document what didn't work - it's valuable knowledge

## 🔍 Example Sessions

### Example 1: Initial Project Setup
**File**: `20251229/session-01.md`

```markdown
# Session: Initial Project Setup

**Date**: 2025-12-29
**Time**: 10:00 (UTC+1)
**Agent**: roocode

## Context
Setting up the initial GitHub template structure for AI coding projects.

## Actions Taken
- Created directory structure
- Wrote roocode rules documentation
- Set up README and .gitignore

## Outcomes
✅ Template structure is complete and ready to use

## Next Steps
- [ ] Test template with a sample project
- [ ] Add language-specific examples
```

### Example 2: Feature Development
**File**: `20260115/user-authentication.md`

```markdown
# Session: User Authentication Implementation

**Date**: 2026-01-15
**Time**: 14:30 (UTC+1)
**Agent**: roocode

## Context
Implementing OAuth2 authentication for the API.

## Decisions Made
- **OAuth Provider**: Chose Auth0 over custom solution for faster implementation
- **Token Storage**: Using httpOnly cookies instead of localStorage for security

## Code Changes
- `src/auth/oauth.ts` - OAuth2 flow implementation
- `src/middleware/auth.ts` - Authentication middleware
- `tests/auth.test.ts` - Unit tests for auth flow

## Outcomes
✅ OAuth2 flow working
⚠️ Need to add refresh token rotation

## Next Steps
- [ ] Implement refresh token rotation
- [ ] Add rate limiting
- [ ] Write integration tests
```

## 🤝 Team Collaboration

When working in teams:
- **Review others' sessions**: Learn from team discussions
- **Reference relevant sessions**: Link to related work
- **Consistent formatting**: Follow the template for easier reading
- **Clear handoffs**: Document status and next steps for other team members

## 📚 Additional Resources

- See [`roocode/rules.md`](../../roocode/rules.md) for full documentation requirements
- Check the [main README](../../README.md) for project overview

---

**Happy documenting! 📝**
