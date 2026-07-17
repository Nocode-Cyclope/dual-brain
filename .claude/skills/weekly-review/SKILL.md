---
name: weekly-review
description: >
  Weekly review at the weekend — summarizes the week, identifies promotion
  candidates for output/ and knowledge/raw/, writes ops/weekly/YYYY-WNN.md.
  Use when the user says "close out the week", "weekly review", "Sunday
  review", "how was the week", "weekend reflection", or looks back on the
  week. Not for daily reflection (see /daily-review).
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# /weekly-review — Weekly Review

Generates `ops/weekly/YYYY-WNN.md` as a summary weekly review.

## Steps

1. Determine the current calendar week (ISO 8601, e.g. `2026-W16`) and cross-check it against the date. On Monday or Tuesday, ask whether the previous week is meant (default: previous week — someone saying "close out the week" on a Monday rarely means the two-day-old current week).
2. Check for an existing `ops/weekly/YYYY-WNN.md` — if present, augment rather than overwrite.
3. Read the week's daily notes: `ls ops/daily/` and collect all `YYYY-MM-DD.md` files from this week.
4. Search `ops/chronicle.md` for entries from this week (entries are ordered newest-first — filter by date, do not rely on position).
5. Search `knowledge/wiki/log.md` for entries from this week (e.g. ingests, lints; also newest-first).
6. Scan tasks: completed (`status: complete` with `updated:` in this week) and newly created (`created:` in this week).
7. Scan the `output/` folder: what was produced this week?
8. List active projects with status changes.
9. Write or update the weekly file.

## Output Format

```markdown
---
type: weekly
week: 2026-W16
tags: []
---

# Weekly Review W16 (2026-04-13 to 2026-04-19)

## Highlights
- 2-3 central events or progress items

## Completed
- [[ops/tasks/...]] (04-15)
- ...

## Newly Captured
- [[ops/projects/...]] — brief context
- [[ops/people/...]] — first contact (e.g. Sarah Chen, Acme Corp)
- ...

## Active Projects with Movement
- [[ops/projects/...]] — what changed

## Outputs of the Week
- [[output/...]] — brief description

## Promotion Candidates
**Candidates for output/ → knowledge/raw/ promotion** (explicit user confirmation required):
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

If confirmed, follow the Promotion Workflow in CLAUDE.md (single source): copy or move the file to `knowledge/raw/`, add an entry in `ops/chronicle.md`. `knowledge/wiki/log.md` is NOT touched — its entry is created only when a later `/knowledge-ingest` actually changes wiki pages. Optionally offer `/knowledge-ingest`.

**Never promote automatically.** Always require explicit confirmation per file.

The view here is week-incremental. The triage of the entire `output/` inventory (delete / archive / promote) lives in `/ops-sweep`.

## Done when

- `ops/weekly/YYYY-WNN.md` exists with `type: weekly` and a correct `week:`; if it pre-existed, it was augmented rather than overwritten.
- The full Mon–Sun range is covered: the week's daily notes, chronicle entries, and `log.md` entries have been reviewed.
- Every template section is filled or deliberately empty ("nothing found", not "not checked").
- Every promotion candidate carries a reason why it is knowledge-worthy.
- No move to `knowledge/raw/` without explicit confirmation per file.

## Stop — what this skill never does

- Never overwrites an existing `ops/weekly/YYYY-WNN.md`; pre-existing content is augmented (Step 2).
- Never promotes automatically to `knowledge/raw/`; every move requires explicit confirmation per file (CLAUDE.md non-negotiable rules).
- Never writes to `knowledge/wiki/` (CLAUDE.md non-negotiable rules); even `knowledge/wiki/log.md` stays untouched — its entry is created only by a later `/knowledge-ingest`.
- Never deletes, archives, or moves `output/` files; the view here is week-incremental, the full triage lives in `/ops-sweep`.
- Never reports an empty template section as checked; emptiness means "nothing found", never "not checked".

## Related Skills

- `/today` — daily plan
- `/daily-review` — end-of-day review
- `/history` — activity overview
- `/ops-sweep` — full-inventory grooming (tasks, projects, inbox, output/ triage)
- `/knowledge-ingest` — trigger after promotion if desired
