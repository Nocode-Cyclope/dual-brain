---
name: memory-lint
description: >
  Periodic review of the accumulated lessons in the Claude Code memory
  directory. Classifies every lesson (Preference / Discipline / Safety /
  Repeated-Mistake / Outdated / Reference-Fact), runs an effectiveness test
  against chronicle.md and recent output files (did the rule actually hold?),
  and proposes an escalation path per lesson (keep / sharpen / promote to
  CLAUDE.md / archive). Use when the user says "memory-lint", "lessons
  review", "check the memory files", "are rules slipping through?".
  Manually triggered. No auto-trigger.
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion
---

# Memory-Lint — Lessons Review with Escalation Path

Systematic review of the lessons in the Claude Code memory directory. Makes visible which lessons hold, which slip through, and which should be escalated into a harder rule.

> **Core principle:** lesson storage is not lesson enforcement. Capture happens immediately (one correction → one lesson file), but effect only comes from periodic checking and targeted escalation. This skill is the enforcement loop.

## Memory layout this skill works on

The standard Claude Code auto-memory layout: a project memory directory containing `MEMORY.md` as the index plus one file per lesson. Lesson files typically carry a prefix that hints at their nature — e.g. `feedback_*` for behavioral corrections, `reference_*` / `project_*` / `user_*` for facts about the world. Locate the directory via the memory path shown in the session context; do not hard-code it.

## When the skill applies

**Yes** — run the skill when the user says:
- "let's review the lessons"
- "memory-lint"
- "check the memory files"
- "are rules slipping through?"
- "lessons pass" or "escalation pass"

**No** — the skill does not apply for:
- Capturing new corrections (that happens ad hoc when the correction occurs, not through this skill)
- CLAUDE.md edits unrelated to existing lessons (use `/second-brain-upgrade`)
- Wiki health checks (use `/knowledge-lint`)

**Manually triggered, no auto-trigger.** Frequency is the user's call — on demand, not periodic.

---

## Classification Substrates

Every lesson is sorted into one of six categories. Each category has a definition + decision rule + default action.

### 1. Preference

- *Definition:* a style, formatting, or address convention with no failure risk.
- *Decision rule:* the lesson is a convention whose violation would be "not pretty" but produces no measurable damage or loss of trust.
- *Default action:* storage in the lesson file is enough. No escalation needed.
- *Examples:* a lesson fixing the date format for client documents; a lesson that a person is always addressed by their full name.

### 2. Discipline

- *Definition:* a behavioral rule whose violation measurably degrades output quality.
- *Decision rule:* the lesson arose from a repeated output correction and the associated skill does not reliably hold with it in place.
- *Default action:* storage plus escalation candidate on effectiveness-test failure.
- *Example:* a lesson that every draft must be checked against a style checklist before sending, created after the same style slip recurred.

### 3. Safety

- *Definition:* a protective rule against irreversible or trust-damaging harm.
- *Decision rule:* violation would produce data loss or reputational damage.
- *Default action:* storage plus immediate escalation candidate to a top-level rule, regardless of the effectiveness test. Safety rules deserve prominence even before they have ever been violated.
- *Example:* a lesson that destructive file operations always require explicit per-action confirmation.

### 4. Repeated-Mistake

- *Definition:* a pattern violated multiple times (≥2) despite an existing lesson.
- *Decision rule:* the effectiveness test finds at least two violation traces (in chronicle.md or output files).
- *Default action:* escalation is mandatory. Decide the promotion target case by case.
- *Example:* a formatting rule that keeps reappearing in corrections even though a lesson file for it exists.

### 5. Outdated

- *Definition:* the lesson is superseded by an architecture change, a new skill, or a context switch.
- *Decision rule:* the occasion for the lesson no longer exists or is covered by other mechanics.
- *Default action:* archive after the user confirms. Move to `archive/` inside the memory directory.
- *Example:* a lesson about a workaround for a tool that has since been replaced.

### 6. Reference/Fact

- *Definition:* a fact file rather than a behavioral lesson — records current states of the world (paths, server addresses, roles, terminology, project context). Usually recognizable by a `reference_*`, `project_*`, or `user_*` file prefix; the label in the table may follow the prefix (Reference / Project / User).
- *Decision rule:* the file describes a current state of the world, not a target state of Claude's behavior.
- *Default action:* keep plus staleness verification — check the recorded facts against reality (paths via `Glob`, addresses and terminology via `Grep`). Update or archive stale facts, never escalate them.
- *Examples:* a file recording the dev-server address for a side project; a file recording that "Sarah Chen" is the user's mentor at "Acme Corp".

