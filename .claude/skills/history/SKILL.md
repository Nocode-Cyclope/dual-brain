---
name: history
description: Shows recent vault activity from ops/chronicle.md and knowledge/wiki/log.md in a readable format. A substitute for git log without git versioning.
allowed-tools: Read, Grep, Bash
---

# /history — Activity Log

Shows the latest activities in the vault. Reads `ops/chronicle.md` (operational events) and `knowledge/wiki/log.md` (knowledge operations).

## Arguments

`$ARGUMENTS` (optional):
- `7d` (default) — last 7 days
- `1d` — today
- `30d` — last 30 days
- `<YYYY-MM-DD>` — from a specific date
- `ops` — only `ops/chronicle.md`
- `knowledge` — only `knowledge/wiki/log.md`

## Steps

1. Derive timeframe from `$ARGUMENTS` (default 7 days).
2. **Read both logs in parallel:**
   - `ops/chronicle.md`
   - `knowledge/wiki/log.md`
3. Filter entries by date. Entry format: `## [YYYY-MM-DD] <operation> | <title>`.
4. Sort chronologically descending per day.
5. Summarize activities thematically (capture, completion, ingest, lint, migration, etc.).
6. Output the report.

## Output Format

```markdown
# Activity — last 7 days (2026-04-09 to 2026-04-15)

## 2026-04-15
**Operations:**
- complete: Sales playbook v2 finalized ([[ops/projects/sales-playbook]])
- capture: 3 new tasks for product launch

**Knowledge:**
- update: FAQ output v3 — deduplicated question 6
- ingest: Q3 planning meeting 2026-04-15 (8 new wiki pages)

## 2026-04-14
...

## Summary
- Operations events: N
- Knowledge events: N
- Most active days: ...
```

## Conventions

- Keep wikilinks in the report — the user can click directly
- If the timeframe is empty: briefly communicate, do not fabricate
- Make no statements about activity that is not in the log

## Related Skills

- `/today` — today's plan
- `/weekly-review` — weekly review
