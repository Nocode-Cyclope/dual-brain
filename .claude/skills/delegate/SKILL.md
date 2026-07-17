---
name: delegate
description: >
  Delegates a scoped research, writing, or analysis task to an autonomous
  sub-agent. Uses an ops anchor plus curated knowledge pages as context,
  writes the result to output/. Use when the user says "have a sub-agent do
  this", "delegate this", "send an agent off", "let someone else take this",
  or when a scoped task should run autonomously instead of being worked
  through in the main dialog. Not for simple capture tasks (see /new) or
  the morning daily plan (see /today).
allowed-tools: Read, Glob, Grep, Agent, Edit, AskUserQuestion
---

# /delegate — Delegate a Task

Has a sub-agent work through a scoped task autonomously.

## When to Use

- Research tasks that need depth (e.g., "compare the three leading static site generators for the docs relaunch")
- Longer writing tasks without strict knowledge dependency
- Analyses spanning many files
- Tasks that justify sub-agent isolation (context protection)

**Do not use for:**
- Simple classification or capture (`/new` is sufficient)
- Wiki ingest (`/knowledge-ingest` is sufficient)
- **Concept/content creation with active knowledge retrieval** → `/produce` is better suited (dedicated workflow for Methodological + Specific)

## Steps

1. **Understand the task** — clarify context, goal, success criterion. If unclear, use `AskUserQuestion`.
2. **Capture the vault root** — determine the current absolute vault path. Provide all paths as absolute to the sub-agent.
3. **Identify context files** — what does the sub-agent need to read?
   - Relevant `ops/projects/`, `ops/tasks/`, `ops/people/`, `ops/context/` files, named via wikilink
4. **Knowledge discovery (always run, lightweight):**
   - Extract terms from task wording, project tags, and involved people; expand them via `knowledge/wiki/glossary.md` with primary-language/English aliases
   - Retrieval per CLAUDE.md → "Retrieval Order" (light form): match the cluster entry blocks plus `Grep` over `knowledge/wiki/{concepts,entities,skills,sources,synthesis}/` — do not read `index.md` (navigation catalog, fallback only)
   - Include 2-6 relevant wiki pages as absolute paths in the sub-agent prompt
   - If nothing relevant is found: honestly note it in the prompt ("no relevant knowledge pages on this topic in the wiki")
   - If the need is extensive (>6 pages, or methodological and specific sources need clean separation): recommend `/produce` instead of continuing here
5. **Set the output path** — `output/YYYY-MM-DD-<slug>.md`
6. **Compose the prompt** for the sub-agent (see template below)
7. **Start the sub-agent** with the `Agent` tool, subagent type depending on task: `general-purpose` for research/writing, `Explore` for pure vault exploration
8. **Review the result** and report to the user — what was produced, where it is

## Sub-Agent Prompt Template

```
Goal: <concrete task in 1-2 sentences>

Context from Operations Layer:
- Vault root: <absolute-vault-path>/
- Project: <absolute-vault-path>/ops/projects/<project>.md
- Stakeholders: <absolute-vault-path>/ops/people/<person>.md
- Daily plan reference: <absolute-vault-path>/ops/daily/<date>.md (if available)

Context from Knowledge Layer (researched beforehand via Parallel Retrieval):
- <absolute-vault-path>/knowledge/wiki/<category>/<page>.md — Reason: ...
- <absolute-vault-path>/knowledge/wiki/<category>/<page>.md — Reason: ...
(If no relevant wiki pages found: explicitly "no knowledge matches on this topic, write from operations context")

If you need to look up further knowledge yourself, follow this retrieval
mechanic — compact copy of CLAUDE.md → "Retrieval Order", kept in sync from
there (single source; do not extend it here):
1. Expand your search terms via knowledge/wiki/glossary.md (primary
   language ↔ English aliases).
2. Parallel Retrieval — both paths always run, neither is a fallback for
   the other:
   - Path A (Cluster Entry, situational): pages in knowledge/wiki/synthesis/
     with `cluster_tier` frontmatter carry an entry block ("## Entry points
     for requests"); match your situation against its lines and take the
     concrete entry-line hit, not the whole cluster page.
   - Path B (Grep, lexical): grep the expanded keywords across
     knowledge/wiki/{concepts,entities,skills,sources}/, in both language
     variants.
3. knowledge/wiki/index.md only as fallback if both paths come back thin;
   grep into it rather than loading the whole file.

If further vault skills are relevant: check .claude/skills/ and use them

Output:
- Save as: <absolute-vault-path>/output/2026-04-15-<slug>.md
- Frontmatter per the CLAUDE.md output standard: type: deliverable,
  output_type: <from the enum, e.g. analysis>, created: <today>,
  project: "[[ops/projects/<project>]]",
  knowledge_sources_methodical / knowledge_sources_specific: the wiki pages
  listed above as wikilinks (empty list if no matches), tags: [...]
- Language: <vault primary language>

Style:
- Substance over hype
- Technical terms stay in English
- No invented sources — only what is supported in the vault

Requirement for report: <what the user wants to see>
```

## After the Sub-Agent

- **Cold review (Generator/Evaluator split):** start the `Agent` tool with subagent type `output-evaluator`; the prompt contains only the absolute output path — no task justifications. Work findings in via `Edit`, maximum two rounds; the verdict goes into the report, open findings are listed visibly (deliver, do not block). The evaluator checks rule conformance (fact sourcing, frontmatter, type obligations) — the content check against the success criterion in the next point stands alongside it; these are two different reviews.
- Verify the output file — against the success criterion clarified in step 1, not just existence and frontmatter: does the content answer the task? Spot-check the source claims (CLAUDE.md Rule 15)
- If relevant: update the associated `ops/projects/` file with a reference to the new output
- For important completions: add an entry in `ops/chronicle.md`
- Report to the user: brief summary + wikilink to the output, evaluator verdict as footer item (`Evaluator ✓ cold (round N)` or `Evaluator ✗ (N findings open)`)

## Promotion Note

Outputs from `/delegate` land in `output/`. **Do not automatically promote to the wiki.** The user decides in the weekly review or directly whether the material moves to `knowledge/raw/`.

## Done when

- Output file sits under the path set in step 5 with deliverable frontmatter per the CLAUDE.md standard.
- The result is checked against the success criterion from step 1: content answers the task, source claims spot-checked — existence alone does not count.
- If project-related: the `ops/projects/` file carries the reference to the output; for an important completion, the chronicle entry exists.
- Cold review ran (max two rounds); the report names the evaluator verdict and, on an open REJECT, lists the findings visibly.
- Report to the user contains a summary, a wikilink to the output, and the sub-agent's open points.

## Stop — what this skill never does

- Never writes to `knowledge/` (CLAUDE.md Rules 3 and 4); results land exclusively under `output/YYYY-MM-DD-<slug>.md`, promotion is the user's decision (see Promotion Note).
- Never gives the output-evaluator more than the absolute output path — no task justifications and no session history (cold review).
- Never runs more than two evaluator correction rounds; after that the output is delivered, open findings stand visibly in the report instead of blocking completion.
- Never reports completion based on file existence alone; without a check against the success criterion from step 1 (including a spot-check of source claims, CLAUDE.md Rule 15), the task is not done.
- Never conceals an empty knowledge retrieval; if step 4 finds nothing, that is stated explicitly in the sub-agent prompt instead of inventing wiki references (CLAUDE.md Rule 11).
