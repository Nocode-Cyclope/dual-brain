---
name: delegate
description: Delegates a task to an autonomous sub-agent. Uses only ops/ context, writes results to output/. For more complex research, writing, or analysis tasks.
allowed-tools: Read, Glob, Grep, Agent
---

# /delegate — Delegate a Task

Has a sub-agent work through a scoped task autonomously.

## When to Use

- Research tasks that need depth (e.g., "compare the last three AI frameworks for sales enablement")
- Longer writing tasks without strict knowledge dependency
- Analyses spanning many files
- Tasks that justify sub-agent isolation (context protection)

**Do not use for:**
- Simple classification or capture (`/new` is sufficient)
- Wiki ingest (`/knowledge-ingest` is sufficient)
- **Concept/content creation with active knowledge retrieval** -> `/produce` is better suited (dedicated workflow for Methodological + Specific)

## Steps

1. **Understand the task** — clarify context, goal, success criterion. If unclear, use `AskUserQuestion`.
2. **Capture the source repo** — current vault path. Provide all paths as absolute to the sub-agent.
3. **Identify context files** — what does the sub-agent need to read?
   - Relevant `ops/projects/`, `ops/tasks/`, `ops/people/`, `ops/context/` files, named via wikilink
4. **Knowledge discovery (always run, lightweight):**
   - Extract terms from task wording, project tags, and involved people
   - Read `knowledge/wiki/index.md`, search there for the terms
   - `Grep` over `knowledge/wiki/{entities,concepts,synthesis}/` for the top terms
   - Include 2-6 relevant wiki pages as absolute paths in the sub-agent prompt
   - If nothing relevant is found: honestly note in the prompt ("no relevant knowledge pages on this topic in the wiki")
   - If extensive need (>6 pages or methodological+specific need clean separation): recommend `/produce` instead
5. **Set the output path** — `output/YYYY-MM-DD-<slug>.md`
6. **Compose the prompt** for the sub-agent (see template below)
7. **Start the sub-agent** with the `Agent` tool, subagent type depending on task: `general-purpose` for research/writing, `Explore` for pure vault exploration
8. **Review the result** and report to the user — what was produced, where it is

## Sub-Agent Prompt Template

```
Goal: <concrete task in 1-2 sentences>

Context from Operations Layer:
- Vault root: <absolute-vault-path>
- Project: <absolute-path>/ops/projects/<project>.md
- Stakeholders: <absolute-path>/ops/people/<person>.md
- Daily plan reference: <absolute-path>/ops/daily/<date>.md (if available)

Context from Knowledge Layer (previously researched via Grep on wiki/index.md):
- <absolute-path>/knowledge/wiki/<category>/<page>.md — Reason: ...
- <absolute-path>/knowledge/wiki/<category>/<page>.md — Reason: ...
(If no relevant wiki pages found: explicitly "no knowledge matches on this topic, write from operations context")

If further vault skills are relevant: check .claude/skills/ and use them

Output:
- Save as: <absolute-path>/output/2026-04-15-<slug>.md
- Frontmatter: type: deliverable, created: <today>, source: delegate, related: ["[[ops/projects/<project>]]"]
- Substance over hype

Requirement for report: <what the user wants to see>
```

## After the Sub-Agent

- Verify the output file (exists, frontmatter correct)
- If relevant: update the associated `ops/projects/` file with a reference to the new output
- For important completions: add an entry in `ops/chronicle.md`
- Report to the user: brief summary + wikilink to the output

## Promotion Note

Outputs from `/delegate` land in `output/`. **Do not automatically promote to the wiki.** The user decides in the weekly review or directly whether the material moves to `knowledge/raw/`.
