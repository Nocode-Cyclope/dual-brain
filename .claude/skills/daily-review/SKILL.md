---
name: daily-review
description: >
  End-of-day review — compares plan vs. reality, updates task status, records
  observations in the chronicle. Use when the user says "close out the day",
  "how was today", "daily reflection", "end-of-day review", "day's done", or
  looks back on the day. Not for weekly reviews (see /weekly-review) or the
  morning daily plan (see /today).
allowed-tools: Read, Glob, Grep, Write, Edit
---

# /daily-review — End-of-Day Review

Compares plan vs. reality for today.

## Steps

1. Read `ops/daily/YYYY-MM-DD.md` (today) — the daily plan. **Fallback without a daily note** (the normal case when /today did not run in the morning): reconstruct the day from `ops/chronicle.md`, `knowledge/wiki/log.md`, and files created today, and create the note directly with the review section included.
2. Extract today's activity from `ops/chronicle.md` and `knowledge/wiki/log.md`; additionally scan files created or modified today in `output/` and `ops/` as reality evidence.
3. Find relevant tasks efficiently (do not read all):
   - `grep -l "due: YYYY-MM-DD" ops/tasks/*.md` for today's due items
   - Resolve task wikilinks referenced in the daily plan
4. Read only the identified task files.
5. Update task status (`status: complete`, reset `updated:`) — but only after a compact check-in with the user ("Completed today: X and Y — is that right?") or with clear evidence (a chronicle entry, an existing deliverable). No silent status flip.
6. Append a review section to the daily note.
7. For important completions: add an entry in `ops/chronicle.md`.

## Appendix to Daily Note

```markdown
## Review

### Completed ✅
- [[ops/tasks/...]] — brief note on what was finished

### Open / Deferred ⏳
- [[ops/tasks/...]] — new date or reason

### Observations
- Patterns that emerged
- Suggestions for tomorrow
- Candidates for `output/` (promotion pipeline)
```

## Chronicle Entry for Important Completions

Format and insertion convention (newest-first) live in the head of `ops/chronicle.md` (single source). Choose the label to match the event (complete, deliverable, decision, ...).

## Done when

- Today's daily note carries a `## Review` section (appended, or created together with the note via the fallback).
- Every status flip is covered by the user's check-in or clear evidence; changed tasks have a fresh `updated:`.
- Open or deferred tasks have a new date or a reason in the review section.
- Important completions appear as an entry in `ops/chronicle.md` (format per the chronicle head).

## Stop — what this skill never does

- Never flips a task status silently: `status: complete` only after the user's check-in or with clear evidence (a chronicle entry, an existing deliverable), as defined in Step 5.
- Never rewrites or deletes existing content of the daily note; the `## Review` section is only appended, or the note is created fresh with the review via the fallback.
- Never reads all task files; only the tasks identified via grep (`due:`) and via daily-plan wikilinks are read and touched.
- Never writes to the chronicle except for important completions, in the format per the head of `ops/chronicle.md`.
- Never writes to `knowledge/` (CLAUDE.md non-negotiable rules); `knowledge/wiki/log.md` serves only as a read source for reconstructing the day.

## Related Skills

- `/today` — generate daily plan
- `/weekly-review` — weekly review
- `/history` — query activity log
