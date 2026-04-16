---
name: knowledge-query
description: >
  Answers questions against the wiki in the knowledge/ layer. Use when the user
  asks a knowledge question, looks for connections between topics, says
  "what do we know about X", or wants the wiki searched.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Knowledge — Query

Answers questions by searching and synthesizing from the wiki.

## Search Strategy

### 1. Start with the Index

Read `knowledge/wiki/index.md`, identify relevant pages. Scan all category sections (Sources, Entities, Concepts, Synthesis).

### 2. Grep for Targeted Search

For large wikis (>100 pages), index scanning alone is insufficient. Use `Grep`:

```bash
# Example: all pages about "product strategy"
grep -l -ri "product strategy" knowledge/wiki/
```

### 3. Read Relevant Pages

Read the wiki pages identified by the index or search. Follow `[[wikilinks]]` to pull in linked context. Read enough for a solid answer, not the entire wiki.

### 4. Check Sources if Needed

If wiki pages do not fully answer the question, consult matching source summaries in `knowledge/wiki/sources/`. Use `knowledge/raw/` only as a last resort.

## Synthesize the Answer

### Format

Adapt format to the question:
- **Factual question** — direct answer with citations
- **Comparison** — table or structured comparison
- **Exploration** — narrative answer with linked concepts
- **List/catalog** — bullet list with brief descriptions

### Citations

Always cite wiki pages via `[[wikilink]]`:

> According to [[Source — Article Title]], the key finding was X. This connects with the broader pattern in [[Concept-Name]], which also describes [[Entity-Name]].

### Offer to Save Valuable Answers

If the answer produces something worth preserving (comparison, analysis, new connection, synthesis):

> "This analysis might be worth keeping in the wiki. Should I save it as a synthesis page?"

If confirmed:
1. Create new page in `knowledge/wiki/synthesis/` with correct frontmatter (`type: synthesis`, `tags`, `sources`, `created`, `updated`).
2. Add entry in `knowledge/wiki/index.md` under Synthesis.
3. Append to `knowledge/wiki/log.md`: `## [YYYY-MM-DD] query | Question Summary`.

## Conventions

- **Wiki first.** Only go to sources when the wiki has no answer.
- **Cite your claims.** Link every factual statement to the relevant wiki page.
- **Aggregate valuable answers** — feed good analyses back into the wiki.
- `[[wikilinks]]` for all internal references. No raw file paths.

## Related Skills

- `/knowledge-ingest` — process new sources
- `/knowledge-lint` — wiki health check
