---
name: knowledge-ingest
description: >
  Processes source documents from knowledge/raw/ into structured, interlinked wiki pages.
  Use when the user places new files in knowledge/raw/ and says "ingest this",
  "process this source", "I put something in raw/", or wants to incorporate new material
  into the knowledge base.
allowed-tools: Task Bash Read Write Edit Glob Grep WebSearch WebFetch
---

# Knowledge — Ingest

Processes raw sources into structured, interlinked wiki pages.

## Identifying Sources

1. If the user names a specific file or files, use those.
2. If they say "ingest new sources" or similar, detect unprocessed files by following the **canonical detection procedure** in `/knowledge-lint` → Check 8 (normalized matching against wikilink targets and `sources:` frontmatter across the whole wiki — never literal comparison against `log.md`, which produces false positives and risks double-ingesting a source into duplicate pages).
3. If nothing unprocessed is found, let the user know.

## Workflow per Source

### 1. Read the Source Completely

Read the entire file. Examine image references separately if they contain important information.

### 2. Discuss Key Points with the User

**Before writing**, share the 3-5 most important findings. Ask if they want to set priorities or skip any topics. Wait for confirmation.

**Diagnosis first (internal, one line per axis):** Before drafting the takeaways, assess the source on four axes. The result appears in the takeaway template and feeds the depth recommendation — it does **not** land as a block in any wiki page.

- **Document type** — paper / trade article / essay / vendor blog / transcript / social post
- **Evidence quality** — does it rest on data and studies, or on bare assertion?
- **Originality** — what is actually new? "Nothing" is a legitimate finding, not a flaw
- **Author agenda** — vendor self-promotion, recognizable conflict of interest?

The diagnosis is a thinking-and-writing rule, not a web lookup. It sharpens the **skip / light / full** cut: a vendor blog with no new substance and pure self-promotion tends toward *light* or *skip*; a dense source with solid evidence tends toward *full*. The cut becomes reproducible instead of gut-driven. The diagnosis also marks whether a source is **dense/load-bearing** enough for the external reality check (step 4b).

When several sources are queued at once, the **Wave Ingest mode** applies (own section below) — the takeaway depth of 3-5 per source is unchanged there; only the confirmation is bundled.

### 2b. Parallel Retrieval before Any New Page

After confirmation, run **both retrieval paths** against the wiki — same mechanic as `/knowledge-query`, see CLAUDE.md → "Retrieval Order". The point is to know which concepts the source already touches, so we update existing pages instead of creating duplicates, and so we capture missed thematic neighbours.

**Path A — Cluster Entry (situational):**

1. From the 3-5 key takeaways, infer the most likely topic cluster(s) (use the Dataview query in `knowledge-query/SKILL.md` if needed).
2. Read the entry block (`## Entry points for requests`) of each plausible cluster and check which concepts it surfaces for situations matching the source.

**Path B — Grep (lexical):**

1. Take the tentative concept and entity names you would create.
2. Grep them (primary-language + English variants, glossary-expanded) across **all wiki content folders**: `knowledge/wiki/{concepts,entities,skills,sources}/` — same scope as Path B in `/knowledge-query` and CLAUDE.md → "Retrieval Order". Skill and source pages carry concept names too; a concepts+entities-only grep misses them.

**Three consolidation paths:**

| Constellation | What it means | Action |
|---|---|---|
| **Both paths find the same page** | The concept already exists. | Update the existing page, do not create a new one. |
| **Only the cluster finds thematic proximity** | A new concept is forming, but it sits in a known cluster's scope. | Create the new page **and** mark the cluster as a sharpening candidate for its entry block. |
| **Only grep finds an alternate spelling / synonym** | The concept exists under a different name. | Add a glossary entry for the alias, update the existing page, do not duplicate. |

This step never writes — it only informs the decisions in step 4 (entity / concept page handling).

### 3. Create Source Summary

New file in `knowledge/wiki/sources/`, slugified filename. Frontmatter and structure:

