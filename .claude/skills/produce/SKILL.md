---
name: produce
description: >
  Produces a content output (concept paper, memo, email, pitch, analysis) in the context
  of an operations item, actively drawing on the Knowledge Layer (methodological knowledge
  + specific prior work). Use when the user says "write me a concept for...",
  "draft a memo for...", "produce a pitch...", "email to X about Y", etc.
argument-hint: <output type and context, e.g. "concept for the website relaunch onboarding for Sarah Chen">
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Agent
---

# /produce — Knowledge-Powered Production

Produces outputs in the operations context with active knowledge retrieval. This is the primary cross-layer workflow.

> **Core principle:** The operations anchor defines *what for* the writing happens. The Knowledge Layer supplies *what with* (methodological frameworks + specific prior work). Output lands in `output/` with a complete source list.

## Steps

### 1. Determine the Operations Anchor

What is this concretely about? Clarify from `$ARGUMENTS` and context:
- **Which output type?** Concept / Memo / Email / Pitch / Analysis / FAQ / One-pager / Script / etc.
- **Which project?** Search for `ops/projects/` slug (`Glob`/`Grep` on tags, names, topics). If ambiguous: `AskUserQuestion`.
- **Which people/addressees?** Search for `ops/people/` slugs.
- **What is the success criterion?** If unclear: brief clarifying question.

### 2. Load Addressee and Project Context

- Read the project file (status, next actions, stakeholders)
- Read addressee file(s) (role, last-contact, follow-ups)
- Scan last 1-2 daily entries for the project (`grep -l "[[ops/projects/<slug>]]" ops/daily/`)

### 3. Knowledge Discovery (Two Sources)

> **Parallel Retrieval applies to both 3a and 3b.** Cluster Entry (which cluster in `knowledge/wiki/synthesis/` covers the situation?) **and** Grep both run — they are not fallbacks for each other. Cluster finds situational hits via the entry block; Grep finds lexical hits via keywords. Compare the two lists, and mark grep-only hits as sharpening candidates if they belong in the matching cluster's scope. See CLAUDE.md → "Retrieval Order" and `knowledge-query/SKILL.md`.

#### 3a. Methodological Knowledge — "how to write this well"

Retrieval per CLAUDE.md → "Retrieval Order" (Parallel Retrieval), with the output type as the cluster-entry situation: formulate the situation from the output type ("write an email to a client", "build a competitive analysis") and match it against the clusters' entry blocks; in parallel, grep the glossary-expanded terms across all wiki folders — skill pages live in `skills/`, not in `concepts/`:

```bash
grep -lri "<topic-or-verb>" knowledge/wiki/{skills,concepts}/
```

For large clusters, take only the concrete entry-line hit, never the whole page. No hardcoded slug lists — the entry blocks are the maintained situational index.

#### 3b. Specific Knowledge — "what we already know about this / have produced"

- Extract project tags and terms, expand them via `glossary.md` with primary-language/English aliases
- Grep across all wiki folders (do not read `index.md` — it is a navigation catalog and declared fallback, see Retrieval Order):

```bash
# Specific wiki pages on project/topics
grep -lri "<project-topic>" knowledge/wiki/{sources,concepts,synthesis,entities,skills}/
```

- Follow linked entities (e.g., if the project is tagged with `[[acme-corp]]`, check all wiki pages with `acme-corp` in their name or frontmatter)
- Person-related: if `ops/people/sarah-chen.md` is involved, check whether `knowledge/wiki/entities/sarah-chen.md` exists and read it too

#### 3c. Consolidate Results

Build a list:
- **Methodological (M):** [[page-1]], [[page-2]], ...
- **Specific (S):** [[page-3]], [[page-4]], ...

With justification per page (half a sentence explaining why this page).

### 4. Adaptive Confirmation with the User

**Rule of thumb for confirmation:**
- **Expected output length < ~500 words** (short email, brief memo, reply text) → write directly, show sources at the end
- **Expected output length >= ~500 words** (concept paper, detailed memo, FAQ, pitch deck outline) → present the source list for confirmation first

Direct case — brief announcement, then write:
> "Writing directly — using [[skill-email-writing]] (M) and [[acme-strategy-guide]] (S). Result coming up."

Confirmation case:
> "Before I start — these are the knowledge sources I would pull in:
>
> **Methodological:**
> - [[skill-concept-writing]] — structure and tone
> - [[argument-first-structure]] — argumentation logic
>
> **Specific:**
> - [[website-relaunch-masterplan]] — existing framework
> - [[acme-guiding-principles]] — tonality and stance
> - [[status-quo-report-2026-04-01]] — factual baseline
>
> Does that work? Anything to add or remove?"

On removals: note them, do not use. On additions: include them in the list.

### 5. Write

Output to `output/YYYY-MM-DD-<type>-<slug>.md`. Frontmatter follows the vault-wide output standard in CLAUDE.md (single source); `output_type` from the enum there (`concept | memo | email | pitch | analysis | faq | onepager | script | worksheet | social-media-post`). Example skeleton:

