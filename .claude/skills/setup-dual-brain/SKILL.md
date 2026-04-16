---
name: setup-dual-brain
description: >
  Interactive onboarding wizard for the Dual-Brain vault. Scaffolds the complete folder
  structure, creates template files, and customizes CLAUDE.md with the user's name and
  domains. Use when the user says "setup", "initialize", "onboard", "scaffold", or is
  starting with a fresh vault.
allowed-tools: Bash Read Write Edit Glob Grep AskUserQuestion
---

# /setup-dual-brain — Onboarding Wizard

Interactive setup that scaffolds a complete Dual-Brain vault and personalizes it for the user.

## Overview

This wizard:
1. Asks for the user's name/alias, work domains, and personal domains
2. Creates the full directory structure
3. Generates empty template files (chronicle.md, index.md, log.md, overview.md)
4. Customizes CLAUDE.md with the user's name and domain taxonomy
5. Confirms what was created

## Step 1: Gather User Information

Use `AskUserQuestion` for each piece of information.

### 1a. Name or Alias

```
Question: "What name or alias should I use to address you throughout the vault?"
Header: "Your Name"
```

Store the response as `$USER_NAME`.

### 1b. Work Domains

```
Question: "What are your work domains? These become tag categories (e.g., 'engineering', 'product-management', 'sales', 'marketing'). List as many as apply, separated by commas."
Header: "Work Domains"
```

Store as `$WORK_DOMAINS` (list). Each becomes a tag like `work/<domain>`.

### 1c. Personal Domains

```
Question: "What personal domains would you like to track? (e.g., 'fitness', 'photography', 'finance', 'travel', 'recipes'). Leave empty if none."
Header: "Personal Domains"
```

Store as `$PERSONAL_DOMAINS` (list). Each becomes a tag like `personal/<domain>`.

### 1d. Primary Language

```
Question: "What language should wiki pages and operations notes be written in?"
Header: "Language"
Options:
  - "English"
  - "German (Deutsch)"
  - "Spanish (Español)"
  - "French (Français)"
  (Other allows custom entry)
```

Store as `$PRIMARY_LANGUAGE`. Default: English.

## Step 2: Scaffold Directory Structure

Create all required directories. Check each before creating to avoid errors on existing vaults.

```
ops/
ops/inbox/
ops/projects/
ops/tasks/
ops/daily/
ops/weekly/
ops/people/
ops/context/

knowledge/
knowledge/raw/
knowledge/raw/assets/
knowledge/wiki/
knowledge/wiki/sources/
knowledge/wiki/entities/
knowledge/wiki/concepts/
knowledge/wiki/synthesis/

output/
archive/
```

Use `mkdir -p` for each path.

## Step 3: Create Template Files

### `ops/chronicle.md`

```markdown
# Chronicle

Operational audit trail. Log notable decisions, important completions, project status changes, promotions to knowledge, and cleanup events.

<!-- Append entries in this format:
## [YYYY-MM-DD] <operation> | <title>
- Details
-->
```

### `knowledge/wiki/index.md`

```markdown
# Wiki Index

Master catalog and navigation page for the knowledge wiki.

## Sources
<!-- - [[Page-Name]] — one-liner description -->

## Entities
<!-- - [[Page-Name]] — one-liner description -->

## Concepts
<!-- - [[Page-Name]] — one-liner description -->

## Synthesis
<!-- - [[Page-Name]] — one-liner description -->
```

### `knowledge/wiki/log.md`

```markdown
# Knowledge Log

Chronological operations log for the knowledge layer.

<!-- Append entries in this format:
## [YYYY-MM-DD] ingest | Source Title
- Source: knowledge/raw/.../filename.md
- Created: entities/xyz.md, concepts/abc.md
- Updated: concepts/def.md
- Tags: work/domain-a
-->
```

### `knowledge/wiki/overview.md`

```markdown
# Knowledge Overview

Running synthesis of the overall knowledge base. Update only when the big picture genuinely shifts.

<!-- This page is maintained by /knowledge-ingest and should reflect the current state of accumulated knowledge. -->
```

## Step 4: Customize CLAUDE.md

Read the existing `CLAUDE.md` in the vault root. Apply the following customizations:

### 4a. User Name

Find the placeholder or generic reference and replace with `$USER_NAME`:
- In the "Address" / naming section: set the user's preferred name
- In frontmatter examples: replace `"[[user-name]]"` with `"[[$USER_NAME_SLUG]]"` where `$USER_NAME_SLUG` is the kebab-case version

### 4b. Language

Find the Language section in CLAUDE.md. Replace the default line:

```
- **Wiki pages and operations notes:** Written in the user's primary language (configured during `/setup-dual-brain`). Default: English.
```

with:

```
- **Wiki pages and operations notes:** Written in $PRIMARY_LANGUAGE.
```

### 4c. Domain Taxonomy

Replace the generic domain taxonomy section with the user's actual domains:

```markdown
## Domain Taxonomy

Tags are hierarchical and can be combined. Mandatory for Knowledge Layer, optional for Operations Layer.

**Work:**
- `work/<domain-1>`
- `work/<domain-2>`
- ...

**Personal:**
- `personal/<domain-1>`
- `personal/<domain-2>`
- ...

Add new domains at any time — update this section accordingly.
```

### 4d. Validate

After editing, read CLAUDE.md back to verify the changes are correct and the file is not corrupted.

## Step 5: Confirmation Report

Present a summary to the user:

```
Dual-Brain vault setup complete!

**User:** $USER_NAME

**Directories created:**
- ops/ (inbox, projects, tasks, daily, weekly, people, context)
- knowledge/ (raw, raw/assets, wiki, wiki/sources, wiki/entities, wiki/concepts, wiki/synthesis)
- output/
- archive/

**Template files created:**
- ops/chronicle.md
- knowledge/wiki/index.md
- knowledge/wiki/log.md
- knowledge/wiki/overview.md

**CLAUDE.md customized with:**
- Name: $USER_NAME
- Language: $PRIMARY_LANGUAGE
- Work domains: $WORK_DOMAINS
- Personal domains: $PERSONAL_DOMAINS

**Next steps:**
1. Drop source material into `knowledge/raw/` and run `/knowledge-ingest`
2. Capture tasks and projects with `/new`
3. Generate your first daily plan with `/today`
```

## Edge Cases

- **Vault already partially set up** — check each directory/file before creating. Skip what exists, create what is missing. Report what was skipped vs. created.
- **CLAUDE.md does not exist** — report the error; the user should clone or copy the template CLAUDE.md from the dual-brain repository first.
- **User provides no work domains** — use a single default `work/general` and note that they can customize later.
- **User provides no personal domains** — omit the personal section entirely.
- **Re-running setup** — safe to re-run. Existing files are not overwritten (check before write). Only CLAUDE.md customization is applied.