```markdown
---
title: Source Title
type: source
tags: [work/domain-a, ...]
sources: ["[[original-filename]]"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Source Title

**Source:** original-filename.md
**Ingested on:** YYYY-MM-DD
**Type:** Article | Paper | Transcript | Notes | etc.

## Summary

Structured summary of the source content.

## Key Findings

- [verified] statement with a referenced / traceable source
- [claim] plausible but unsourced statement (including self-reported results without independent verification)
- [unsourced ⚠️] specific number or factual claim with no source given at all

## Mentioned Entities

- [[Entity-Name]] — brief context

## Covered Concepts

- [[Concept-Name]] — brief context
```

**Provenance markers (mandatory):** Every statement under `## Key Findings` opens with an inline marker classifying its evidence status. Four levels:

- `[verified]` — source referenced or traceable (linked study, named report)
- `[claim]` — plausible but unsourced; includes self-reported results without independent verification
- `[unsourced ⚠️]` — specific number or factual claim with no source given at all
- `[speculation]` — explicitly marked as a forecast or the author's opinion

The marker is a meta-fact about the evidence status, **not** an interpretation — so it is compatible with the "purely factual" rule for source pages (see Conventions). Provenance markers apply to all newly written or touched pages from the start.

### 4. Create or Update Entity and Concept Pages

For each entity (person, organization, product, tool) and each concept (idea, framework, theory, pattern):

**If a wiki page exists:**
- Read the page
- Add new information from this source
- Add the source to the `sources:` frontmatter list
- Update the `updated:` date
- Explicitly flag contradictions with existing content, citing both sources

**If no page exists:**
- Create a new page:
  - `knowledge/wiki/entities/` for people, organizations, products, tools (`type: entity`)
  - `knowledge/wiki/concepts/` for ideas, frameworks, theories, patterns (`type: concept`)
- Frontmatter with `title`, `type`, `tags`, `sources`, `created`, `updated`

**Core-statement head (mandatory):** Every `concept` and `synthesis` page created or touched in this run opens directly under the H1 with a `> ` blockquote of 1-3 sentences carrying the core point self-sufficiently. The normative definition and boundaries (core statement — not an epigraph quote, not a provenance note) live in CLAUDE.md → "Knowledge Operations → Ingest" — this is only the pointer. `/knowledge-lint` Check 10.8 verifies exactly this head; whatever is missed here comes back there as a finding.

**Provenance markers in the body:** Where a concept or synthesis page carries a specific factual claim or number in its prose, that sentence gets the same inline marker as the source key findings (`[verified]` / `[claim]` / `[unsourced ⚠️]` / `[speculation]`, defined in step 3). The **core-statement head itself stays marker-free** ("not a provenance note" applies there). Pure definition or framing sentences without a factual claim need no marker.

### 4b. External Reality Check (dense sources only)

Only for sources the diagnosis (step 2) classified as **dense/load-bearing**. Never blanket-applied to every source: the check costs web access and time, and forcing it onto everything bloats every ingest.

Procedure:

1. Identify the **2-3 load-bearing claims** the source's argument stands on. Not every aside — only the pillars.
2. Check each against the current discourse (`WebSearch`/`WebFetch`). Verdict per claim: **confirmed** (broad consensus / strong evidence) / **contested** (relevant counter-positions) / **refuted** (clear contradiction with the evidence), with one or two sentences of reasoning each.
3. If none of the load-bearing claims is problematic, **one sentence** suffices ("load-bearing claims well supported in current discourse"). No bloated block.

**Where the result goes (layer cleanliness):** The reality check is external assessment, not what the source says. It **never** lands in the source page (which stays "what the source says") — it goes into a clearly labeled block `## Assessment (externally checked, YYYY-MM-DD)` on the concept/synthesis page carrying the claim. The source page may point to it via `[[wikilink]]`.

**Guardrails:** at most 3 checked claims per source; only when diagnosis = dense/load-bearing; result never in the source page.

### 5. Set Wikilinks

Link every mention of an entity or concept that has its own page via `[[wikilink]]` — both from the new page to existing ones and vice versa.

### 6. Update `knowledge/wiki/index.md`

Add one entry per new page under the appropriate category:

```
- [[Page-Name]] — one-liner description (max 120 characters)
```

