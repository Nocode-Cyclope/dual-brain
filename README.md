[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Dual Brain

**Your second brain is half a brain. This adds the other half.**

---

## The Problem

I built a second brain. 350 wiki entries. Structured, interlinked, steadily growing. I followed the [Karpathy approach](https://x.com/karpathy/status/1871554790498951368): curated sources in, LLM-maintained wiki out. The collection part worked beautifully.

Then Monday morning hits. You are planning your week, prepping a pitch, drafting an email to a stakeholder. And your wiki just sits there. You *know* you wrote something about this six weeks ago. You *know* there is a framework that fits. But the gap between "I stored this somewhere" and "it shapes my work right now" is wider than you think.

The second brain had long-term memory but no working memory.

## The Idea

Your brain does not have one memory. It has two. **Long-term memory** stores what you know. **Working memory** handles what you are doing right now. They work together: working memory constantly pulls from long-term memory. And occasionally, something from your daily work is important enough to commit to long-term storage.

Dual Brain mirrors this in a single Obsidian vault:

**Knowledge Layer.** Your long-term memory. A curated, interlinked wiki built from quality sources. Persistent, cumulative, ever-improving.

**Operations Layer.** Your working memory. Tasks, projects, daily plans, meeting notes, people, context. High-churn, action-oriented.

The key mechanic: **Operations reads from Knowledge freely and proactively.** When you draft a concept for a client, the system pulls in relevant frameworks, past analyses, and entity context from your wiki. Without you having to remember where you put them.

The reverse direction is deliberately manual. You decide when something from your daily work is good enough to become permanent knowledge. No auto-promotion. No silent bleed between layers.

## Architecture

```
ops/                          # Working memory
  chronicle.md                #   Operational audit trail
  inbox/                      #   Unsorted incoming material
  projects/                   #   Active projects and next actions
  tasks/                      #   Trackable work items
  daily/                      #   Daily plans and reviews
  weekly/                     #   Weekly summaries
  people/                     #   Stakeholders, contacts, follow-ups
  context/                    #   Reference material for current work

knowledge/                    # Long-term memory
  raw/                        #   Curated source documents (read-only)
  wiki/
    sources/                  #   One summary per ingested source
    entities/                 #   People, orgs, products, tools
    concepts/                 #   Ideas, methods, frameworks
    synthesis/                #   Cross-source analyses
    index.md                  #   Master catalog
    log.md                    #   Operation log

output/                       # Shared: deliverables, drafts, polished artifacts
archive/                      # Cold storage
```

### How Information Flows

```mermaid
flowchart LR
    subgraph ops ["Operations Layer"]
        inbox["ops/inbox/"]
        active["ops/projects/ tasks/ daily/"]
    end

    subgraph out ["Shared Output"]
        output["output/"]
    end

    subgraph knowledge ["Knowledge Layer"]
        raw["knowledge/raw/"]
        wiki["knowledge/wiki/"]
    end

    inbox -->|classify and file| active
    active -->|produce| output
    output -->|explicit promote| raw
    raw -->|ingest| wiki
    wiki -.->|reads from| active

    style ops fill:#1a1a2e,stroke:#e94560,color:#fff
    style knowledge fill:#1a1a2e,stroke:#0f3460,color:#fff
    style out fill:#1a1a2e,stroke:#16213e,color:#fff
```

The dotted line is the whole point. Knowledge flows into daily work automatically. The solid lines require your say-so.

## What Makes This Different

**Continuous Routing.** The system does not wait for you to invoke a skill. Every message you send is evaluated: Is this a new task? Does it belong to an existing project? What does the wiki know about this topic? This runs in the background on every interaction, not just when you type a slash command.

**Cross-layer bridge.** A `knowledge:` frontmatter field in any operations file links it to relevant wiki pages. Obsidian backlinks make these connections visible in both directions. When you open a wiki page about "Bid Management," you see every project and task that drew from it.

**Knowledge-powered production.** `/produce` drafts memos, pitches, concepts, and analyses by actively pulling in two types of knowledge: methodological (how to write well, how to structure an argument) and specific (what you wrote about this topic before, what your wiki says about the people involved). Your 350 entries finally do something.

**Explicit promotion.** Nothing moves from operations to knowledge automatically. The path is always: `ops/ > output/ > knowledge/raw/ > knowledge/wiki/`. Every step requires your decision. This keeps the wiki clean and the operations layer disposable.

## Getting Started

**You need:** [Obsidian](https://obsidian.md/) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code) pointed at your vault directory.

1. **Clone into your vault directory**
   ```bash
   git clone https://github.com/Nocode-Cyclope/dual-brain.git my-vault
   cd my-vault
   ```

2. **Open in Obsidian** and start a Claude Code session in the same directory.

3. **Run the setup**
   ```
   /setup-dual-brain
   ```
   This asks for your name and domains, scaffolds the folder structure, and tailors the `CLAUDE.md` to your setup.

4. **Start working.**
   - `/new meeting with Sarah about the Q3 launch` captures, classifies, and files it
   - `/today` builds your daily plan from due tasks and active projects
   - `/knowledge-ingest` processes a source document into linked wiki pages
   - `/produce concept for the Q3 launch strategy` writes a deliverable backed by your wiki

The system builds itself as you use it. Capture into Operations, ingest into Knowledge, and the connections grow naturally.

## Skills

### Knowledge Layer

| Skill | What it does |
|---|---|
| `/knowledge-ingest` | Processes source documents from `knowledge/raw/` into structured, interlinked wiki pages. Discusses key takeaways before writing. |
| `/knowledge-query` | Answers questions from the wiki. Cites sources. Offers to save valuable answers as synthesis pages. |
| `/knowledge-lint` | Finds broken links, orphan pages, contradictions, stale claims, and unprocessed sources. Reports by severity. |

### Operations Layer

| Skill | What it does |
|---|---|
| `/new` | Quick capture. Classifies input as task, project, person, idea, or context. Checks for existing projects before creating new ones. Bridges to wiki entities. |
| `/today` | Generates a daily plan from due tasks, active projects, and a knowledge briefing section with relevant wiki context. |
| `/daily-review` | End-of-day review. Compares plan vs. reality, updates task statuses, logs observations. |
| `/weekly-review` | Weekly summary. Identifies promotion candidates for the knowledge layer. |
| `/produce` | Creates deliverables with active knowledge support. Pulls in methodological frameworks and specific prior work from the wiki. |
| `/delegate` | Hands off a task to a sub-agent. Includes automatic knowledge discovery before the agent starts. |
| `/history` | Shows recent vault activity from chronicle and wiki log. |
| `/farm` | Triggers a context farmer to pull external sources into `ops/inbox/`. |
| `/create-farmer` | Builds or schedules a context farmer for an external source (Slack, RSS, email). |

### Setup

| Skill | What it does |
|---|---|
| `/setup-dual-brain` | Interactive onboarding. Scaffolds the vault, configures domains, tailors CLAUDE.md. |

## Recommended Tools

None of these are required. All of them make the system better as your vault grows.

### CLI Tools

| Tool | What it does | When it matters |
|---|---|---|
| [qmd](https://github.com/tobi/qmd) | Local search engine for markdown files with hybrid BM25/vector search | Once your wiki passes ~100 pages, index scanning gets slow. `qmd` makes `/knowledge-query` fast again. Install: `npm i -g @tobilu/qmd` |
| [summarize](https://github.com/steipete/summarize) | Summarizes links, files, and media from the CLI | Speeds up source preparation before dropping files into `knowledge/raw/`. Install: `npm i -g @steipete/summarize` |
| [agent-browser](https://github.com/vercel-labs/agent-browser) | Browser automation CLI for AI agents | Useful for `/delegate` tasks that involve gathering information from the web. Install: `npm i -g agent-browser` |

### Obsidian Plugins

| Plugin | What it does | Why it matters here |
|---|---|---|
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) | Query frontmatter across all files | The `type:` field is vault-wide by design. Queries like `TABLE due, status WHERE type = "task" AND status = "pending"` work across both layers. This is the plugin that turns frontmatter from metadata into an interface. |
| [Templater](https://github.com/SilentVoid13/Templater) | Template engine for new files | Pairs well with `/new` for consistent frontmatter when you create files manually in Obsidian. |
| [Calendar](https://github.com/liamcain/obsidian-calendar-plugin) | Calendar view for daily notes | Makes `ops/daily/` navigable. Click a date, see the plan. |

## Standing on Shoulders

This project builds directly on the work of others:

- **Andrej Karpathy** published the [original idea](https://x.com/karpathy/status/1871554790498951368) and the [reference implementation](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) for LLM-maintained knowledge bases. The insight that an LLM can be your librarian, not just your search engine, started everything.
- **Nicholas Spisak** built [second-brain](https://github.com/NicholasSpisak/second-brain): the wiki architecture and knowledge operations (ingest, query, lint). The Knowledge Layer stands on this foundation.
- **Brad** built [second-brain](https://github.com/bradautomates/second-brain): the operations layer and active second brain patterns (capture, classify, daily review). The Operations Layer adapts these ideas.
- **Claude Code** by Anthropic was the development partner for the entire implementation. Every skill, every workflow, every line of `CLAUDE.md` was built in collaboration.

## License

[MIT](LICENSE)

## Contributing

PRs are welcome. If you have found a way to make the two layers talk to each other better, or you have built a skill that fills a gap, open an issue or a PR.

The architecture is intentionally opinionated: two layers, explicit promotion, no auto-mixing. But there is room to improve individual skills, add new farmers, or refine the workflows.
