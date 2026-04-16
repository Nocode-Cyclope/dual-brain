---
name: daily-review
description: End-of-day review — compare plan vs. reality, update task status, capture observations. Part of the Operations Layer.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# /daily-review — End-of-Day Review

Compares plan vs. reality for today.

## Steps

1. Read `ops/daily/YYYY-MM-DD.md` (today) — the daily plan.
2. Extract today's activity from `ops/chronicle.md` and `knowledge/wiki/log.md`.
3. Find relevant tasks efficiently (do not read all):
   - `grep -l "due: YYYY-MM-DD" ops/tasks/*.md` for today's due items
   - Resolve task wikilinks referenced in the daily plan
4. Read only the identified task files.
5. Update task status (`status: complete` for finished items, reset `updated:`).
6. Append a review section to the daily note.
7. For important completions: add an entry in `ops/chronicle.md`.

## Appendix to Daily Note

```markdown
## Review

### Completed
- [[ops/tasks/...]] — brief note on what was finished

### Open / Deferred
- [[ops/tasks/...]] — new date or reason

### Observations
- Patterns that emerged
- Suggestions for tomorrow
- Candidates for `output/` (promotion pipeline)
```

## Chronicle Entry for Important Completions

In `ops/chronicle.md`:

```
## [YYYY-MM-DD] complete | What was completed
- Project: [[ops/projects/...]]
- Output: [[output/...]]  # if relevant
```

## Related Skills

- `/today` — generate daily plan
- `/weekly-review` — weekly review
- `/history` — query activity log
