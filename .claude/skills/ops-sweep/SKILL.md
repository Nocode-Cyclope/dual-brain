---
name: ops-sweep
description: >
  Inventory grooming across the Operations Layer and output/ — produces
  confirmation-gated proposal lists: pull task and project statuses onto the
  schema, classify every inbox file as done/active/ingest candidate, triage
  output/ into three columns (delete/archive/promote). Use when the user says
  "ops-sweep", "grooming", "clean up the inbox", "go through task statuses",
  "tidy up output", "what's lying around", "is the state still accurate", or
  when working memory and reality visibly drift apart. Executes nothing itself —
  moves and status changes only after explicit OK per tranche. Not for the
  week-incremental review (see /weekly-review).
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# /ops-sweep — Inventory Grooming

Reconciles working memory with the actual inventory — full inventory, not a weekly increment. The skill produces **proposal lists only**; every execution follows the File Operations Discipline in CLAUDE.md (single source for the confirmation requirement and the recovery path, not duplicated here). The full-inventory triage of `output/` lives exclusively here; `/weekly-review` only looks at the current week.

## Trigger

- **Manual:** the user invokes `/ops-sweep` (optionally with a scope argument, see below).
- **Staleness hint in /today:** if no `ops-sweep` entry exists in `ops/chronicle.md`, or the most recent one is older than 30 days, `/today` adds a hint line to the daily plan. The hint only reminds — it does not start the sweep.

## Arguments

`$ARGUMENTS` (optional): `tasks`, `projects`, `inbox`, `output` — restricts the sweep to one area. Without an argument, all four run.

## Steps

1. **Reference point:** `grep -E "^## \[.*\] ops-sweep" ops/chronicle.md` — name the most recent date (context for what has accumulated since). The sweep itself always runs over the full inventory, never just the delta.
2. **Tasks:** one pass of `grep -H -E "^(due|status):" ops/tasks/*.md` (same as /today). For every open task with a passed `due` or content that is recognizably done (cross-check against the chronicle), one proposal: **close** (complete/cancelled), **reschedule** (new due), **defer** (remove due, stays pending). Pull off-schema status values onto the task schema in CLAUDE.md (pending | in-progress | complete | cancelled) — no new status value is invented.
3. **Projects:** project list via Glob (`ops/projects/*` — top-level `.md` files and directories), then `grep -H "^status:" ops/projects/*.md ops/projects/*/README.md`. Proposals for complete / paused / archived when no artefact is still open, there is no chronicle movement, and no open tasks hang off the project. Pull off-schema values (e.g. `status: draft`) onto the project schema (active | paused | complete | archived). Cross-check: flag open tasks whose `project:` points to a completed project. List projects without status frontmatter as findings — do not guess.
4. **Inbox:** capture every file under `ops/inbox/` — including non-Markdown (docx, pptx, pdf, txt) and subfolders. Every file gets exactly one class:
   - **done** — processed or superseded → candidate for archiving (default) or deletion. Typical: `_`-prefixed extraction intermediates, raw states of already-delivered deliverables.
   - **active** — belongs to ongoing work → proposal: move into the associated project or leave in place with a note.
   - **ingest candidate** — valuable long-term → the path is `ops/` → `output/` → `knowledge/raw/` (Promotion Workflow in CLAUDE.md), never directly from the inbox into `knowledge/`.
5. **output/:** recursively across all subfolders. Three-column triage: **delete** / **archive** / **promote** (candidate — the promotion itself stays manual). One half-sentence justification per file; similar files may share one justification as a group, but every file appears in the list. Whatever deliberately stays (templates, reference states, active working states) gets an explicit **keep note** instead of silently remaining.
6. **Emit the lists and wait:** summary plus tranches in chat; for large inventories, write the full tables as a working file to `ops/context/ops-sweep-YYYY-MM-DD.md` (`type: context`) and show only totals and tranches in chat. Then ask the confirmation question per tranche following the File Operations Discipline and wait for an explicit OK. Without an OK: no moves, no status edits, no deletion. Offer the risk-free tranche first (e.g. `_` intermediates).
7. **Execute (confirmed tranches only):** moves go to `archive/<YYYY-MM-DD>-<reason>/` (existing convention), status changes via Edit on the frontmatter including the `updated:` date. Delete only when the user explicitly wants deletion instead of archiving.
8. **Chronicle:** entry `## [YYYY-MM-DD] ops-sweep | <short title>` with verified numbers (checked / proposed / confirmed / moved), newest-first under the header. The entry doubles as the timestamp for the `/today` staleness check — so write the label `ops-sweep` exactly like that. If the sweep only ran partially (single areas, rest postponed), say so in the entry.

## Output Format (proposal lists)

```markdown
# Ops Sweep 2025-07-02

Last sweep: <date | never> · Tasks: N open / M total · Projects: N active / M total · Inbox: N files · output/: N files

## Tasks — Proposals
| Task | Current | Proposal | Justification |
|---|---|---|---|
| [[ops/tasks/<slug>]] | pending, due 2025-04-20 | close (complete) | done on 04-22 per chronicle |

## Projects — Proposals
| Project | Current | Proposal | Justification |
|---|---|---|---|
| [[ops/projects/<slug>]] | active | complete | deliverable shipped, no movement since May |

## Inbox — Classification
| File | Class | Proposal | Justification |
|---|---|---|---|
| ops/inbox/_<extract>.txt | done | archive | extraction intermediate, target deliverable was shipped |
| ops/inbox/<source>.pdf | ingest candidate | via output/ into knowledge/raw/ | framework with value beyond the project |

## output/ — Triage
**Delete:** [list with justification]
**Archive:** [list with justification]
**Promote (candidates, manual):** [list with justification]
**Keep (deliberate reserve):** [list with keep note]

## Tranches
1. Risk-free (e.g. `_` intermediates): [list]
2. [next tranche]
```

Then, per tranche:

> "I would now move tranche 1 to `archive/2025-07-02-<reason>/`: [list]. OK?"

## Stop — what this skill never does

- Never executes moves, status edits, or deletions without an explicit OK per tranche; a previously agreed plan does not replace the confirmation (File Operations Discipline in CLAUDE.md).
- Never writes to `knowledge/`, not even for ingest candidates; promotion stays manual via `output/` (CLAUDE.md Rules 3 and 4).
- Never deletes by default; the standard path for confirmed tranches is `archive/<YYYY-MM-DD>-<reason>/`, deletion happens only on explicit request.
- Never invents new status values; off-schema values are pulled onto the schemas in CLAUDE.md (task: pending / in-progress / complete / cancelled, project: active / paused / complete / archived).
- Never guesses on unclear classification or missing status frontmatter; unclear cases are listed as a question or a finding (CLAUDE.md Rule 8).
- Never estimates inventory numbers; every number in the report and the chronicle entry is verified via `grep -c` or `ls | wc -l` (CLAUDE.md Rule 15).

## Related Skills

- `/weekly-review` — week-incremental review; promotion candidates of the current week
- `/today` — carries the staleness hint
- `/new` — cleanly re-file individual inbox finds
- `/knowledge-ingest` — after manual promotion into `knowledge/raw/`
