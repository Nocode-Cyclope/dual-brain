---
name: history
description: >
  Shows recent vault activity from ops/chronicle.md (operational events)
  and knowledge/wiki/log.md (knowledge operations) in a readable format —
  the curated audit trail. Where the vault is git-versioned, git log serves
  as a second verification path. Use when the user says "what did I do
  yesterday", "recent vault activity", "what happened this week in the
  vault", "activity log", "vault log", or wants an audit trail of vault
  operations.
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
2. **Grep-first, never a full-text read** (both logs grow large over time; a full-text read returns wrong "latest activity" once read limits truncate the file):
   - `grep -n "^## \[" ops/chronicle.md` and `grep -n "^## \[" knowledge/wiki/log.md` — all entry headers with line numbers.
   - Filter the headers to the timeframe; load only the affected ranges via Read with offset/limit.
3. Entry format: `## [YYYY-MM-DD] <operation> | <title>`. Both logs are declared newest-first (see the file heads) — still, never rely on the ordering; always filter by date.
4. Sort chronologically descending per day.
5. Summarize activities thematically (capture, completion, ingest, lint, migration, etc.).
6. **Verify counts:** check every event count in the report against `grep -c`, do not estimate.
7. Output the report. If you suspect gaps in `knowledge/wiki/log.md` and the vault is git-versioned, use `git log -- knowledge/wiki/` as a second verification path.

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

## Done when

- The timeframe matches `$ARGUMENTS` (default 7 days) and is stated explicitly in the report.
- No full-text read of the logs ran — only the header grep plus targeted offset/limit reads.
- All event counts in the report are verified via `grep -c`, not estimated.
- The report contains only activity evidenced in the logs (or `git log` as the second path); an empty timeframe is reported as empty.

## Related Skills

- `/today` — today's plan
- `/weekly-review` — weekly review
