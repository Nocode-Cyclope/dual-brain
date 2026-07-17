---
name: council
description: >
  Expert council of five isolated Claude subagents for substantial decisions.
  Five roles (Skeptic, Philosopher, Visionary, Operator, Outsider) research
  independently, critique each other anonymously, a Chair renders the verdict.
  Use when the user says "/council", "convene the council", "ask the council",
  "council this", or wants a weighty question examined from multiple
  perspectives. NOT for everyday questions or yes/no follow-ups.
user-invocable: true
allowed-tools: Agent, Read, Grep, Glob, WebSearch, WebFetch, Write, AskUserQuestion
---

# /council — Expert Council

A council of five isolated Claude subagents deliberates a substantial question. Not a confirmation service.

## Scope Gate (first)

The council is heavy (around ten subagents plus research). Before convening, check:
- Is the question substantial (a decision with weight, trade-offs, ambiguity)? Then go.
- Is it a small matter, a yes/no question, or fishing for agreement? Then do NOT convene the council — answer briefly and directly, and say so.

## The Five Roles

Four run as `subagent_type: council-insider` (wiki + web), the Outsider as `subagent_type: council-outsider` (web only):

1. **Skeptic** (insider): Attacks assumptions. Looks for what goes wrong, what is being overlooked, where the question itself is posed wrongly.
2. **Philosopher** (insider): Goes to the deeper principles. What is the real topic behind the question, which values and goal conflicts sit underneath.
3. **Visionary** (insider): Thinks the possibilities big. Where could this lead, what would the ambitious path be, which opportunity is being underestimated.
4. **Operator** (insider): Focus on execution. Concrete steps, effort, gotchas, what actually has to happen on Monday morning.
5. **Outsider** (outsider): Deliberately without house knowledge. Brings external context, industry analogies, what outside observers would see immediately. Researches externally with particular thoroughness.

## Stage 1 — Independent First Answers

Start all five in parallel via the `Agent` tool in ONE message (so they run concurrently). Prompt per role:

```
Persona: <role name> — <role brief from the list above>.

Question before the council: <the user's question verbatim>

Task: Answer the question independently from your persona. Research within
your profile (wiki and/or web) before you judge. Support your core claims
(wikilinks for internal sources, URLs for external ones). Do not invent
numbers. Structure: your core position in 2-3 sentences, then the carrying
points with evidence, then your biggest open risk/doubt. Keep it focused.
```

Collect the five answers.

## Stage 2 — Anonymized Peer Review

Anonymize the five answers: remove role labels, relabel them "Answer A" through "Answer E" in random order. Then start all five roles again in parallel (same subagent types), prompt per role:

```
Persona: <role name> — <role brief>.

Here are five anonymized answers to the council question "<question>":
<Answer A ... E>

Task: Evaluate the CONTENT, not the presumed role. What is the strongest
insight across all five? What have all five missed in common (the council's
blind spot)? Where do the answers contradict each other on substance, and
who is more likely right? Cite evidence where needed. Short and sharp.
```

Collect the five critiques. Critique subagents research only lightly (they work over the delivered text); heavy fresh research is not needed here.

## Stage 3 — Chair Verdict (in the main context, not as a subagent)

You yourself are the Chair. Synthesize from the five first answers and the five critiques:
- **Verdict:** the council's defensible answer, including the tensions that remain open (do not smooth over contradictions).
- **The blind spot:** what the critique round brought to light that no member saw alone.
- **One concrete first step:** what the user does next, concrete enough for Monday morning.
- **Evidence:** the carrying sources as wikilinks and URLs.

The verdict is a substantive answer, so it carries the self-check footer per CLAUDE.md → Self-Check. No invented numbers (CLAUDE.md Rule 11). Cross-check contested claims before the verdict.

## Output

- The verdict appears in chat.
- Filing to `output/` ONLY on request. When the user says "save it": write to `output/YYYY-MM-DD-council-<slug>.md` with frontmatter (`type: deliverable`, `output_type: analysis`, `about: council verdict on <question>`, `created`, sources). No auto-write.
- **Chronicle for decision verdicts:** if the user makes a decision based on the verdict, a line belongs in `ops/chronicle.md` (format and insertion convention: top of the file, label `decision`) — analogous to the delegate rule, not left to chance.

## Dual-Brain Rules

- Reads Knowledge freely (through the insider agents), NEVER writes to `knowledge/wiki/`.
- Filing only to `output/`, and only on request. Promotion into the wiki stays explicit and manual.
- Single source: this skill is the authoritative definition of the council.

## Stop — what this skill never does

- Never writes to `output/` unprompted. Filing only when the user explicitly says "save it" — no auto-write.
- Never writes to `knowledge/` (CLAUDE.md Rule 3). Promotion into the wiki stays explicit and manual (Rule 4).
- Never passes role labels into the peer-review round. Stage 2 evaluates exclusively anonymized answers ("Answer A" through "Answer E") in random order.
- Never delegates the Chair verdict to a subagent. The synthesis runs in the main context.
- Never smooths over contradictions between the roles in the verdict. Open tensions remain visibly named.
- Never invents numbers, quotes, or sources (CLAUDE.md Rule 11). Cross-check contested claims before the verdict.

## Related Skills

- `/produce` — when a deliverable with knowledge retrieval is needed, without multi-perspective deliberation.
- `/delegate` — when a single sub-agent should work through a scoped task autonomously.
