---
name: knowledge-ingest
description: >
  Processes source documents from knowledge/raw/ into structured, interlinked wiki pages.
  Use when the user places new files in knowledge/raw/ and says "ingest this",
  "process this source", "I put something in raw/", or wants to incorporate new material
  into the knowledge base.
allowed-tools: Bash Read Write Edit Glob Grep
---

# Knowledge — Ingest

Processes raw sources into structured, interlinked wiki pages.

## Identifying Sources

1. If the user names a specific file or files, use those.
2. If they say "ingest new sources" or similar, detect unprocessed files:
   - List all files in `knowledge/raw/` (excluding `knowledge/raw/assets/`)
   - Read `knowledge/wiki/log.md`, extract all previously ingested source filenames from `ingest` entries
   - Any file in `knowledge/raw/` not found in the log is unprocessed
3. If nothing unprocessed is found, let the user know.

## Workflow per Source

### 1. Read the Source Completely

Read the entire file. Examine image references separately if they contain important information.

### 2. Discuss Key Points with the User

**Before writing**, share the 3-5 most important findings. Ask if they want to set priorities or skip any topics. Wait for confirmation.

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

- Finding 1
- Finding 2

## Mentioned Entities

- [[Entity-Name]] — brief context

## Covered Concepts

- [[Concept-Name]] — brief context
```

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

### 5. Set Wikilinks

Link every mention of an entity or concept that has its own page via `[[wikilink]]` — both from the new page to existing ones and vice versa.

### 6. Update `knowledge/wiki/index.md`

Add one entry per new page under the appropriate category:

```
- [[Page-Name]] — one-liner description (max 120 characters)
```

### 7. Append to `knowledge/wiki/log.md`

Append:

```
## [YYYY-MM-DD] ingest | Source Title
- Source: knowledge/raw/.../filename.md
- Created: entities/xyz.md, concepts/abc.md
- Updated: concepts/def.md
- Tags: work/domain-a
```

### 8. Review `knowledge/wiki/overview.md`

Only update if the new source genuinely shifts the overall picture.

### 9. Report

Tell the user:
- Created pages (with wikilinks)
- Updated pages (what changed)
- Newly identified entities and concepts
- Contradictions found

## Conventions

- Source summary pages are **purely factual**. Interpretation and synthesis belong in concept and synthesis pages.
- A single source typically touches **5-15 wiki pages** — ~10 is normal and desired. Do not compress out of caution.
- When new information contradicts existing wiki content: **update the wiki page and document the contradiction** citing both sources.
- **Prefer updating existing pages** over creating new ones. Only create a new page if the topic is sufficiently independent.
- `[[wikilinks]]` for all internal references. Never raw file paths.
- Use tags from the domain taxonomy defined in CLAUDE.md.

## What Comes Next

After ingesting, the user can:
- **Ask questions** with `/knowledge-query`
- **Ingest more sources**
- **Health-check** with `/knowledge-lint` after every ~10 ingests
