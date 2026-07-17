---
name: knowledge-lint
description: >
  Health check of the wiki for contradictions, orphan pages, stale claims, missing
  cross-references, missing provenance markers, and unprocessed sources. Use when
  the user says "audit", "health check", "lint", "find problems", or wants to
  improve wiki quality.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Knowledge — Lint

Health check of the wiki. Report with actionable fixes.

**Wiki folder set:** Where this skill says "all wiki subfolders", the folder list from the Architecture block in CLAUDE.md applies (single source: `sources/`, `entities/`, `concepts/`, `skills/`, `synthesis/`). No per-check folder enumeration — if CLAUDE.md gains a folder, it is automatically covered here. Checks with a deliberately narrower scope (e.g. 10.8: only `concepts/` and `synthesis/`) name their deviation themselves.

## Execution

A grown wiki is too large to run every check over the full inventory inside one context. Therefore two modes plus fan-out:

**Routine run (default):** Mechanical checks (1, 2, 5, 7, 8, 10.x) always run over the full inventory — they are grep/script-able and scale. Semantic checks (3, 4, 6, 9) run over the **delta**: the pages touched since the last `lint |` entry in `log.md` (taken from the log entries since then), checked **against the inventory** — each delta page against its linked neighbours and thematically adjacent existing pages, not only delta pages among themselves.

**Full run ("thorough"):** only on request. The semantic checks also run over the whole inventory, then mandatorily via fan-out.

**Subagent fan-out:** For full runs and large deltas, distribute the checks across parallel subagents. Every subagent returns a structured findings list (file, line, finding, fix suggestion), not a prose summary. **Spot-check subagent tallies yourself** before they land in the report or in `log.md` — subagent counts can be wildly off (observed failure mode: a subagent reporting a small fraction of the real count).

**Scope honesty:** The report always names which mode ran and what was not checked (e.g. "semantic checks only over the delta since [date]"). A routine run never claims full coverage.

## Check Steps

Run all checks (scope per mode, see "Execution"), then report in a consolidated manner.

### 1. Broken Wikilinks

Scan all wiki pages for `[[wikilink]]`. For each link, verify the target page exists.

```bash
grep -roh '\[\[[^]]*\]\]' knowledge/wiki/ | sort -u
```

Match against actual files in `knowledge/wiki/`.

### 2. Orphan Pages

Find pages without incoming links — no other page references them via `[[wikilink]]`.

For each `.md` file in all wiki subfolders (see wiki folder set):
- Extract page name (filename without extension)
- Search all other wiki pages for `[[PageName]]`
- If no other page links to it — orphan

### 3. Contradictions

Read pages that share entities or concepts. Check for conflicting statements:
- Two source summaries make opposing claims about the same topic
- An entity page contains information contradicting a source summary
- Dates, numbers, or facts diverge between pages

### 4. Stale Claims

Cross-check source dates with wiki content:
- Concept page cites only old sources although newer ones exist on the same topic
- Entity information has not been updated although newer sources mention the entity

### 5. Missing Pages

Find `[[wikilinks]]` pointing to non-existent pages. Assess whether those topics deserve their own page.

### 6. Missing Cross-References

Find pages covering the same topic without linking to each other:
- Entity pages mention concepts without linking
- Concept pages mention entities without linking
- Source summaries cover the same topic without cross-referencing

### 7. Index Consistency

Check `knowledge/wiki/index.md`:
- Every page in all wiki subfolders (see wiki folder set) has an index entry
- **Dataview coverage counts as an index entry:** pages enumerated through Dataview code blocks count as covered (e.g. cluster pages via `cluster_tier` tier tables). Heuristic, if resolving the query is too expensive: if a cluster page with `cluster_tier` frontmatter exists AND `index.md` contains the string `cluster_tier`, all tier clusters count as covered. Distributor pages without `cluster_tier` need a direct link or a documented exception.
- No index entries point to deleted pages
- Entries are under the correct category

### 8. Unprocessed Sources (canonical detection procedure)

Single source for this check — `/knowledge-ingest` and CLAUDE.md reference it. **Never compare raw filenames literally against `log.md` text** (slug mismatch produces false-positive series and risks double-ingesting).