### 7. Append to `knowledge/wiki/log.md`

Append (newest-first, directly under the file header):

```
## [YYYY-MM-DD] ingest | Source Title
- Source: knowledge/raw/.../filename.md
- Created: entities/xyz.md, concepts/abc.md
- Updated: concepts/def.md
- Tags: work/domain-a
```

### 8. Review `knowledge/wiki/overview.md`

Only update if the new source genuinely shifts the overall picture.

### 9. Retrieval Hookup

New pages are only done when they will be reachable through the retrieval paths tomorrow. Two checks:

**Glossary (free write permission — infrastructure):** For every new concept/entity page, check whether the common primary-language **and** English names are listed as aliases in `knowledge/wiki/glossary.md`. Add missing aliases directly (`- [[canonical-page]] — alias1, alias2`). Same rule as in `/knowledge-query` → "Maintaining the Glossary": the glossary is infrastructure, not a knowledge page, and needs no individual confirmation.

**Cluster entry lines (narrow sharpening protocol — no standing write permission):** For central new concepts, check whether a thematically matching cluster makes them reachable via its `## Entry points for requests` block. If not: draft an entry line (`"<situation>" → [[concepts/<name>]]`). Such a line is written **exclusively** through the sharpening protocol from `/knowledge-query` → "Entry-Block Sharpening" — exactly one line, a `sharpen` entry in `log.md`, and only if the line was part of the user-confirmed write plan or the user confirms it individually. Otherwise it remains a **candidate**: named in the report (step 12) and in the ingest log entry. Cluster pages are "Do not write casually" — ingest gets no standing license here.

### 10. Definition of Done

Before the report, verify across all pages created or touched in this run:

- [ ] Every new page has an `index.md` entry under the correct category
- [ ] `log.md` entry appended (newest-first, directly under the header)
- [ ] Every touched existing page: source added to `sources:` frontmatter, `updated:` refreshed
- [ ] Every new or touched concept/synthesis page carries the core-statement head (step 4)
- [ ] Every new/touched source page carries provenance markers on its key findings; concept/synthesis pages on their body factual claims (steps 3/4)
- [ ] For dense sources: external reality check ran, result on the concept/synthesis page (never in the source page), step 4b
- [ ] All outgoing `[[wikilinks]]` of the new/touched pages resolve to existing files — verify mechanically (grep/script over the touched-page list), not by feel
- [ ] Glossary aliases checked (step 9)

### 11. Findability Smoke Test

Ingest does not end at "written" — it ends at "findable". For **1-2 central new concepts** of the run (in waves: the most important ones of the wave):

