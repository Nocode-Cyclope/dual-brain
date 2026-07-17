---
name: farm
description: Manually triggers a context farmer sub-agent that pulls data from external sources (e.g., Slack, RSS, email) into ops/inbox/. Usage - /farm <name>
user-invocable: true
---

# /farm — Trigger Context Farmer

Starts a farmer sub-agent that pulls data from an external source into the vault.

> **Note:** Farmers require corresponding MCP connectors (Slack, Gmail, Calendar, etc.) or local data sources (RSS, filesystem). Only becomes fully active once the user makes connectors or sources available. `/create-farmer` builds new farmers.

## Argument

`$ARGUMENTS` is the farmer name (e.g., `slack`, `rss`, `mail`).

## Workflow

1. **Validate argument**: If `$ARGUMENTS` is empty, list available farmers via `Glob` on `.claude/agents/*-farmer.md` and ask the user which one.

2. **Check farmer existence**: Does `.claude/agents/$ARGUMENTS-farmer.md` exist? If not, list available ones and report the error.

3. **Execute farmer**: Start a sub-agent via the `Agent` tool:
   - Agent name: `$ARGUMENTS-farmer`
   - Prompt: "Execute your farming instructions now."

4. **Report results**: After the farmer run, summarize for the user:
   - Number of new files in `ops/inbox/`
   - Number of updated files (e.g., `ops/people/`)
   - List of entities with type (task / project / person / inbox / context)
   - Any problems encountered

## Filing Rule

Farmers **always write to `ops/inbox/`** (or `ops/people/`, `ops/context/` when classification is clear). **Never directly to `knowledge/`.** Valuable material goes through the explicit promotion workflow.

Farmer-generated files carry in their frontmatter:
```yaml
source: farmer/<name>
farmed: 2025-01-15T14:32:00
```

## Done when

- The farmer sub-agent ran (or a clear error was reported when the farmer file does not exist).
- The report states counts of new and updated files and lists the created entities with their types.
- All farmer-created files landed inside `ops/` and carry `source: farmer/<name>` and `farmed:` frontmatter.
- Any problems from the farmer run are surfaced to the user, not swallowed.

## Stop — what this skill never does

- Never start a farmer whose file `.claude/agents/<name>-farmer.md` does not exist; instead, list available farmers and report the error (step 2).
- Never fetch external sources itself or write farming results itself; this skill validates, starts the sub-agent, and reports — the farmer does the writing.
- Never create new farmers or modify existing farmer files; that is what `/create-farmer` is for.
- Never write to `knowledge/` or let anything write there (Filing Rule, CLAUDE.md Rule 3); farmer output lands in `ops/inbox/`, or in `ops/people/` / `ops/context/` when classification is clear.
- Never promote farmer material into the Knowledge Layer automatically (CLAUDE.md Rule 4); valuable material goes exclusively through the explicit promotion workflow.

## Related Skills

- `/create-farmer` — build a new farmer or schedule an existing one
- `/new` — manual capture when no farmer exists for the source