1. List all files in `knowledge/raw/` (excluding `assets/`).
2. A raw file counts as **processed** if its normalized basename appears in any wikilink target (`[[X]]`, `[[X|alias]]`) or `sources:` frontmatter entry across the **whole wiki** — not only in `sources/` pages: some raw files become `entities/` pages or are only referenced in a body.
3. **Normalization for the comparison:** lower-case; strip extensions (`.docx`, `.pdf`, `.md`, `.htm`, `.msg`, `.txt`, `.extracted`); strip all separator and special characters — including typographic apostrophes (`’` U+2019 vs `'`), quotation marks, brackets, dots, hyphens/underscores, spaces, em/en dashes (U+2014/U+2013), colons, and pipes. Treat path forms `knowledge/raw/X` and `raw/X` alike.
4. Track extraction artifacts (`.htm`, `.msg`, `.extracted.txt` duplicates) as their own category, not flagged as unprocessed.
5. **Counter-test before reporting:** for every supposedly unprocessed file, grep the whole wiki for significant parts of its name (false-negative sample).
6. Output the result as an ingest backlog; the ingest-vs-discard decision belongs to the user.

### 9. Knowledge Gaps

Based on current wiki coverage, suggest:
- Frequently mentioned topics without depth
- Questions the wiki would answer poorly
- Areas that should be filled by new sources

### 10. Structural Hygiene (readability & consistency)

Structural wiki-quality checks — all purely additive; none is fixed automatically.

**10.1 Long pages without H2 structure** → 🔵 BLUE
- For each `.md` file in all wiki subfolders (see wiki folder set):
  - Count lines. Count `^## ` / `^### ` headings.
  - If **lines > 90 AND headings < 2** → report.
- Fix suggestion: add an H2 outline. Typical for concepts: `## Definition` / `## Context` / `## Relationships` / `## Sources`. For entities: `## Overview` / `## Role` / `## Connections` / `## Sources`.

**10.2 Stub pages** → 🔵 BLUE
- Page < 20 lines (excluding frontmatter) with no clear reason to exist (e.g. redirect stub, placeholder with TODO).
- Fix suggestion: expand or merge into a larger concept page.

**10.3 Inconsistent wikilink spelling** → 🟡 YELLOW
- Per term, collect all variants that appear anywhere in the vault as `[[variant]]`.
- If several spellings exist for the same target (e.g. `[[Growth Marketing]]` AND `[[growth-marketing]]` both used although only one file is the target), report.
- Fix suggestion: normalize to the canonical spelling (usually the file slug).

**10.4 Tag term missing from body text** → 🟡 YELLOW
- For each frontmatter tag (e.g. `work/domain-a`): check whether the human-readable term appears anywhere in the page's body text.
- If the tag is present but the term is missing → report. The term should also appear in the text so a search finds it.

