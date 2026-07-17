---
name: heartbeat
description: >
  Weekly read-only vault heartbeat — reads the state of the vault (inbox
  backlog, lint distance and ingest threshold, overdue tasks, sweep staleness,
  weekly-review status) and writes a report to ops/context/heartbeat.md,
  including a small read-sample for the user. Reports only, changes nothing,
  never asks back. Use when the user says "heartbeat", "vault status",
  "how is the vault doing", "health pulse", or wire it to a weekly scheduled
  run. Runs manually as /heartbeat or on a schedule.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# /heartbeat — the vault reports its own state

The heartbeat is a pure reporter: discovery turned inward, persistence in one state file, scheduling via a timer. It decides nothing and repairs nothing; it makes state visible before the user has to ask.

## Scheduling

Two equivalent ways to run it:

- **Manual:** the user invokes `/heartbeat` at any time.
- **Scheduled:** wire it to a weekly scheduled run — via Claude Code scheduled tasks or the OS scheduler (cron, Task Scheduler). A typical setup is a Monday-morning run so the report is waiting when the week starts. The skill behaves identically in both cases; because scheduled runs are headless, it never asks questions.

## Procedure (exactly one pass, then stop)

1. **Read the previous run:** the topmost entry in `ops/context/heartbeat.md` (if the file exists), for delta comparisons.
2. **Collect state.** Read-only commands exclusively; every number is counted, never estimated:
   - **Inbox:** total entries in `ops/inbox/` and files older than 30 days (`ls | wc -l`, `find -maxdepth 1 -type f -mtime +30 | wc -l`).
   - **Lint:** date of the most recent `lint |` entry in `knowledge/wiki/log.md`. Careful — that file is **newest-first**: the most recent entry is the FIRST hit from the top, exactly `grep -m1 "^## \[.*\] lint" knowledge/wiki/log.md`. (A naive scan that takes the last hit reports the oldest lint as the newest — this mistake has happened.) Then: days since; count of `knowledge/wiki/sources/` files with a `created:` date after that lint date. Mark as due according to the threshold definition in `/knowledge-lint` → "When to Lint" (reference it, do not copy it).
   - **Tasks:** `grep -H -E "^(due|status):" ops/tasks/*.md`; overdue = `status: pending` or `in-progress` with a `due:` before today.
   - **Sweep:** most recent `ops-sweep` entry in `ops/chronicle.md`; older than 30 days or never run → flag it.
   - **Weekly:** does `ops/weekly/<current ISO week>.md` exist? Name the most recent weekly file that does exist.
   - **Read sample (guard against comprehension rot):** three randomly drawn files (`shuf`) from the artifacts created or changed in the last 7 days (`output/*.md` by file date plus `knowledge/wiki/{concepts,sources,synthesis,entities}/*.md` with a fresh `updated:`).
3. **Write the report:** insert a new section **newest-first** into `ops/context/heartbeat.md` (format below). On first run, create the file with frontmatter `type: context`, `captured: <date>`, `source: heartbeat`.
4. **Stop.** No second pass, no follow-up actions, no report anywhere else.

## Report Format

```markdown
## [YYYY-MM-DD] heartbeat | week NN
- Inbox: N entries (M older than 30 days) · delta vs. last run: +/-X
- Lint: last YYYY-MM-DD (N days ago), K new sources since → due / ok
- Overdue tasks: N — [[ops/tasks/...]] (name at most 5)
- Sweep: last YYYY-MM-DD → due / ok · Weekly week NN: present / missing
- Read sample: [[file1]] · [[file2]] · [[file3]] — can you explain each in one sentence?
- Unclear/notes: [anything the run could not read cleanly; "—" if nothing]
```

Due lines are reports, not actions: "lint due" means the user decides whether `/knowledge-lint` runs.

## Guardrails (unattended run)

- **Run limits:** exactly one pass per trigger; no subagents, no workflows, no retries. If a read command fails, note it under "Unclear/notes" and keep going.
- **Uncertainty default:** note instead of ask. The run never asks follow-up questions (it may be running headless) and never acts on suspicion.
- **Write radius (exhaustive):** exactly one file in the vault, `ops/context/heartbeat.md`. Nothing else is touched.

## Stop — what this skill never does

- Never writes to any file other than `ops/context/heartbeat.md`; tasks, projects, inbox, `chronicle.md`, and everything under `knowledge/` remain untouched (CLAUDE.md Rule 3).
- Never changes statuses, never cleans up, never moves or deletes; it reports candidates, and `/ops-sweep`, `/knowledge-lint`, and the user do the executing.
- Never starts subagents, workflows, or other skills — not even the ones whose dueness it reports.
- Never asks back and never guesses; anything unclear goes under "Unclear/notes".
- Never reports estimated numbers; every number in the report is counted, not plausibility-checked (CLAUDE.md Rules 11 and 15).

## Related Skills

- `/ops-sweep` — executes the grooming the heartbeat only announces
- `/knowledge-lint` — the health check whose dueness gets reported
- `/today` — interactive daily plan (different goal: planning, not state reporting)
- `/weekly-review` — weekly review; the heartbeat only reports whether it has run
