---
name: produce
description: >
  Produces a content output (concept paper, memo, email, pitch, analysis) in the context
  of an operations item, actively drawing on the Knowledge Layer (methodological knowledge
  + specific prior work). Use when the user says "write me a concept for...",
  "draft a memo for...", "produce a pitch...", "email to X about Y", etc.
argument-hint: <output type and context, e.g. "concept for Q3 product launch onboarding for Sarah">
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Agent
---

# /produce — Knowledge-Powered Production

Produces outputs in the operations context with active knowledge retrieval. This is the primary cross-layer workflow.

> **Core principle:** The operations anchor defines *what for* the writing happens. The Knowledge Layer supplies *what with* (methodological frameworks + specific prior work). Output lands in `output/` with a complete source list.

## Steps

### 1. Determine the Operations Anchor

What is this concretely about? Clarify from `$ARGUMENTS` and context:
- **Which output type?** Concept paper / Memo / Email / Pitch / Analysis / FAQ / One-pager / Script / etc.
- **Which project?** Search for `ops/projects/` slug (`Glob`/`Grep` on tags, names, topics). If ambiguous: `AskUserQuestion`.
- **Which people/addressees?** Search for `ops/people/` slugs.
- **What is the success criterion?** If unclear: brief clarifying question.

### 2. Load Addressee and Project Context

- Read the project file (status, next actions, stakeholders)
- Read addressee file(s) (role, last-contact, follow-ups)
- Scan last 1-2 daily entries for the project (`grep -l "[[ops/projects/<slug>]]" ops/daily/`)

### 3. Knowledge Discovery (Two Sources)

#### 3a. Methodological Knowledge — "how to write this well"

Derive verb/noun from the output type and find matching methodological wiki pages:

```bash
# Methodological skill pages
grep -lri "skill-" knowledge/wiki/concepts/ | grep -i "<verb-from-mapping>"

# Frameworks
grep -lri "framework\|principle\|pattern" knowledge/wiki/concepts/ | grep -i "<topic>"
```

Mapping aids (typical):
- "Concept", "Strategy" -> `strategy-*`, `minimum-viable-strategy`, `walking-skeleton`
- "Email", "Letter" -> `skill-email-writing`, `storytelling-*`
- "Pitch", "Presentation" -> `bid-presentations-*`, `executive-summary-tactics`
- "Analysis" -> `skill-competitive-analysis`, `analysis-*`, `thinking-tools-*`
- "FAQ", "Onboarding" -> `change-communication`, `audience-profile`
- "Workshop concept" -> `ideation-*`, `pip-decks-*`
- "Speech", "Talk" -> `storytelling-*`, `narrative-structures`

#### 3b. Specific Knowledge — "what we already know about this / have produced"

- Extract project tags and terms
- Read `knowledge/wiki/index.md`, search there with the terms
- Open matches in `knowledge/wiki/sources/`, `concepts/`, `synthesis/`
- Follow linked entities (e.g., if the project is tagged with `[[acme-corp]]`, check all wiki pages with that name in their name or frontmatter)
- Person-related: if `[[ops/people/john-doe]]` is involved, check whether `knowledge/wiki/entities/john-doe.md` exists and read it

```bash
# Specific wiki pages on project/topics
grep -lri "<project-topic>" knowledge/wiki/{sources,concepts,synthesis}/
```

#### 3c. Consolidate Results

Build a list:
- **Methodological (M):** [[page-1]], [[page-2]], ...
- **Specific (S):** [[page-3]], [[page-4]], ...

With justification per page (half a sentence explaining why this page).

### 4. Adaptive Confirmation with the User

**Rule of thumb for confirmation:**
- **Expected output length < ~500 words** (short email, brief memo, reply text) -> write directly, show sources at the end
- **Expected output length >= ~500 words** (concept paper, detailed memo, FAQ, pitch deck outline) -> present source list for confirmation first

Direct case — brief announcement, then write:
> "Writing directly — using [[skill-email-writing]] (M) and [[acme-strategy-guide]] (S). Result coming up."

Confirmation case:
> "Before I start — these are the knowledge sources I would pull in:
>
> **Methodological:**
> - [[skill-concept-writing]] — structure and tone
> - [[strategy-signal-workshop]] — argumentation logic
>
> **Specific:**
> - [[acme-rollout-masterplan]] — existing framework
> - [[acme-guiding-principles]] — tonality and stance
> - [[status-quo-report-2026-04-01]] — factual baseline
>
> Does that work? Anything to add or remove?"

On removals: note them, do not use. On additions: include them in the list.

### 5. Write

Output to `output/YYYY-MM-DD-<type>-<slug>.md`. Frontmatter:

```yaml
---
type: deliverable
output_type: concept | memo | email | pitch | analysis | faq | onepager | script
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
- Substance over hype — the user's stance
- No invented facts — only what is supported in the vault
- Wikilinks in the body where knowledge directly comes from a wiki page (makes sources traceable for the reader)

### 6. Backlinks and Updates

- **Update project file**: in `ops/projects/<slug>.md` under `## Outputs` add a wikilink, reset `updated:`
- **For important outputs**: entry in `ops/chronicle.md`
- **Do not touch knowledge pages** — backlink visibility is created automatically via Obsidian backlinks (every wiki page now shows the outputs it fed into)

### 7. Report

Brief confirmation to the user:

> Created: [[output/2026-04-15-concept-q3-launch-onboarding]] (concept, ~800 words)
> Sources: 3 methodological, 4 specific
> Project updated: [[ops/projects/q3-product-launch]] (Outputs section)

## Edge Cases

- **Knowledge is empty on the topic** -> tell the user honestly: "I find nothing specific about X in the wiki. Should I write from methodological knowledge and you provide the factual basis?"
- **Multiple projects match** -> `AskUserQuestion` with the candidates
- **Output type unclear** -> brief clarifying question, do not guess
- **Contradictions between knowledge sources** -> name them in the output, do not hide them (aligns with "substance over hype")

## Promotion Note

Outputs from `/produce` land in `output/`. **Do not automatically promote to the wiki.** If the output contains substantial new knowledge (e.g., a standalone concept), the user offers promotion to `knowledge/raw/` in the weekly review or directly — and then optionally triggers `/knowledge-ingest`.

## Related Skills

- `/delegate` — when the output is extensive and sub-agent isolation helps
- `/knowledge-query` — when only knowledge is sought, no output produced
- `/new` — for pure capture without production