**Escalation logic:**
- Preference → never escalate
- Discipline → escalate when the effectiveness test shows violation
- Safety → escalate at the first opportunity, prophylactically
- Repeated-Mistake → escalation is mandatory
- Outdated → do not escalate, archive
- Reference/Fact → never escalate; update or archive stale facts

---

## Effectiveness-Test Substrates

Sources that combine into the effectiveness picture.

### Source A — search chronicle.md

- *Method:* `Grep` on `ops/chronicle.md` for correction patterns in the last 50 entries. Extract search terms from the lesson itself (title, key terms, failure patterns from the memory file).
- *Output:* list of date + entry snippet where the pattern appeared.
- *Limitation:* only catches corrections that were explicitly documented. Silent corrections in chat do not show up.

### Source B — check recent output files

- *Method:* `Glob` on `output/**/*.md` — recursive, deliverables also live in subfolders. Check window: since the last memory-lint entry in chronicle.md, at minimum the last 30 days (by filename date or modification time). Check lesson-specific markers:
  - **For a formatting lesson:** grep for the wrong pattern vs. the required one (e.g. date-format regex).
  - **For a style lesson:** count the specific markers the lesson names (forbidden phrases, structural tics).
  - **For other lessons:** derive markers from the respective memory file (if the file defines no markers: mark the lesson as unmeasurable).
- *Output:* file + marker hits plus date.
- *Limitation:* only works for machine-checkable lessons. Discipline and Preference often are; Safety rarely is.

### Source C — the user's gut feeling

- *Method:* via `AskUserQuestion`, ask one scale question per lesson. Options: "holds" / "slips" / "unsure". With more than 4 lessons: in batches of 4 questions.
- *Output:* a user annotation per lesson.
- *Limitation:* subjective. For non-measurable lessons it is the only reliable path.

### Source D — reference check

- *Method:* per memory file, mechanically check all references: resolve `[[...]]` wikilink targets against the vault via `Glob`, check quoted CLAUDE.md passages against the current CLAUDE.md via `Grep`. For Reference/Fact files, additionally run the staleness verification from category 6 (paths, addresses, terminology).
- *Output:* list of stale references per file — dead wikilink target, CLAUDE.md passage that no longer exists, superseded fact.
- *Limitation:* only finds mechanically checkable references. Content-level staleness stays with Source C.

### Combination rule

- Source A or B with a hit → sign of violation → mark as "violated" in the table
- No source with a sign → counts as "held", unless Source C contradicts
- Source C overrides A and B when the gut feeling clearly speaks against the objective signals
- Source D with a hit → not a violation signal, but "file stale" → recommend sharpen (fix the reference) or update (Reference/Fact)

---

## Memory Frontmatter and Delta Rule

Target schema for uniform frontmatter per memory file:

```yaml
---
type: feedback | user | project | reference
escalated: <YYYY-MM-DD> → <target>       # only for escalated lessons
lint_category: <category from the last pass>
last_linted: YYYY-MM-DD
---
```

- **One-time normalization of the existing stock:** never done silently. On the first pass after introduction, the skill presents the schema plus the list of files to change for confirmation (`AskUserQuestion`); normalization happens only after an explicit OK.
- **Delta rule for follow-up passes:** only classification (step 2) and frontmatter maintenance may run on deltas — new files, files without `lint_category`, files changed since `last_linted`. The effectiveness test (step 3) **always runs over the full stock**: old lessons can start slipping again, and exactly this failure mode is what motivated the skill.

---

## Workflow

Every step has a "done when" criterion.

### Step 1 — Inventory

- *Do:* `Glob` on `*.md` in the memory directory. `Read` on `MEMORY.md` (the index).
- *Done when:* the list of all memory files plus the index mapping is on the table.

### Step 2 — Classification per lesson

- *Do:* assign one of the six categories per lesson, based on the classification substrates above. One sentence of reasoning per assignment. Respect the delta rule: already-classified files unchanged since `last_linted` keep their `lint_category` and are only confirmed, not re-derived.
- *Done when:* every memory file has a category plus reasoning.

### Step 3 — Effectiveness test per lesson (Sources A, B, and D)

- *Do:* run Source A (`Grep` on chronicle.md with lesson-specific search terms), Source B (`Glob` plus `Read` on recent output files with lesson-specific markers), and Source D (reference check). Derive markers for each lesson from its content — if no markers are definable, mark it as unmeasurable. The effectiveness test always runs over the full stock, no delta shortcut.
- *Done when:* every lesson has an A, B, and D result (or the marker "unmeasurable").

