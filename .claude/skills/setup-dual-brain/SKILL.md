---
name: setup-dual-brain
description: >
  Interactive onboarding wizard for a FRESH Dual-Brain vault. Scaffolds the folder
  structure derived from the CLAUDE.md Architecture block, creates template files, and
  customizes the template CLAUDE.md with the user's name and domains. Use only when the
  user is standing up a new, empty vault ("set up the dual brain", "initialize this
  vault", "scaffold a fresh vault"). Do NOT trigger on everyday uses of "setup" or
  "initialize", and never on an established, customized vault — structural changes there
  go through /second-brain-upgrade.
allowed-tools: Bash Read Write Edit Glob Grep AskUserQuestion
---

# /setup-dual-brain — Onboarding Wizard

Interactive setup that scaffolds a complete Dual-Brain vault and personalizes it for the user.

## Overview

This wizard:
0. Guards against re-runs on an established vault (abort + gap report, no writes)
1. Asks for the user's name/alias, work domains, personal domains, and primary language
2. Creates the directory structure derived from the CLAUDE.md Architecture block
3. Generates empty template files (chronicle.md, index.md, glossary.md, log.md, overview.md)
4. Customizes the template CLAUDE.md with the user's name and domain taxonomy
5. Verifies the result against the Architecture block and reports the diff

## Step 0: Re-Run Guard — Detect an Established Vault

**Runs before everything else. No question, no write before this check passes.**

A blind re-run on a living vault is destructive: Step 4 would replace a grown domain taxonomy and customized CLAUDE.md sections with generic template text. Check two signals:

1. **CLAUDE.md customized?** If `CLAUDE.md` exists in the vault root, grep it for the Step 4b template line (search string: `configured during`). Placeholder absent → customized.
2. **Vault in use?** Glob `ops/**/*`. Any file present → in use.

If **either** signal fires, this is an established vault — **abort the wizard:**

- Skip Steps 1–4 entirely. Write nothing.
- Diff the existing structure against the CLAUDE.md Architecture block (derivation as in Step 2) and present only the **missing** directories/files as a proposal.
- Create missing elements only after an explicit OK from the user — and nothing beyond them.
- **Never** rewrite or replace CLAUDE.md sections that deviate from the template; those deviations are the customization. Structural changes to an established CLAUDE.md go through `/second-brain-upgrade`, not through this wizard.

Only when both signals are clean (template or absent CLAUDE.md, empty `ops/`) proceed to Step 1.

## Step 1: Gather User Information

Ask via `AskUserQuestion`, one question per item. Exact wording is free — these are the intents:

| Variable | Intent | Notes |
|---|---|---|
| `$USER_NAME` | Name or alias to address the user throughout the vault | slug: `$USER_NAME_SLUG` (kebab-case) |
| `$WORK_DOMAINS` | Work domains, comma-separated (e.g. engineering, sales, marketing) | each becomes a `work/<domain>` tag |
| `$PERSONAL_DOMAINS` | Personal domains, comma-separated (e.g. fitness, travel) | each becomes a `personal/<domain>` tag; may be empty |
| `$PRIMARY_LANGUAGE` | Language for wiki pages and operations notes | offer English / German / Spanish / French, allow custom; default English |

## Step 2: Scaffold Directory Structure

**Do not hardcode the directory list.** The single source for the vault structure is the fenced `text` code block under `## Architecture` in the vault root `CLAUDE.md` (guaranteed present — see Edge Cases). Derive the scaffold from it:

1. Read the Architecture block from `CLAUDE.md`.
2. Parse it: entries ending in `/` are directories (nesting = indentation), entries ending in `.md` are template files (handled in Step 3).
3. `mkdir -p` each directory that does not exist; skip existing ones. Record created vs. skipped for the Step 5 report.

This keeps the wizard in sync automatically when the Architecture block gains new elements — as happened when `knowledge/wiki/skills/`, `knowledge/wiki/glossary.md`, and `knowledge/wiki/overview.md` joined the architecture and an older hardcoded list never learned about them.

**Shipped with the template repo, not created here:** `.claude/hooks/`, `.claude/settings.json`, and `.claude/agents/` are part of the template repository itself. The wizard **verifies** they exist and flags them in the Step 5 report if missing (the user should re-clone or copy them from the template repo) — it does not create or overwrite them.

## Step 3: Create Template Files

Create every `.md` file the Architecture block lists, using the templates below. If the block lists an `.md` file with no template here, create it with an H1 title only and flag it in the Step 5 report.

### `ops/chronicle.md`

```markdown
# Chronicle

Operational audit trail. Log notable decisions, important completions, project status changes, promotions to knowledge, and cleanup events. Entries are ordered newest-first.

<!-- Insert entries at the top in this format:
## [YYYY-MM-DD] <operation> | <title>
- Details
-->
```

### `knowledge/wiki/index.md`

One `## <Section>` per `knowledge/wiki/` subdirectory found in the Architecture block (currently: Sources, Entities, Concepts, Skills, Synthesis), each carrying the placeholder comment:

```markdown
# Wiki Index

Master catalog and navigation page for the knowledge wiki.

## <Section — one per wiki subdirectory>
<!-- - [[Page-Name]] — one-liner description -->
```

### `knowledge/wiki/glossary.md`

```markdown
# Glossary

Synonym bridge between query phrasing and canonical wiki page names. First stop for retrieval, before grep and index.

Format: `- [[canonical-page]] — alias1, alias2, alias3`

<!-- Extend opportunistically during ingest and after failed queries. Include cross-language aliases where the vault language differs from source or technical terms. -->
```

### `knowledge/wiki/log.md`

```markdown
# Knowledge Log

Chronological operations log for the knowledge layer. Entries are ordered newest-first.

<!-- Insert entries at the top in this format:
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

Read the existing `CLAUDE.md` in the vault root. Apply the following customizations.

**Precondition (Step 0):** this step runs only on a template CLAUDE.md. Before each substep, verify its anchor still exists (4a: the generic name reference, 4b: the default language line, 4c: the generic domain taxonomy). Anchor missing → that section is customized: skip the substep, record it as skipped for the Step 5 report, leave the section untouched. Never replace CLAUDE.md content that deviates from the template — structural changes to an established CLAUDE.md go through `/second-brain-upgrade`.

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

## Step 5: Verify and Report

Do not copy a summary from this instruction file — **measure it**:

1. Glob the created structure and diff it against the Architecture block from Step 2.
2. Generate the report from that diff, grouped as:
   - **Created** — directories and files this run created
   - **Skipped** — already existed, left untouched
   - **Missing** — declared in the Architecture block but still absent (should be empty; if not, say so and offer to fix)
3. Verify the template-shipped infrastructure (`.claude/hooks/`, `.claude/settings.json`, `.claude/agents/`) exists; if any is missing, flag it with the advice to restore it from the template repo.
4. Add the CLAUDE.md customization summary (name, language, work/personal domains) — only for substeps actually executed; list skipped substeps explicitly.
5. Close with next steps: drop source material into `knowledge/raw/` and run `/knowledge-ingest`, capture tasks and projects with `/new`, generate the first daily plan with `/today`.

## Edge Cases

- **Vault already partially set up** — check each directory/file before creating. Skip what exists, create what is missing. Report what was skipped vs. created.
- **CLAUDE.md does not exist** — abort with a clear message; Step 2 derives the scaffold from its Architecture block, so the wizard cannot run without it. The user should clone or copy the template CLAUDE.md from the dual-brain repository first.
- **User provides no work domains** — use a single default `work/general` and note that they can customize later.
- **User provides no personal domains** — omit the personal section entirely.
- **Re-running setup** — NOT safe to re-run blindly: Step 4 would overwrite a grown domain taxonomy and customized CLAUDE.md sections with template text. Step 0 guards this — on an established vault (customized CLAUDE.md or non-empty `ops/`) the wizard aborts and only proposes missing structure elements, written solely after an explicit OK.

## Stop — what this skill never does

- Never writes before the re-run guard (Step 0) has passed: on an established vault (customized CLAUDE.md or non-empty `ops/`) the wizard aborts, proposes only missing structure elements, and creates them only after an explicit OK.
- Never overwrites or replaces CLAUDE.md sections that deviate from the template; the deviation is the customization. Structural changes to an established CLAUDE.md go through `/second-brain-upgrade`.
- Never deletes or overwrites existing directories and files; what exists is skipped and reported as "Skipped" in the Step 5 report.
- Never creates or overwrites `.claude/hooks/`, `.claude/settings.json`, or `.claude/agents/` — those ship with the template repo; the wizard only verifies their presence.
- Never hardcodes the directory list and never guesses a structure: if CLAUDE.md with its Architecture block is missing, the wizard aborts with a clear message.
- Never copies the success report from this instruction text; Step 5 measures via glob diff against the Architecture block.

## Done when

- Every directory and `.md` file declared in the CLAUDE.md Architecture block exists (measured via glob diff, not asserted).
- All template files carry their header content from Step 3; extra `.md` files without a template exist with an H1 and are flagged.
- CLAUDE.md customization (name, language, domains) is applied for every substep whose anchor was present; skipped substeps are listed explicitly.
- The Step 5 report groups Created / Skipped / Missing and includes the infrastructure verification result.
