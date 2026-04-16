---
name: knowledge-lint
description: >
  Health check of the wiki for contradictions, orphan pages, stale claims, missing
  cross-references, and unprocessed sources. Use when the user says "audit",
  "health check", "lint", "find problems", or wants to improve wiki quality.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Knowledge — Lint

Health check of the wiki. Report with actionable fixes.

## Check Steps

Run all checks, then report in a consolidated manner.

### 1. Broken Wikilinks

Scan all wiki pages for `[[wikilink]]`. For each link, verify the target page exists.

```bash
grep -roh '\[\[[^]]*\]\]' knowledge/wiki/ | sort -u
```

Match against actual files in `knowledge/wiki/`.

### 2. Orphan Pages

Find pages without incoming links — no other page references them via `[[wikilink]]`.

For each `.md` file in `knowledge/wiki/{sources,entities,concepts,synthesis}/`:
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
- Every page in `sources/`, `entities/`, `concepts/`, `synthesis/` has an index entry
- No index entries point to deleted pages
- Entries are under the correct category

### 8. Unprocessed Sources

Compare `knowledge/raw/` with `knowledge/wiki/log.md`:
- List all files in `knowledge/raw/` (excluding `assets/`)
- Extract all ingested source filenames from `log.md`
- Difference = not yet ingested sources
- Output the list so the user can schedule them for `/knowledge-ingest`

### 9. Knowledge Gaps

Based on current wiki coverage, suggest:
- Frequently mentioned topics without depth
- Questions the wiki would answer poorly
- Areas that should be filled by new sources

## Report

Grouped by severity:

### Red — Errors (must fix)
- Broken wikilinks
- Contradictions between pages
- Index entries pointing to non-existent pages

### Yellow — Warnings (should fix)
- Orphan pages without incoming links
- Stale claims from outdated sources
- Missing pages for frequently referenced topics
- Unprocessed sources in `knowledge/raw/`

### Blue — Notes (nice to fix)
- Possible additional cross-references
- Knowledge gaps
- Index entries with better descriptions

Per finding:
- **What:** Description
- **Where:** File(s) and line(s)
- **Fix:** Recommended action

## After the Report

> "Found: N errors, N warnings, N notes. Should I fix any of these?"

If confirmed, fix and report what was changed.

## Log the Lint Pass

Append to `knowledge/wiki/log.md`:

```
## [YYYY-MM-DD] lint | Health Check
Found: N errors, N warnings, N notes. Fixed: [list of fixes].
```

## When to Lint

- **After every 10 ingests** — catch fresh cross-reference gaps
- **At least monthly** — stale claims and orphan pages accumulate over time
- **Before major queries** — ensure wiki health

## Related Skills

- `/knowledge-ingest` — process new sources
- `/knowledge-query` — answer questions
