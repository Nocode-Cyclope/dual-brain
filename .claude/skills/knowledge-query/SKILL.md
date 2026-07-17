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

**Discipline:** Steps 1 and 2 are **mandatory** before every query — not only for hard questions. They cost little but prevent the two most common failure modes: (a) the right page exists but is not found because the question uses a synonym; (b) cluster entry and grep are played off against each other instead of run in parallel — losing either the situational or the lexical hits.

### 1. Glossary Check First (synonym bridge)

Read `knowledge/wiki/glossary.md` (or grep into it directly when the term is clear).

- Match the question's terms against the aliases.
- Note the **canonical page name** plus every alias listed there.
- That is the search-term list for Path B in step 2.

If the question contains a term missing from the glossary: continue anyway, but add the entry after the query (see "Maintaining the Glossary" below).

### 2. Parallel Retrieval — Cluster Entry + Grep

**Both paths always run.** They are not fallbacks for each other — they solve different problems. Cluster Entry is situational (request situation → entry block → concept). Grep is lexical (keyword → concept hit). Run them in parallel, collect two separate result lists, then compare.

#### Path A — Cluster Entry (situational)

1. Find the candidate clusters via this Dataview query (or run it mentally if Dataview is not available):

   ~~~dataview
   TABLE cluster_tier, cluster_slug, concepts_covered
   FROM "knowledge/wiki/synthesis"
   WHERE type = "synthesis" AND cluster_tier
   SORT cluster_tier ASC, concepts_covered DESC
   ~~~

