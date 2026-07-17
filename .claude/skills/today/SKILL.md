---
name: today
description: >
  Generates the daily plan from due tasks, active projects, and recent chronicle
  entries — including a knowledge briefing on the wiki pages relevant today. Use
  when the user starts their day or says "what's on today", "daily plan", "start
  the day", "my day", "what should I begin with". Not for the end-of-day review
  (see /daily-review).
allowed-tools: Read, Glob, Grep, Write, Edit
---

# /today — Daily Planning

Generates the daily plan from vault contents.

## Steps

1. Check whether `ops/daily/YYYY-MM-DD.md` (today's date) already exists — if so, read it first.
2. **Find tasks via one-pass grep** (never glob all tasks):
   - One run: `grep -H -E "^(due|status):" ops/tasks/*.md` — returns due date and status per task.
   - The model does the date comparison, not the pattern: due < today → overdue, due = today → due today, due through Sunday → this week; otherwise name the next due date.
   - Only `status: pending` and `status: in-progress` count; complete/cancelled are dropped.
   - No date character-class patterns (`due: 2026-04-1[0-4]` and the like) — they break at month and year boundaries.
3. Read only the found task files.
4. `grep -l "status: active" ops/projects/*.md` → read active projects.
5. **Create the knowledge briefing** (cross-layer step, see the "Knowledge Briefing" section below).
6. Extract recent activity from `ops/chronicle.md` and `knowledge/wiki/log.md` (today's date).
   - **Check sweep staleness:** `grep -E "^## \[.*\] ops-sweep" ops/chronicle.md` — determine the most recent date among the hits (filter by date, do not rely on ordering). If no entry exists or the most recent one is older than 30 days: add a notice line to the daily plan (see Output Format). Notice only — never auto-start `/ops-sweep`.
7. Read the most recent existing daily note as the format template (the user's lived structure beats the template; the template below is only the cold-start skeleton), then create or update `ops/daily/YYYY-MM-DD.md`.

## Task Discovery (Grep-first, one pass)

All tasks carry `due: YYYY-MM-DD` and `status:` in frontmatter:

```bash
grep -H -E "^(due|status):" ops/tasks/*.md
```

A single run over all tasks; the model does the date comparison and status filtering, not the pattern. Then read only the relevant files.

## Update Behavior

If the daily file already exists:
- Leave `[x]` completed items unchanged
- Keep manually added items (not from the vault)
- Add new tasks from the vault that are not yet present
- Repopulate the recent-activity section with the current state
- Preserve custom sections added by the user

## Knowledge Briefing

For each active project and each task due today:

1. **Check the `knowledge:` frontmatter field** of the file — if present, carry those wikilinks 1:1 into the briefing.
2. **If no `knowledge:` field**: derive topics from the file body and tags and search per CLAUDE.md → "Retrieval Order" (Parallel Retrieval: glossary expansion, cluster entry blocks, grep across all wiki folders, including `skills/`). Max 3 hits per project.
3. **Check involved people** — if `[[ops/people/<slug>]]` is referenced, check whether `knowledge/wiki/entities/<slug>.md` exists.

Keep the briefing compact: max 3 wiki references per project, brief justification in half a sentence.

## Output Format

```markdown
---
type: daily
date: 2026-04-15
tags: []
---

# Daily Plan 2026-04-15

## Due Today
- [ ] [[ops/tasks/task-slug]] — brief description

## Overdue
- [ ] [[ops/tasks/task-slug]] — X days overdue

## Active Projects
- [[ops/projects/project-slug]] (next: next action from file)

## Knowledge Briefing
**[[ops/projects/project-slug]]:**
- [[knowledge/wiki/entities/<person>]] — stakeholder background
- [[knowledge/wiki/concepts/<concept>]] — methodological framework
- [[knowledge/wiki/sources/<source>]] — relevant prior work

**[[ops/projects/second-project]]:**
- ...

## Recent Activity
- From chronicle.md / log.md for today
- Last /ops-sweep: <date or "never"> → inventory sweep due (line only if the entry is missing or older than 30 days)

## Notes
```

If zero knowledge matches: omit the section entirely instead of leaving it empty.

## Done when

- `ops/daily/YYYY-MM-DD.md` exists with `type: daily` frontmatter and today's `date:`.
- Every task with `status: pending` or `in-progress` and `due:` up to today appears under "Due Today" or "Overdue" — cross-checked against the grep output from Step 2.
- No task with `status: complete` or `cancelled` is listed.
- If the daily note already existed: `[x]` items, manual items, and custom sections are unchanged.
- The knowledge briefing has max 3 wiki references per project with a half-sentence justification; with zero hits the section is absent entirely.

## Stop — what this skill never does

- Never writes to any file other than `ops/daily/YYYY-MM-DD.md`. Tasks, projects, `chronicle.md`, and everything under `knowledge/` stay untouched (CLAUDE.md non-negotiable rules).
- Never sets or changes the `knowledge:` frontmatter field in tasks or projects; /today only reads it (CLAUDE.md, Knowledge Bridge).
- Never overwrites or deletes `[x]` items, manually added items, or custom sections in an existing daily note (see Update Behavior).
- Never loads all tasks via glob+read and never builds date character-class patterns; task discovery runs exclusively through the one-pass grep from Step 2.
- Never auto-starts `/ops-sweep`; on sweep staleness, only the notice line appears in the daily plan.

## Related Skills

- `/daily-review` — end-of-day review
- `/weekly-review` — weekly review
- `/new` — capture new items
