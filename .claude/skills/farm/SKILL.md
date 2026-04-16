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
farmed: 2026-04-15T14:32:00
```

## Related Skills

- `/create-farmer` — build a new farmer or schedule an existing one
- `/new` — manual capture when no farmer exists for the source