### Step 4 — Initialize the proposal table

- *Do:* fill the canonical output (format below) with all lessons, category, effectiveness-test results A and B, and a preliminary recommendation.
- *Done when:* the table stands, all columns filled except "Gut feeling" and "Decision".

### Step 5 — Collect the user's gut feeling (Source C)

- *Do:* `AskUserQuestion` with multiple choice per lesson. Max 4 lessons per call (`AskUserQuestion` limit). With more lessons: in batches.
- *Done when:* the gut-feeling column is filled for every lesson.

### Step 6 — Finalize the recommendation per lesson

- *Do:* derive the final recommendation from classification + effectiveness-test combination + gut feeling:
  - **keep** (default for Preference, held Discipline, and Reference/Fact)
  - **sharpen** — extend the lesson file with the observed slip vector, add a sharpened marker (🔧 plus date) in the MEMORY.md index, no CLAUDE.md change. Decision rule: the lesson holds at its core, but a concrete slip vector is visible that the file does not yet name.
  - **escalate** with a promotion-target recommendation (Repeated-Mistake, Safety, slipping Discipline)
  - **archive** (Outdated, stale Reference/Fact)
  - **merge** with another lesson (on thematic overlaps)
- *Done when:* table updated, final recommendation per row.

### Step 7 — Clarify the promotion target per escalation

- *Do:* for every escalation recommendation, `AskUserQuestion`: which of the three targets?
  - **Numbered rule in CLAUDE.md** — for a short hard rule (under 50 words)
  - **Top-level block in CLAUDE.md** — for a longer rule with context (50–200 words)
  - **`memory/rules/` as a third tier** — for rules with examples, how-to-apply, and history (over 200 words)
- Give a recommendation per case following the heuristic (see below). The user decides finally.
- *Done when:* a promotion target is decided per escalation.

### Step 8 — Execution

- *Do:*
  - **Kept lessons:** nothing.
  - **Sharpened lessons:** extend the lesson file via `Edit` with the slip vector, carry the sharpened marker (🔧 plus date) into the MEMORY.md index.
  - **Escalated lessons:**
    - Target numbered rule: `Edit` on CLAUDE.md, append the new rule at the end of the list
    - Target top-level block: `Edit` on CLAUDE.md, insert the new block
    - Target `memory/rules/`: `Write` a new file at `memory/rules/<slug>.md`, plus an index entry in CLAUDE.md
    - In all cases: annotate the original lesson file with "escalated to <target> on <date>", update the MEMORY.md index
    - **Self-Check hook:** on every escalation and every de-escalation (e.g. archiving an escalated rule), cross-check the per-output-type items in the CLAUDE.md `## Self-Check` section and adjust them. Format and maintenance rule live in CLAUDE.md, not here.
  - **Archived lessons:** copy the full content via `Write` to `<memory-dir>/archive/<slug>.md`, then reduce the original via `Edit` to a two-line tombstone ("Archived to archive/<slug>.md on <date>" plus a one-sentence reason). No deletion — archive instead of unlink, per the File Operations Discipline in CLAUDE.md. Explicit confirmation by the user per file remains mandatory. Update the MEMORY.md index.
  - **Merged lessons:** merge the content of the two files into one. Archive the original of the second (tombstone mechanics as above). Update the index.
  - **All reviewed lessons:** update `lint_category` and `last_linted` in the frontmatter — only after the one-time schema normalization has been confirmed (see "Memory Frontmatter and Delta Rule").
- *Done when:* all actions executed and verified via `Read`.

### Step 9 — Chronicle entry and report

- *Do:* entry in `ops/chronicle.md` in the format `## [YYYY-MM-DD] memory-lint | Lessons review pass` with the number of reviewed lessons, escalations, sharpenings, archivings, and the list of promotion targets. Insert newest-first.
- *Done when:* the entry stands. The user gets a compact report (three to five lines) with the key results.

---

## Canonical Output

The proposal table is built in full on every run and presented visibly to the user. Format:

