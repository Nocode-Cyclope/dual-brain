---
name: today
description: Generates a daily plan from due tasks, active projects, and recent chronicle entries. Part of the Operations Layer.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# /today — Daily Planning

Generates the daily plan from vault contents.

## Steps

1. Check whether `ops/daily/YYYY-MM-DD.md` (today's date) already exists — if so, read it first.
2. **Find tasks via Grep** (never glob all tasks):
   - `grep -l "due: YYYY-MM-DD" ops/tasks/*.md` (today's date) -> due today
   - Dates before today -> overdue
   - If nothing due: dates through end of week -> this week
   - If still nothing: find the next due date
3. Read only the found task files.
4. `grep -l "status: active" ops/projects/*.md` -> read active projects.
5. **Create knowledge briefing** (cross-layer step, see "Knowledge Briefing" section below).
6. Extract recent activity from `ops/chronicle.md` and `knowledge/wiki/log.md` (today's date).
7. Create or update `ops/daily/YYYY-MM-DD.md`.

## Task Discovery (Grep-first)

All tasks have `due: YYYY-MM-DD` in frontmatter. Efficient discovery:

```bash
# Today's tasks (insert today's date)
grep -l "due: 2026-04-15" ops/tasks/*.md

# Overdue: individual dates or range pattern
grep -l "due: 2026-04-1[0-4]" ops/tasks/*.md  # days 10-14

# This week
grep -l "due: 2026-04-1[5-9]\|due: 2026-04-20" ops/tasks/*.md
```

Only read files that Grep returns. Never global glob+read on all tasks.

## Update Behavior

If the daily file already exists:
- Leave `[x]` completed items unchanged
- Keep manually added items (not from vault)
- Add new tasks from vault that are not yet present
- Repopulate the recent-activity section with current state
- Preserve custom sections added by the user

## Knowledge Briefing

For each active project and each task due today:

1. **Check the `knowledge:` frontmatter field** of the file — if present, carry those wikilinks 1:1 into the briefing.
2. **If no `knowledge:` field**: derive topics from the file body and tags, search `knowledge/wiki/index.md` for matching pages (max 2-3 per project).
3. **Check involved people** — if `[[ops/people/<slug>]]` is referenced, check whether `knowledge/wiki/entities/<slug>.md` exists.

Keep the briefing compact: max 3-5 wiki references per project, brief justification in half a sentence.

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

## Notes
```

If zero knowledge matches: omit the section entirely instead of leaving it empty.

## Related Skills

- `/daily-review` — end-of-day review
- `/weekly-review` — weekly review
- `/new` — capture new items
