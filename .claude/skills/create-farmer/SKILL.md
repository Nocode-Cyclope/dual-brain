---
name: create-farmer
description: Builds a new context farmer (sub-agent for external sources) or schedules an existing one. Checks what already exists first, then asks.
user-invocable: true
---

# /create-farmer — Farmer Manager

Manages context farmers: build, list, schedule.

> **Note:** Farmers require corresponding MCP connectors or local data sources. Activatable once the user makes sources available (e.g., Slack MCP, Gmail MCP, local RSS).

## First Step

Check inventory before asking the user:

1. **Scan existing farmers**: `Glob` on `.claude/agents/*-farmer.md`
2. **Check scheduled triggers**: If `/schedule` skill is available, call it with action `list`
3. **Show status**: Which farmers exist, which are scheduled
4. **Ask**: Build a new farmer or schedule an existing one?

## Building a New Farmer

### 1. Source and MCP

Ask the user which source should be farmed (e.g., "Slack #product-launch", "RSS feeds on AI news", "Outlook inbox"). Then check whether a matching MCP server is already connected (via `mcp__mcp-registry__search_mcp_registry`). If not: `mcp__mcp-registry__suggest_connectors` for suggestions.

### 2. Try the Connector

Discover available tools for the source. Test 1-2 read-only tools to understand the connection and data shape.

### 3. Gather Details

What should be monitored:
- Channels / senders / calendars / feeds / URLs
- Keywords or filters
- Classification rules beyond the vault defaults

### 4. Create the Sub-Agent

Create `.claude/agents/<name>-farmer.md`.

**Frontmatter:**

```yaml
---
name: <name>-farmer
description: Farms context from <source> into the Operations Layer
model: sonnet
permissionMode: acceptEdits
---
```

**Rules:**
- No `tools` field — MCP tools are inherited from the parent
- No `mcpServers` field
- Always `permissionMode: acceptEdits`
- Name must end with `-farmer`
- Body is the complete system prompt — no CLAUDE.md context, no parent context

**Body must contain:**

1. **Process** — Discover tools (by service name), use generic tool references. Then: read config, check state, read source (max 24h back), classify, deduplicate, write, update state.
2. **Classification rules** — How source data maps to vault types (`task`, `project`, `person`, `inbox`, `context`). **Never write to `knowledge/`.**
3. **Filing rule** — all outputs go to `ops/inbox/` or, when classification is clear, `ops/people/` / `ops/context/`. Frontmatter with `source: farmer/<name>`, `farmed: <timestamp>`.
4. **Useful MCP tools** — Table `| Tool | Purpose |` with plain tool names. Only read/search/list — no write/send/delete.
5. **Guidelines** — Signal-to-noise ratio, naming conventions, source attribution.

### 5. Whitelist Read-Only MCP Tools

Add the farmer's read-only MCP tools to `.claude/settings.local.json` under `permissions.allow`. **Never add write/send/delete tools there.**

### 6. Create Watchlist

Add a section in `ops/context/watchlists.md` for the new source (filters, channels, keywords).

### 7. Offer Scheduling

After the build, ask whether the user wants to schedule the farmer.

## Scheduling an Existing Farmer

Scheduling depends on what tools are available in the user's environment:

- **Claude Code scheduled tasks**: If `mcp__scheduled-tasks__create_scheduled_task` is available, create a scheduled task with prompt `/farm <name>` and the desired cron expression.
- **CronCreate**: If the `CronCreate` tool is available in the session, use it for session-scoped recurring runs (e.g., every 30 minutes).
- **Manual**: `/farm <name>` on demand. Always works, no setup needed.

Important details for any scheduling method:
- **Frequency**: daily (recommended for most sources), weekdays, hourly
- **MCP connector**: must be available when the farmer runs

## Related Skills

- `/farm` — trigger a farmer manually
- `/new` — manual capture as fallback