```markdown
### Memory-Lint Pass: <YYYY-MM-DD>

| # | Lesson | Category | Test A (chronicle) | Test B (output) | Gut feeling | Recommendation | Promotion target | Decision |
|---|---|---|---|---|---|---|---|---|
| 1 | Date format for client docs | Preference | 0 hits | 0 hits | holds | keep | — | ✓ |
| 2 | Style checklist before sending | Discipline | 2 hits | 3 markers / 5 outputs | slips | escalate | numbered rule (recommendation) | ? |
| 3 | Destructive operations need confirmation | Safety | 0 hits | unmeasurable | holds | keep, observe | — | ✓ |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Summary:** N lessons reviewed · K escalation candidates · S sharpening candidates · M archive candidates · X merges
```

The table is the skill's visible mechanic. It shows the user at a glance what the skill recommends and gives them a clear decision point per row.

---

## Promotion Recommendation Heuristic

For every escalation, the skill recommends which of the three promotion targets fits best.

| Lesson characteristic | Recommended target | Reason |
|---|---|---|
| Short (under 50 words), expressible as a one-line imperative | **Numbered rule in CLAUDE.md** | maximum prominence, no context bloat |
| Medium (50–200 words), needs some context, several sub-rules | **Top-level block in CLAUDE.md** | its own section, escalation history stays visible |
| Long (over 200 words), with examples, how-to-apply, negative cases | **`memory/rules/<slug>.md`** with an index entry in CLAUDE.md | third tier, full context, still in the memory layer |

The user decides per case. The recommendation is a proposal, not a ruling.

---

## Failure Modes and Protection

| Failure mode | Protection |
|---|---|
| Skill misclassifies | classification substrates with clear decision rules; the user sees the classification in the table and can correct per row |
| Skill accidentally overwrites memory files | the original lesson file stays untouched on escalation (annotation line instead of overwrite). On merge, the original is explicitly archived, not deleted. Archiving requires explicit confirmation per file |
| Skill ignores critical lessons | the Safety category has escalation-candidate status by default, regardless of the effectiveness test |
| Gut-feeling question gets skipped | step 5 is mandatory in the workflow. Step 6 (finalize recommendation) requires step-5 data |
| Skill changes CLAUDE.md without confirmation | step 7 forces an explicit decision per escalation via `AskUserQuestion`. No `Edit` without the user's choice of promotion target |
| `memory/rules/` folder does not exist at first need | step 8 creates the folder on demand (no separate setup needed) |
| More than 4 lessons to clarify (`AskUserQuestion` limit) | steps 5 and 7 work in batches of 4 |

---

## Edge Cases

- **Memory files with unclear category** → ask the user via `AskUserQuestion`, do not guess. A classification must be justifiable.
- **Lessons without machine-checkable markers** → mark Source B as "unmeasurable". Sources A and C carry the assessment.
- **Two lessons with thematic overlap** → merge recommendation in step 6. The user decides per pair.
- **A new `memory/rules/` file is created** → add the CLAUDE.md index entry in the same action (otherwise the file stays unlinked).
- **Escalation conflict** (two lessons want the same numbered rule) → combine into one rule or create two separate rules, the user's choice.

---

## Report

After the pass, the skill delivers a compact report (three to five lines):

```
Memory-lint pass complete.
N lessons reviewed · K escalated · S sharpened · M archived · X merged.
Escalation targets: [list per case].
Chronicle entry: [date].
Smoke-test note: watch whether the escalated rules take effect on their next application.
```

---

## Stop — what this skill never does

- Never changes CLAUDE.md or creates `memory/rules/` files without the user's explicit choice of promotion target via `AskUserQuestion` (step 7).
- Never deletes memory files: archiving means a full copy into the memory `archive/` folder plus a tombstone in the original (File Operations Discipline in CLAUDE.md).
- Never archives, merges, or normalizes the frontmatter schema of the existing stock without explicit user confirmation (for archiving: per file).
- Never overwrites the original lesson file on escalation; it only gets an annotation line plus an index update.
- Never shortens the effectiveness test (step 3) to deltas; it always runs over the full stock.
- Never escalates Preference or Reference/Fact lessons; stale facts get updated or archived.

## Related Skills

- `/second-brain-upgrade` — when an escalation requires structural architecture changes (e.g. a new rule tier), use that skill as the preceding stage
- `/knowledge-lint` — analogous mechanics for wiki health, clearly separated in scope
- `/weekly-review` — may recommend `/memory-lint` as an optional sub-step when the user notices rules slipping through

## When to Lint

- On demand (default) — when the user senses lessons slipping or the memory grows too large for an intuitive overview
- After significant correction clusters — when several corrections on the same topic occur in one session
- Before larger structural upgrades — to ensure no old lessons become obsolete unnoticed
