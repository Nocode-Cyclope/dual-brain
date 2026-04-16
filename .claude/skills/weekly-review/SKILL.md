---
name: weekly-review
description: Weekly review — summarizes the week, identifies promotion candidates for output/ and potentially knowledge/raw/. Part of the Operations Layer.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# /weekly-review — Weekly Review

Generates `ops/weekly/YYYY-WNN.md` as a summary weekly review.

## Steps

1. Determine the current calendar week (ISO 8601, e.g. `2026-W16`).
2. Check for existing `ops/weekly/YYYY-WNN.md` — if present, augment rather than overwrite.
3. Read daily notes for the week: `ls ops/daily/` and collect all `YYYY-MM-DD.md` files from this week.
4. Search `ops/chronicle.md` for entries from this week.
5. Search `knowledge/wiki/log.md` for entries from this week (e.g., ingests, lints).
6. Scan tasks: completed (`status: complete` with `updated:` in this week) and newly created (`created:` in this week).
7. Scan `output/` folder: what was produced this week?
8. List active projects with status changes.
9. Write or update the weekly file.

## Output Format

```markdown
---
type: weekly
week: 2026-W16
tags: []
---

# Weekly Review CW 16 (2026-04-13 to 2026-04-19)

## Highlights
- 2-3 central events or progress items

## Completed
- [[ops/tasks/...]] (MM/DD)
- ...

## Newly Captured
- [[ops/projects/...]] — brief context
- [[ops/people/...]] — first contact
- ...

## Active Projects with Movement
- [[ops/projects/...]] — what changed

## Outputs of the Week
- [[output/...]] — brief description

## Promotion Candidates
**Candidates for output/ -> knowledge/raw/ promotion** (explicit user confirmation required):
- [[output/...]] — reason why it is knowledge-worthy

## Knowledge Activity
- Ingests this week from `knowledge/wiki/log.md`
- Lint results if available

## Observations / Lessons
- Patterns, friction, what did not work
- Suggestions for next week
```

## Triggering the Promotion Workflow

After creating the review:

> "I see N candidates for promotion to `knowledge/raw/`. Should I start the promotion workflow for any of them?"

If confirmed:
1. Copy or move the file to `knowledge/raw/`.
2. Add entry in `ops/chronicle.md` and `knowledge/wiki/log.md`.
3. Optionally offer `/knowledge-ingest`.

**Never promote automatically.** Always require explicit confirmation per file.

## Related Skills

- `/today` — daily plan
- `/daily-review` — end-of-day review
- `/history` — activity overview
- `/knowledge-ingest` — trigger after promotion if desired