**10.5 Generic or too-short titles** → 🟡 YELLOW
- Check the frontmatter `title:` against a blacklist: `Methods`, `Overview`, `Basics`, `Concepts`, `Topics`, `Summary`, `Notes`, `Info`, `Details`, `Introduction` (extend with equivalents in the vault's primary language).
- Or title < 3 words and NOT simultaneously an entity name (proper name of a person/organization/product).
- Fix suggestion: a more precise title with a context term (e.g. "Methods" → "Methods of User Research").

**10.6 Language inconsistency within a page** → 🟡 YELLOW
- On pages written predominantly in the vault's primary language: check whether whole paragraphs in another language exist (not meant: individual English technical terms — those are allowed).
- Heuristic: classify paragraph by paragraph via function-word share per language. Flag only genuine block-level mixing.
- Fix suggestion: either translate the foreign-language paragraphs or switch the whole page (the latter is the exception).

**10.7 Cluster entry-block coverage** → 🔵 BLUE
- For each page in `knowledge/wiki/synthesis/` with `cluster_tier` frontmatter:
  - Read `concepts_covered` (an integer) and `cluster_scope` (a list) from the frontmatter.
  - Locate the block under the heading `## Entry points for requests`.
  - Extract every wikilink of the form `[[concepts/...]]` and `[[skills/...]]` in that block. Deduplicate.
  - **Coverage ratio** = unique wikilinks in the entry block ÷ `concepts_covered`.
- Report when:
  - Coverage ratio < 0.20 → entry block surfaces less than 20 % of the cluster's concepts → 🔵 BLUE.
  - The closing line `Topic unclear →` is missing → 🟡 YELLOW (every cluster needs a fallback target).
- **Name the data basis honestly:** if fewer than 3 query logs exist in `ops/context/query-log/`, the ≥3-logs aggregation cannot fire — then report a 🔵 BLUE "no data basis for sharpening aggregation (N logs present)" instead of silently reporting nothing.
- **Fix suggestion:** aggregate `sharpening_candidates` across query logs in `ops/context/query-log/` for this cluster — if ≥3 logs name the same `grep_only` concept, propose a new entry line in the format `"<situation>" → [[concepts/<name>]]`. Apply only on the user's confirmation (cluster pages are "Do not write casually").

**10.8 Missing core-statement head (readability)** → 🔵 BLUE
- For each `.md` file in `knowledge/wiki/{concepts,synthesis}/`:
  - Check whether a `> ` blockquote stands directly under the H1 as the first content line (before the first H2).
  - Pure epigraph quotes (author quote with attribution) or provenance notes (`> External source …`) do NOT count as a core statement.
- Report when the core-statement head is missing. Advisory only, never auto-fix.
- **Fix suggestion:** when the page is next touched, add a 1-3 sentence core statement as a `> ` blockquote under the H1 (see CLAUDE.md → Knowledge Operations → Ingest). No mass retrofit.

**10.9 log.md date monotonicity** → 🟡 YELLOW
- The `## [YYYY-MM-DD]` headers in `knowledge/wiki/log.md` must follow the insertion convention declared at the top of the file (newest-first). Report outliers, never auto-fix.
- Applies only to `log.md` — `ops/chronicle.md` belongs to the Operations Layer (mode separation).

**10.10 Cluster split candidate** → 🟡 YELLOW
- For each page in `knowledge/wiki/synthesis/` with `cluster_tier` frontmatter: check `concepts_covered` against the threshold. Distributor pages without `cluster_tier` are automatically exempt.
- **Threshold: `concepts_covered` > 100.** Tuning parameter of this skill — it lives here, not in CLAUDE.md, and may be adjusted without an architecture upgrade. Calibrate it just above your largest deliberately agreed-upon cluster, so the settled inventory does not fire immediately. Left unchecked, clusters can grow well past the point where their entry blocks stay navigable before anyone splits them reactively.
- Report as a split candidate, with a suggestion along which `cluster_scope` lines it could be divided. Never auto-fix — the split decision belongs to the user.

**10.11 Missing provenance markers** → 🔵 BLUE (sub-check C → 🟡 YELLOW)
- **Purpose:** verifies that pages carry the provenance-marker convention (`knowledge-ingest/SKILL.md` steps 3/4). Four markers: `[verified]` / `[claim]` / `[unsourced ⚠️]` / `[speculation]`. **The single source of the marker definition is knowledge-ingest step 3** — this check references it and does not duplicate the definition; it only uses the four marker strings as match targets.
- **Scope (deliberately narrower than the wiki folder set, like 10.8):** `knowledge/wiki/sources/` (key findings), `knowledge/wiki/concepts/` and `knowledge/wiki/synthesis/` (body factual claims). Other folders are not affected.
- The ingest rule applies provenance markers to all newly written or touched pages from the start, so **every page in the scope folders is in scope** — there is no legacy exemption. Like 10.8, the check is purely additive — never auto-fix, never a mass rewrite.

  **Sub-check A — source key findings (mechanical, high confidence):**
  - For each page in `sources/`, locate the block under `## Key Findings` (up to the next `## ` heading).
  - Every list line (`^\s*[-*]\s`) must **begin** with one of the four markers. Match pattern (because of the ⚠️ in the third marker, match on the prefix):
    ```bash
    grep -nE '^\s*[-*]\s+\[(verified|claim|unsourced|speculation)' <file>
    ```
  - List lines under `## Key Findings` **without** a leading marker → 🔵 BLUE (file + line).

  **Sub-check B — concept/synthesis body claims (heuristic, review candidate):**
  - A page in `concepts/` or `synthesis/` that carries a specific factual claim or number in its body (`\d+([.,]\d+)?\s*%`, currency `€|EUR|\$`, the word "percent", salient numeric values in claim context) but contains **not a single one** of the four markers anywhere on the page → report as a **review candidate**, **not** as a hard error.
  - **Conservative trigger (deliberate, against noise):** the condition is page-wide — a single existing marker suppresses B, because the page then counts as marker-aware. Consequence: a page with partly marked, partly unmarked body claims is **not** re-flagged by B. Stricter per-claim checking is intentionally out (it would drive up the false-positive rate); B is only the floor that catches entirely marker-less new pages with numeric claims.
  - Excluded from the body check: frontmatter, H1, the core-statement `> ` blockquote, all `## `/`### ` headings, pure wikilink lines.
  - **Name it honestly:** years, dates, version numbers, and list counters generate noise — hence review candidate with high false-positive tolerance, not an error claim. Pure definition or framing sentences without a factual claim need no marker and are not flagged.

  **Sub-check C — head purity (mechanical):**
  - If the core-statement `> ` blockquote (first content line under the H1) itself carries one of the four markers → 🟡 YELLOW. The head stays marker-free (ingest step 4: "the core-statement head itself stays marker-free").

- **Fix suggestion (never auto-fix):** add markers per ingest steps 3/4 when the page is next touched.

## Report

Grouped by severity:

### 🔴 Errors (must fix)
- Broken wikilinks
- Contradictions between pages
- Index entries pointing to non-existent pages

### 🟡 Warnings (should fix)
- Orphan pages without incoming links
- Stale claims from outdated sources
- Missing pages for frequently referenced topics
- Unprocessed sources in `knowledge/raw/`

### 🔵 Notes (nice to fix)
- Possible additional cross-references
- Knowledge gaps
- Index entries with better descriptions
- **Structural hygiene:** long pages without H2 outline (10.1), stub pages (10.2)
- **Cluster entry-block coverage < 20 %** (10.7)
- **Missing core-statement head** on concept/synthesis pages (10.8)
- **Missing provenance markers** on source key findings (10.11-A) and concept/synthesis body claims (10.11-B, review candidate)

### 🟡 Additional structural warnings (from Check 10)
- Inconsistent wikilink spelling (10.3)
- Tag term missing from body text (10.4)
- Generic or too-short titles (10.5)
- Language inconsistency within a page (10.6)
- Cluster without the `Topic unclear →` fallback line (10.7)
- log.md entries against the insertion convention (10.9)
- Cluster split candidate: `concepts_covered` above threshold (10.10)
- Provenance marker inside the core-statement head (head must stay marker-free) (10.11-C)

Per finding:
- **What:** Description
- **Where:** File(s) and line(s)
- **Fix:** Recommended action

## After the Report

> "Found: N errors, N warnings, N notes. Should I fix any of these?"

If confirmed, fix and report what was changed.

## Log the Lint Pass

Append to `knowledge/wiki/log.md` (newest-first, directly under the file header):

```
## [YYYY-MM-DD] lint | Health check (routine, delta since YYYY-MM-DD) or (thorough)
Found: N errors, N warnings, N notes. Fixed: [list of fixes]. Scope: [mode + what was not checked].
```

## When to Lint

- **Threshold (countable): ≥10 new source pages since the last lint** — catch fresh cross-reference gaps (routine run, delta scope). Counting method: files in `knowledge/wiki/sources/` with `created:` after the date of the last `lint |` entry in `log.md`. A typical full ingest wave produces 8-10 source pages — one to two waves cross the threshold. `/knowledge-ingest` checks it at the end of every run (step 12) and suggests the lint.
- **At least monthly** — stale claims and orphan pages accumulate over time (full run, "thorough")
- **Before major queries** — ensure wiki health (a routine run suffices)

## Stop — what this skill never does

- Never fix a finding automatically. All checks (including every 10.x hygiene check) are purely additive; fixes only after the user's confirmation to the question in "After the Report".
- Never compare raw filenames literally against `log.md` text. Detect unprocessed sources exclusively via the canonical procedure in Check 8 (slug mismatch produces false positives).
- Never decide on ingesting or discarding backlog sources. The skill only outputs the ingest backlog; the decision belongs to the user (Check 8, step 6).
- Never take subagent tallies into the report or `log.md` unverified; always spot-check the counts yourself (see "Execution", subagent fan-out).
- Never claim full coverage when only a routine run over the delta ran; the report names mode and check gaps (scope honesty).
- Never write to `knowledge/raw/` (CLAUDE.md Rule 1) and never touch wiki pages outside confirmed fixes and the log entry ("Do not write casually").

## Related Skills

- `/knowledge-ingest` — process new sources
- `/knowledge-query` — answer questions
