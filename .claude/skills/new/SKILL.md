---
name: new
description: >
  Quick Capture — classifies and files natural-language input into the Operations Layer.
  Use for capturing tasks, projects, people, ideas, inbox material, or context.
  Never write directly to knowledge/.
argument-hint: <what the user has in mind (projects, ideas, tasks, people)>
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion
---

# /new — Quick Capture

Creates items from natural language: `/new <input>`. Input is in `$ARGUMENTS`.

## Steps

1. **Decompose** — Extract all entities from the input (there can be multiple)
2. **Classify** each entity: `task | project | person | idea | inbox | context | daily`
3. **Extract structured data** (due dates, tags, names, organizations)
4. **Knowledge lookup** — for each recognized person, organization, and concept, check whether the Knowledge Layer has a wiki page (see "Knowledge Bridge" section below)
5. **Link** entities via frontmatter fields, body wikilinks, and knowledge bridge
6. **Write** files with correct frontmatter (see below)
7. **Respond** with a summary of what was created — including any found knowledge connections

## Decomposition

Parse the input for multiple entities. Example:

> "new project with Sarah about the Q3 product launch onboarding, need a FAQ page and brainstorm for training content"

Entities:
- Person: Sarah (if not already existing)
- Project: q3-product-launch-onboarding (linked to Sarah)
- Task: create FAQ page (linked to project)
- Task: brainstorm training content (linked to project)

## Classification

- Named person with context -> **person**
- Ongoing work, multiple steps -> **project**
- Concrete actionable item -> **task**
- Speculative, "what if" -> **idea**
- Raw unsorted input -> **inbox**
- Background information, no action needed -> **context**
- Daily plan entry -> **daily**
- **Confidence < 0.5** -> use `AskUserQuestion` to clarify, do not guess

**Edge Cases:**
- "Start/begin with X" -> **task** (the action of beginning), not project
- "I'm currently working on the strategy concept" -> **project** (ongoing)
- "Should I think about X" -> **idea**

## Missing Information

For a task without a due date, use `AskUserQuestion`:

```
Question: "When is this due?"
Header: "Due date"
Options:
  - "Today" -> today's date
  - "This week" -> Friday of this week
  - "Next week" -> Monday next week
  - (Other allows free input)
```

Same pattern for other ambiguous fields when classification is certain but core data is missing.

## Linking

- Obsidian wikilinks `[[slug]]` in the markdown body for connections
- For task -> project: update the project file with `[[task-slug]]`
- For project -> person: update the person file with `[[project-slug]]`
- Before creating: check if person/project already exists (`Glob` + `Grep`). If it exists, `Read` before `Edit`.

**Existing entities take precedence.** Do not create duplicates — update the existing file.

## Knowledge Bridge

For every **person**, **organization**, or **topic/concept** recognized from the input (e.g., "bid management", "storytelling", "partner-corp"):

1. **Lookup** in `knowledge/wiki/`:
   ```bash
   # People + Organizations
   ls knowledge/wiki/entities/ | grep -i "<name-slug>"
   # Concepts / Topics
   ls knowledge/wiki/concepts/ | grep -i "<topic-slug>"
   ```
2. **On match**, add the wikilink to the `knowledge:` frontmatter field of the new operations file (list). Example:
   ```yaml
   knowledge:
     - "[[knowledge/wiki/entities/john-doe]]"
     - "[[knowledge/wiki/entities/partner-corp]]"
     - "[[knowledge/wiki/concepts/ai-readiness-assessment]]"
   ```
3. **In the body**, insert the wikilink where the name first appears — Obsidian renders the connection visibly.
4. **In the response report**, briefly mention: "Knowledge bridge: John Doe exists as an entity in the wiki."

**Important:** Do not modify the knowledge page, only reference it. Backlinks are created automatically via Obsidian.

If no match exists but the person/topic is obviously "wiki-worthy" (e.g., important stakeholder, recurring concept), note it as a hint: "[[ops/people/<slug>]] does not have a knowledge entity yet. Should I flag it for promotion?"

## File Formats

Paths and frontmatter must be strictly followed — `type` is vault-wide unique (for Dataview queries).

### Task -> `ops/tasks/<slug>.md`

```yaml
---
type: task
status: pending
due: 2026-04-20            # optional
project: "[[project-slug]]" # optional, wikilink
tags: []
created: 2026-04-15
updated: 2026-04-15
---

Description of the task.
```

### Project -> `ops/projects/<slug>.md`

```yaml
---
type: project
status: active
owner: "[[user-name]]"      # optional
tags: []
created: 2026-04-15
updated: 2026-04-15
---

## Next Action
- [[task-slug]]

## Notes

## Stakeholders
- [[person-slug]]
```

### Person -> `ops/people/<slug>.md`

```yaml
---
type: person
last-contact: 2026-04-15
role: ...                     # optional
organization: "[[org-name]]"   # optional, wikilink
tags: []
created: 2026-04-15
updated: 2026-04-15
---

## Context
Who they are, relationship.

## Follow-ups
- [ ] Open items
```

### Idea -> `ops/inbox/<slug>.md`

```yaml
---
type: idea
captured: 2026-04-15
tags: []
---

Description of the idea.
```

### Inbox -> `ops/inbox/<slug>.md`

```yaml
---
type: inbox
captured: 2026-04-15
source: chat | email | call | manual
tags: []
---

Raw content.
```

### Context -> `ops/context/<slug>.md`

```yaml
---
type: context
created: 2026-04-15
updated: 2026-04-15
tags: []
---

Background information.
```

### Daily Entry -> append to existing `ops/daily/YYYY-MM-DD.md` or create via `/today`

## Response

Brief confirmation with wikilinks:

> Created: [[ops/projects/q3-product-launch-onboarding]] (project), [[ops/tasks/create-faq-page]] (task, due 2026-04-22), updated: [[ops/people/sarah-miller]] (last-contact today).

## Non-Negotiable

- **Never write directly to `knowledge/`.** Promotion is explicit (see CLAUDE.md).
- **Frontmatter is mandatory** — `type`, `created`, `updated` always.
