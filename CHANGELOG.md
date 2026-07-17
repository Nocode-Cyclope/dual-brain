# Changelog

## v2.0 — 2026-07-16

The first major upgrade since the initial release. Everything here was battle-tested in a production vault for three months before being folded back into the template.

### Added

- **5 new skills** (13 → 18):
  - `/ops-sweep` — inventory grooming over the Operations Layer and `output/`. Produces confirmation-gated proposal lists (statuses, inbox triage, delete/archive/promote) instead of acting directly.
  - `/heartbeat` — weekly read-only vault health report (inbox backlog, lint distance, overdue tasks, sweep staleness) written to `ops/context/heartbeat.md`. Reports only, changes nothing.
  - `/second-brain-upgrade` — meta-skill for structural changes. Auto-triggers on structural signals and enforces the Dual-Brain base principles (two layers, asymmetric flow, explicit promotion) before any proposal is drafted.
  - `/memory-lint` — periodic review of accumulated memory lessons with a per-lesson escalation path (keep / sharpen / promote to CLAUDE.md / archive).
  - `/council` — five isolated sub-agent roles (Skeptic, Philosopher, Visionary, Operator, Outsider) research a weighty question independently, cross-critique anonymously, and a Chair renders the verdict.
- **Agents** (`.claude/agents/`, new in the template):
  - `output-evaluator` — the Generator/Evaluator split: deliverables from `/produce` and `/delegate` are certified by a cold, read-only evaluation agent instead of by their author. Default verdict "flawed until proven"; after at most two correction rounds the deliverable ships with open findings listed.
  - `council-insider` / `council-outsider` — the two research agent types behind `/council`.
- **Guardrail hooks** (`.claude/hooks/` + `.claude/settings.json`, new in the template):
  - `wiki_ask_guard.py` — asks once per session before the first write into `knowledge/wiki/` ("Do not write casually").
  - `delete_guard.py` — asks before any delete command (File Operations Discipline: explicit OK plus recovery path).
  - Both fail open: any hook error lets the tool run normally.
- **Retrieval canon** in CLAUDE.md — a single normative description of retrieval mechanics: glossary-based alias expansion, then Parallel Retrieval (Path A situational cluster entry blocks, Path B lexical grep in both languages), `index.md` demoted to fallback, overlap comparison between the two paths. Skills reference it instead of duplicating it.
- **Provenance markers** in `/knowledge-ingest` — every claim on a wiki page is tagged `[verified]`, `[claim]`, `[unsourced ⚠️]`, or `[speculation]`, backed by a four-axis source diagnosis and an external reality check. `/knowledge-lint` checks marker integrity.
- **Self-Check footer** — substantive outputs end with a visible one-line self-check (wiki consulted, facts sourced). Visibility enforces discipline; silent self-grading does not hold up.
- **File Operations Discipline** in CLAUDE.md — destructive operations require explicit per-step confirmation and a planned recovery path (`archive/` instead of unlink).
- **Rigor rules** (Non-Negotiable Rules 11–16) — never invent facts/numbers/quotes, active pushback instead of friendly confirmation, consult the wiki before substantive answers, provided material is a starting point not a boundary, verify against something external, offer unconventional ideas marked as speculative.
- New wiki infrastructure: `knowledge/wiki/skills/` (executable LLM skill definitions, `type: skill`) and `knowledge/wiki/glossary.md` (alias expansion for retrieval).

### Changed

- **All 13 original skills** upgraded with two uniform blocks: `## Stop — what this skill never does` (hard boundaries) and `## Done when` (verifiable completion criteria), plus their individual mechanics upgrades (see per-skill history in the diff).
- `/knowledge-lint` — substantially extended check catalog: canonical unprocessed-source detection via wikilink targets and `sources:` frontmatter (never literal log comparison), Dataview blocks count as index linking, newest-first date monotonicity, cluster split thresholds, provenance-marker integrity, countable thresholds, RED/YELLOW/BLUE reporting.
- `/produce` and `/delegate` — wired into the Generator/Evaluator split; output frontmatter with a canonical English `output_type` enum.
- `/setup-dual-brain` — Step-0 guard: detects an established vault and refuses to scaffold over it; scaffolds the extended wiki structure.
- Logs (`ops/chronicle.md`, `knowledge/wiki/log.md`) are now **newest-first**.
- Projects: canonical form is `ops/projects/<slug>/README.md` (directory with artefacts); flat files remain allowed for small projects.
- Concept and synthesis pages open with a core-statement blockquote directly under the H1 — a page leads with its point.

### Fixed

- `knowledge/wiki/overview.md` was referenced by CLAUDE.md but never shipped or scaffolded. It now exists in the template and in the setup wizard.
- `.claude/agents/` was described as created-on-first-use; it now ships with the template (it carries the evaluator and council agents).

## v1.0 — 2026-04-16

Initial release: two-layer vault (Operations + Knowledge), 13 skills, Continuous Routing, explicit promotion path, context farmers.