```yaml
---
type: deliverable
output_type: concept
created: 2026-04-15
project: "[[ops/projects/<slug>]]"
addressed_to: ["[[ops/people/<slug>]]"]   # optional, can be empty
knowledge_sources_methodical:
  - "[[knowledge/wiki/concepts/<slug>]]"
knowledge_sources_specific:
  - "[[knowledge/wiki/sources/<slug>]]"
  - "[[knowledge/wiki/concepts/<slug>]]"
tags: [...]
---

# <Title>

<Body>

---

## Source Base

**Methodological:**
- [[knowledge/wiki/concepts/<slug>]] — What for
- ...

**Specific:**
- [[knowledge/wiki/sources/<slug>]] — What for
- ...
```

While writing:
- Technical terms stay in English regardless of the vault's primary language
- Substance over hype
- No invented facts — only what is supported in the vault
- Wikilinks in the body where knowledge directly comes from a wiki page (makes sources traceable for the reader)

### 5b. Cold Review (Generator/Evaluator Split)

The author does not certify their own work. After writing:

1. Start the `Agent` tool with subagent type `output-evaluator`. The prompt contains **only** the absolute path of the output file — no justifications, no session summary. The evaluator's strength is the absence of author context.
2. Work findings in via `Edit`, run the evaluator again. **Maximum two rounds.**
3. The verdict goes into the report (step 7) and the chat footer, as `Evaluator ✓ cold (round N)` or `Evaluator ✗ (N findings open)` — **not into the deliverable file** (deliverables carry no self-check footer).
4. If a REJECT remains after round 2: deliver, do not block. The report lists the open findings visibly; the user decides.

### 6. Backlinks and Updates

- **Update the project file**: in `ops/projects/<slug>.md` under `## Outputs`, add a wikilink and reset `updated:`
- **Maintain the `knowledge:` field**: add the project-relevant wiki pages confirmed in step 4 (not the purely output-specific ones) to the `knowledge:` frontmatter field of the project file, without duplicates — this is the Knowledge Bridge maintenance that CLAUDE.md assigns to `/produce`
- **For important outputs**: entry in `ops/chronicle.md`
- **Do not touch knowledge pages** — backlink visibility is created automatically via Obsidian backlinks (every wiki page now shows the outputs it fed into)

### 7. Report

Brief confirmation to the user:

> Created: [[output/2026-04-15-concept-relaunch-onboarding]] (concept, ~800 words)
> Sources: 3 methodological, 4 specific
> Evaluator ✓ cold (round 2) — or, on an open REJECT: Evaluator ✗ (N findings open): [list]
> Project updated: [[ops/projects/website-relaunch]] (Outputs section)

## Edge Cases

- **Knowledge is empty on the topic** → tell the user honestly: "I find nothing specific about X in the wiki. Should I write from methodological knowledge and you provide the factual basis?"
- **Multiple projects match** → `AskUserQuestion` with the candidates
- **Output type unclear** → brief clarifying question, do not guess
- **Contradictions between knowledge sources** → name them in the output, do not hide them (substance over hype)

## Promotion Note

Outputs from `/produce` land in `output/`. **Do not automatically promote to the wiki.** If the output contains substantial new knowledge (e.g., a standalone concept), offer the user promotion to `knowledge/raw/` in the weekly review or directly — which then optionally triggers `/knowledge-ingest`.

## Done when

- Output sits under `output/YYYY-MM-DD-<type>-<slug>.md` with complete deliverable frontmatter; `knowledge_sources_methodical`/`_specific` match the Source Base section.
- For expected length >= ~500 words, the source confirmation happened before writing; anything the user removed was not used.
- Project file is updated: outputs wikilink, `knowledge:` field without duplicates, fresh `updated:`.
- No file under `knowledge/` was touched.
- Cold review ran (step 5b, max two rounds); the report names the evaluator verdict and, on an open REJECT, lists the findings visibly.
- Report names the output, source counts, and updated project as wikilinks.

## Stop — what this skill never does

- Never creates or modifies files under `knowledge/` (CLAUDE.md Rule 3); writing goes exclusively to `output/`, plus updates to the project file and chronicle.
- Never promotes the output automatically to the wiki; promotion to `knowledge/raw/` remains the user's explicit step (see Promotion Note).
- Never certifies its own deliverable; the review is done by the cold `output-evaluator` (step 5b), and the deliverable file carries no self-check footer.
- Never runs more than two evaluator rounds; after round 2 the output is delivered, open findings stand visibly in the report.
- Never uses knowledge sources the user removed in the confirmation; never starts writing without a confirmed source list once the expected length reaches ~500 words.
- Never invents facts, numbers, or sources; only what is supported in the vault counts (CLAUDE.md Rule 11).

## Related Skills

- `/delegate` — when the output is extensive and sub-agent isolation helps
- `/knowledge-query` — when only knowledge is sought, no output produced
- `/new` — for pure capture without production