1. Formulate a realistic question the user might ask in a week — deliberately **not** in the wording of the page title.
2. Have a **context-free subagent** (general-purpose, without this run's ingest knowledge) run the retrieval paths: glossary expansion, then cluster entry + grep in parallel (mechanics: `/knowledge-query`). The author must not test themselves — they know where the page is.
3. Evaluate: the subagent finds the page via at least one path → passed. It does not → close the gap immediately: missing glossary alias → add it directly (step 9); missing entry line → candidate, same confirmation rule as in step 9 — the smoke test creates **no** write permission of its own on cluster pages.
4. Include the result (passed / gap + fix) in the report and the log entry.

### 12. Report

Tell the user:
- Created pages (with wikilinks)
- Updated pages (what changed)
- Newly identified entities and concepts
- Contradictions found
- Smoke-test result (step 11) and open entry-line candidates (step 9)
- Check the lint threshold (definition and counting method: `/knowledge-lint` → "When to Lint") — if crossed, suggest `/knowledge-lint`

## Wave Ingest (optional mode for source batches)

When several fresh sources are queued at once (batches of roughly 4-14 raw files), the workflow runs bundled instead of strictly serial. The mode changes the cadence, not the diligence — every rule from "Workflow per Source" still applies.

1. **Scope the wave.** Identify unprocessed sources (procedure under "Identifying Sources" above), name the wave, group sources into thematic clusters (Cluster A, B, C …).
2. **Bundled takeaway round — the per-source takeaway depth is non-negotiable.** For **every** source in the wave: 3-5 key takeaways, the four-axis diagnosis (step 2), and a derived depth recommendation: **full** (source + concept/entity work), **light** (source page only, possibly bundled with others), **skip** (do not ingest, with reason). The recommendation follows the diagnosis, not gut feeling: thin vendor self-promotion tends toward light/skip; dense, well-evidenced sources toward full. The confirmation may be bundled — one answer for the whole wave — but every source appears individually in the template with its takeaways, diagnosis, and recommendation. Blanket sentences ("ten sources, all interesting") are not a gate. Nothing is written without confirmation.
3. **Retrieval once across the wave.** Parallel Retrieval (step 2b) consolidated across all planned concept/entity names of the wave instead of per source — make dedup decisions across the clusters (typical: several sources in the same wave touch the same concept → one page, multiple `sources:` entries).
4. **Write cluster by cluster.** Per source, steps 3-5; `index.md`, glossary, and the `overview.md` check once at the end of the wave.
5. **One log entry per wave** instead of per source:

   ```
   ## [YYYY-MM-DD] ingest-wave | <wave title: key sources>
   - **N raw files processed.** [extraction and verification notes]
   - **Tally: N sources, N entities new, N concepts new; ~N updates; index, glossary, log.**
   - **Agreed cuts:** [skip/light decisions with reasons]
   ### Cluster A — <topic>
   - Created: … / Updated: …
   - Tags: [domain tags of the wave]
   ```

6. **Steps 9-12 once across the whole wave** (retrieval hookup, Definition of Done, smoke test, report).

## Conventions

- Source summary pages are **purely factual**. Interpretation and synthesis belong in concept and synthesis pages. Provenance markers (`[verified]` etc., step 3) are compatible with this rule: they are meta-facts about a claim's evidence status, not interpretation. The external reality check, by contrast, is external assessment and never belongs in the source page (step 4b).
- A single source typically touches **5-15 wiki pages** — ~10 is normal and desired. Do not compress out of caution.
- When new information contradicts existing wiki content: **update the wiki page and document the contradiction** citing both sources.
- **Prefer updating existing pages** over creating new ones. Only create a new page if the topic is sufficiently independent.
- `[[wikilinks]]` for all internal references. Never raw file paths.
- English technical terms (e.g. "Prompt Engineering") stay in English regardless of the wiki's primary language.
- Use tags from the domain taxonomy defined in CLAUDE.md.

## What Comes Next

After ingesting, the user can:
- **Ask questions** with `/knowledge-query`
- **Ingest more sources**
- **Health-check** with `/knowledge-lint` once the lint threshold is crossed (countable definition in `/knowledge-lint` → "When to Lint"; step 12 checks it at the end of every run)

## Stop — what this skill never does

- Never write wiki pages before the user has confirmed the 3-5 takeaways per source (step 2). In wave mode the confirmation may be bundled, but the gate stands: blanket sentences do not count; nothing is written without confirmation.
- Never modify files in `knowledge/raw/`. Sources are read, not edited (CLAUDE.md Rule 1).
- Never create a new concept or entity page without Parallel Retrieval (step 2b) having run. On an existing hit, the page is updated, not duplicated.
- Never touch cluster pages outside the sharpening protocol (step 9): at most one confirmed entry line, no standing write permission. The smoke test (step 11) creates none either.
- Never detect unprocessed sources via literal comparison against `log.md`. The canonical procedure from `/knowledge-lint` → Check 8 is the only valid method.
- Never run the findability smoke test with the author's own ingest context. The checking subagent stays context-free; the author does not test themselves (step 11).
- Never write the external reality check into the source page. It belongs as a labeled "Assessment (externally checked)" block on the concept/synthesis page (step 4b).
- Never blanket-apply the web check to every source. Only when diagnosis = dense/load-bearing, at most 3 load-bearing claims (step 4b).
- Never write a relevance verdict ("keep/ignore") or personal-transfer commentary into a wiki page. The factual layer stays free of personalization; that job deliberately lives outside ingest.

## Related Skills

- `/knowledge-query` — answer questions
- `/knowledge-lint` — wiki health check