2. Read the entry block of each plausible cluster:

   ```bash
   grep -A 20 "^## Entry points for requests" "knowledge/wiki/synthesis/cluster-<slug>.md"
   ```

   Grep for the literal heading used in the cluster pages (if the vault's cluster pages are authored in another primary language, use that heading verbatim).

3. Semantically match the request situation against the entry lines. Each line has the form `"<situation>" → [[concepts/<name>]]`. Collect the resulting concept (and optional skill) wikilinks as `CLUSTER_HITS`.

4. If no cluster matches: take the closest cluster's `Topic unclear →` fallback line.

5. **Large-cluster rule:** for clusters with `concepts_covered` above 50 the entry block is longer. Always return the concrete entry-line hit, never the cluster page as a whole (threshold rule, normative in CLAUDE.md → Retrieval Order).

#### Path B — Grep (lexical)

1. Take the keywords from the request, expanded with the glossary aliases from step 1.
2. Grep across the wiki, primary-language **and** English variants always:

   ```bash
   # canonical term, synonym, primary-language variant
   grep -rln -i "customer segmentation" knowledge/wiki/
   grep -rln -i "client segmentation" knowledge/wiki/
   grep -rln -i "<primary-language variant>" knowledge/wiki/
   ```

3. Backlink check on each candidate:

   ```bash
   grep -rln "\[\[concepts/customer-segmentation\]\]" knowledge/wiki/
   ```

4. Cap at 10 hits per keyword. More than that → keyword too generic, refine.
5. Ranking when consolidating hits: `concepts > skills > synthesis > sources`. Tiebreaker: backlink count.
6. Collect the resulting wikilinks as `GREP_HITS`.

#### Merge step — compare the two lists

Three constellations (normative in CLAUDE.md → Retrieval Order; here the operational handling):

| Constellation | Meaning | Handling |
|---|---|---|
| **Overlap** (both paths find the same concept) | High confidence, the situational entry and the lexical match agree. | Central page for the answer. |
| **Cluster-only hit** | The situational entry surfaced something the keywords did not match (often: synonym bridge). | Include in the answer; check whether the glossary needs a new alias. |
| **Grep-only hit** | Lexical match that the cluster entry block does not surface. | Include in the answer **and** flag as `sharpening_candidate` for the matching cluster's entry block. |

Grep-only hits are the explicit feedback signal of the system — they grow the entry blocks over time (see "Entry-Block Sharpening" below).

### 3. Read Relevant Pages

Open the identified pages (from `CLUSTER_HITS` and `GREP_HITS`) with `Read`. Follow `[[wikilinks]]` on the pages you read to pull in linked context. Read enough for a grounded answer, not the entire wiki.

### 4. Index or Source Fallback if Needed

Open `knowledge/wiki/index.md` only as a fallback when both paths come back thin — the index is structural navigation, not a retrieval path. If the wiki pages do not fully answer the question, consult matching source summaries in `knowledge/wiki/sources/`. Use `knowledge/raw/` only as a last resort.

## Query Log

Every explicit `/knowledge-query` invocation gets logged to:

```
ops/context/query-log/YYYY-MM-DD--<question-slug>.md
```

**Why `ops/context/`?** Operational meta-knowledge, not knowledge production. The promotion rule (Knowledge is never written from Ops) stays intact — query logs are an Ops artefact about Knowledge usage, not a Knowledge artefact.

**Frontmatter (mandatory):**

```yaml
---
type: context
tags: [meta/query-log]
captured: 2025-01-22
question: "<verbatim question>"
cluster_path_hits: ["[[concepts/...]]", ...]
grep_path_hits: ["[[concepts/...]]", ...]
overlap: ["[[concepts/...]]", ...]
cluster_only: ["[[concepts/...]]", ...]
grep_only: ["[[concepts/...]]", ...]
sharpening_candidates: ["[[concepts/...]]", ...]
clusters_inspected: 3        # countable: cluster entry blocks read
grep_keywords: 8             # countable: keywords grepped incl. glossary expansions
---
```

`sharpening_candidates` is the subset of `grep_only` items that semantically belong to the matching cluster's scope but do not appear in its entry block.

**Body sections:**

1. **Cluster path** — which clusters were inspected, which entry lines matched, which concepts came out.
2. **Grep path** — which keywords were grepped (incl. glossary expansions), which hits ranked highest.
3. **Comparison** — overlap / cluster-only / grep-only with one-line notes.
4. **Sharpening candidates** — for each, a proposed new entry line in the format `"<situation>" → [[concepts/<name>]]`, ready to be inserted into the cluster's entry block.

For implicit wiki consultations (Axis 2 of Continuous Routing in CLAUDE.md), the parallel paths still run silently but no log file is written — otherwise the directory floods.

## Entry-Block Sharpening

The cluster entry blocks are the system's situational index. They get better only when they are sharpened against real-world queries.

**Triggers:**

- **Manual** — the user says "sharpen the entry block of <cluster>" or equivalent.
- **Automatic, accumulative** — aggregation as defined once in `/knowledge-lint` Check 10.7 (≥3 query logs naming the same `grep_only` concept for the same cluster): when the threshold is met, proactively propose the new entry line in the next response.

**Procedure:**

1. Read the cluster page (`knowledge/wiki/synthesis/cluster-<slug>.md`).
2. Insert a new entry line in the format `"<situation>" → [[concepts/<name>]]` directly before the closing `Topic unclear →` line. The situation phrasing stays in the language the cluster page uses.
3. Set `updated:` in the frontmatter to today.
4. Append a log entry to `knowledge/wiki/log.md`: `## [YYYY-MM-DD] sharpen | cluster-<slug>` with the new line as quoted body.
5. Leave the query logs in place — they are the historical trace of why the entry line was added.

Cluster pages are "Do not write casually" (CLAUDE.md). Sharpening edits stay narrow: one line at a time, with a log entry, no broader restructuring.

## Maintaining the Glossary

Two occasions during a query to extend `knowledge/wiki/glossary.md`:

1. **Alias gap:** the question contained a term that grep did not find although the page exists → add the term as an alias to the canonical entry.
2. **New entry:** a relevant term/concept is missing entirely → create a new entry in the appropriate category.

Keep it short: `- [[canonical-page]] — alias1, alias2, alias3`. The user does not need to confirm this explicitly — the glossary is infrastructure, not a knowledge page.

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
3. Append to `knowledge/wiki/log.md` (newest-first): `## [YYYY-MM-DD] query | Question Summary`.

## Conventions

- **Wiki first.** Only go to sources when the wiki has no answer.
- **Cite your claims.** Link every factual statement to the relevant wiki page.
- **Aggregate valuable answers** — feed good analyses back into the wiki.
- `[[wikilinks]]` for all internal references. No raw file paths.

## Stop — what this skill never does

- Never answer without the glossary check and Parallel Retrieval: steps 1 and 2 of the search strategy are mandatory before every query, even simple ones.
- Never return the cluster page as a whole for large clusters (`concepts_covered` above 50) — always the concrete entry line.
- Never create a synthesis page without the user's explicit confirmation; valuable answers are offered for saving, never saved unilaterally. The only confirmation-free write exception is glossary maintenance (see "Maintaining the Glossary": infrastructure, not a knowledge page).
- Never touch cluster pages more broadly than one entry line per sharpening edit, always with a log entry in `log.md`; on automatic aggregation the new line is proposed, not inserted unasked ("Do not write casually", CLAUDE.md).
- Never write query logs for implicit wiki consultations (Axis 2); the log applies only to explicit `/knowledge-query` invocations.
- Never modify `knowledge/raw/` (CLAUDE.md Rule 1); raw/ serves only as a last reading resort.

## Related Skills

- `/knowledge-ingest` — process new sources
- `/knowledge-lint` — wiki health check
