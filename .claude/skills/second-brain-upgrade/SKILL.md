---
name: second-brain-upgrade
description: >
  Activates on structural changes to the Second Brain — new skills, CLAUDE.md
  edits, retrieval logic, write permissions, promotion paths, frontmatter
  schemas, architecture refactors. Puts the Dual-Brain base principles (two
  layers, asymmetric relationship, explicit promotion) at the start of every
  upgrade thought. Use automatically when the user sends structural signals
  ("we should change the structure...", "CLAUDE.md needs...", "new skill...",
  "a learning for future upgrades..."). Do not trigger for pure content,
  capture, query, or lint work.
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion, WebFetch, Task
---

# Second Brain — Upgrade

Engages silently and automatically as soon as a user request changes the **structures, rules, mechanics, or taxonomies** of the Second Brain. Puts the base principles at the start of every upgrade thought, **before** a proposal is drafted.

> **Core statement:** A Second-Brain upgrade that does not respect the Dual-Brain asymmetry (Operations reads Knowledge freely; Knowledge accepts input only via explicit promotion) is not an upgrade — it is a breach.

---

## Part 0 — The Dual-Brain Base (top-level, always first)

**Conflict rule:** CLAUDE.md is always normative. Part 0 is an anchor against drift, not a second rule source — on divergence, CLAUDE.md wins and Part 0 gets updated to match.

- **Knowledge Layer = long-term memory:** a curated, interlinked wiki built from quality sources. Persistent, cumulative, ever-improving.
- **Operations Layer = working memory:** tasks, projects, daily plans, meeting notes, people, context. High-churn, action-oriented.
- **Asymmetric relationship (core invariant):** Operations reads from Knowledge freely and proactively. BUT: no auto-promotion, no silent bleed between layers.
- **Unidirectional automatic flow:** Knowledge → Operations. The reverse direction happens only through an explicit user decision.
- **Explicit promotion pathway:** `ops/ > output/ > knowledge/raw/ > knowledge/wiki/` — every step requires the user's consent.
- **Bridging mechanism:** the `knowledge:` frontmatter field.

**Consequence for every upgrade:**
- Whoever extends Ops must not accidentally open Knowledge write permissions.
- Whoever changes Knowledge retrieval must not soften the promotion rule.
- Whoever builds a new skill must clarify in which layer it writes and whether it reads from the other.

---

## Part 1 — Two Views (both must be served)

**User view:**
- Wants to give input and rely on **existing knowledge being used optimally**.
- Must **not need to know where anything lives**.
- Expects Claude to find and pull the right clusters/concepts/entities on its own.

**AI view (Claude):**
- Needs **structures that are findable** — a clear tag taxonomy, cluster entry blocks, glossary aliases.
- Needs **unambiguity instead of redundancy** — one place per rule, otherwise drift.
- Needs **explicit write permissions** per folder — so productions don't accidentally land in `knowledge/`.

**Pass/fail criterion:** to pass, one sentence per view must be formulable for every change:
- "The user gains X."
- "Claude gains Y."

No sentence possible → one-sided → sharpen the upgrade.

---

## Part 2 — Non-Negotiable Fixed Points (in addition to Part 0)

1. **Mode separation** — Operations Mode and Knowledge Mode stay separate. Upgrades do not blend them.
2. **CLAUDE.md is the single source of truth** for retrieval order, architecture rules, frontmatter standards. Skills reference it, they do not duplicate it.
3. **Language convention** — agent rules (CLAUDE.md, SKILL.md files) follow the existing pattern per file; wiki content and deliverables follow the vault's primary language; English technical terms stay in English; literal headings used as retrieval anchors (e.g. the cluster block `## Entry points for requests`) must not be reworded, because they are exact matches against existing pages.
4. **The Non-Negotiable Rules** in CLAUDE.md apply unchanged — an upgrade may make them more concrete, never weaker. Their count grows through escalations; always check against the current block, never against a counted snapshot.
5. **Fixed decisions get anchored, not framed as hypotheses.**

**Concrete failure patterns (from real upgrades, to be avoided):**

- **"If this proves itself"** phrasing for a decision already made → instead: "The decision is X. Anchoring:" — hedging an already-committed decision leads to repeated corrections.
- **Plan only emitted in chat** instead of **written** to a plan file → the plan file is the authoritative spec, chat is discussion.
- **Incomplete replacement** in plan files → always verify the target region with Read around edit operations; no trailing remnants of previous content.
- **Duplication of a rule across multiple skills** when it should be single-source in CLAUDE.md → reference, don't copy.

**Skill standard: guardrails for unattended runs.** Every skill that runs on a timer or event without the user carries, in addition to its Stop section, a block `## Guardrails (unattended run)` with three obligations: (a) hard run limits — exactly one pass, no open retries, subagent count named or zero; (b) uncertainty default "note instead of ask" — anything unclear lands as a note in the run's own report or in `ops/inbox/`, never as a follow-up question (which nobody answers at night) and never as an action on suspicion; (c) write radius enumerated exhaustively — which files the run may touch; everything else is off limits. Interactive skills do not need the block; if an existing skill is put on a timer, the block is a mandatory part of the conversion. Rationale: the silent costs of unattended loops (verification debt, comprehension rot, cognitive surrender, token blowout) accumulate without noise; guardrails convert an open risk into a bounded one. **A scheduled or unattended run may only report and propose — it never restructures the vault.**

**Skill standard: Stop section.** Every skill that acts (writes files, starts agents, changes state) carries — before its "Related skills" section, otherwise at the end of the file — a block with the literal heading `## Stop — what this skill never does`: 3–6 skill-specific action boundaries, concrete and checkable. Trigger boundaries ("when the skill does not fire") stay separate in the description and boundary sections — that is routing, not stop. Global CLAUDE.md rules are referenced by short pointer, never copied (Q2). Pure rulebook/style modules without their own execution are exempt. New skills get the section at build time; its existence is greppable and therefore lintable. Rationale: a skill that may one day run on a timer does everything its text says and nothing it omits — the Stop section is the place where intent over control is permanently fixed.

---

## Part 3 — Upgrade Checklist (Q0–Q5, a mini-substrate per question)

Every question has a **definition** (what is checked), a **decision rule** (how it is answered), and an **escalation** (when unclear). At the end the skill produces a visible result (see "Canonical Output").

### Q0 — Existing structures before new construction?

- **Definition:** Does an existing mechanism (skill, rule, convention, frontmatter field) already cover the need, or nearly?
- **Decision rule:** Build new only if (a) the closest existing mechanism is named along with why it is not enough, AND (b) a concrete present-day problem is solved, not a hypothetical future one ("in case we need it" = over-built).
- **Carve-out:** Applies only to structure (skills, rules, folders, schemas). Content volume is exempt — the recall rule (~10 wiki pages per dense source) stays untouched.
- **Escalation:** If it is contested which mechanism is closest → `AskUserQuestion` instead of parallel new construction.

### Q1 — Fixed or hypothesis?

- **Definition:** Has the user already made the directional decision of the upgrade?
- **Decision rule:**
  - **Fixed** = the user has stated the decision, in this or an earlier session, OR has approved a plan that commits the decision.
  - **Hypothesis** = the decision is currently under discussion, still open, or an exploratory question.
- **Escalation:** Unclear → ask via `AskUserQuestion`: "Is X already decided or are we still discussing?" — do not guess.
- **Consequence:** Fixed → anchor in committed language ("We are implementing: …"). Hypothesis → explore, show options, do not frame as committed.

### Q2 — One place or distributed?

- **Definition:** Does the new rule land in exactly one authoritative file, or is it stated in several?
- **Decision rule:**
  - **One place** = a single file (CLAUDE.md, one SKILL.md, one cluster page) contains the normative statement; every other location only links to it.
  - **Distributed** = the same rule is stated substantively in ≥2 files that could be edited independently.
- **Escalation:** If distribution is unavoidable (e.g. a short reminder in several skills makes sense): add an explicit reference line pointing to the single source, do not duplicate content.

### Q3 — Backward compatible?

- **Definition:** Do existing pages, tags, frontmatter fields, and skills keep working after the upgrade without migration?
- **Decision rule:**
  - **Yes** = no schema field is removed, no tag namespace changes meaning, no existing skill semantics break.
  - **No** = at least one of these changes.
- **Escalation:** On "No" → name a migration plan **before** implementation: affected files, order, rollback path.

### Q4 — Both views served?

- **Definition:** Does the upgrade help the user AND the AI (see Part 1)?
- **Decision rule:**
  - **Pass** = one sentence per view is formulable ("The user gains X.", "Claude gains Y.").
  - **Fail** = a sentence is missing or a placeholder.
- **Escalation:** Fail → sharpen the upgrade, do not ship it. Reduce scope if necessary until both sentences stand honestly.

### Q5 — Logging and verification?

- **Definition:** Is the change loggable and testable?
- **Decision rule:**
  - **Pass** = (a) a log location is named (`ops/chronicle.md` for Ops changes; `knowledge/wiki/log.md` if the wiki is touched — though wiki touches typically do not belong in upgrade flows), AND (b) an end-to-end smoke test is formulated (for a retrieval change, that means a real test query plus a regression pass).
- **Escalation:** No smoke test conceivable → warn. No log location fits → probably structural ambiguity, go back to Q2.

---

## Part 4 — Upgrade Workflow (every step with "done when")

1. **Trigger detection** — signal read from the user's message (see Auto-Trigger Substrate below). *Done when:* the substrate yields a clear TRIGGER or NO-TRIGGER; on UNCLEAR → `AskUserQuestion`.

2. **Reference the base principles internally** — walk through concretely before any proposal:
   - (a) asymmetric flow (Knowledge → Ops only)
   - (b) explicit promotion pathway
   - (c) the specific Non-Negotiable Rule (from the current block in CLAUDE.md) that applies to this upgrade — or state explicitly that none applies

   *Done when:* the three items (a)/(b)/(c) are named internally.

3. **Draft the proposal** in the language of Part 2 — fixed decisions not framed as hypotheses, both views addressed. *Done when:* the draft contains no hypothesis phrasing on fixed decisions and one sentence per view.

4. **Run the checklist** (Part 3, Q0–Q5). *Done when:* the Canonical Output (six-row table) stands.

5. **Clarify with the user** via `AskUserQuestion` for every open point raised by the checklist. *Done when:* all Q1/Q4 ambiguities are answered.

6. **Plan mode** for the actual change. The plan is **written into the plan file**, not only returned in chat. *Done when:* the plan file (e.g. `~/.claude/plans/<name>.md`) contains the complete plan; no trailing remnants of previous content.

7. **Implement** with `Edit` (when the file exists), `Write` only for genuinely new files. *Done when:* all planned edits are applied and verified with Read.

8. **Log** — `ops/chronicle.md` for operational changes. *Done when:* the chronicle entry exists with date, scope, and link.

9. **Verify** — run the end-to-end smoke test (from Q5). For retrieval, trigger, and routing changes, a fresh read-only subagent (`Task` tool) runs the test **cold** — without this session's author context; the main context compares result against expectation (self-grading by the author does not count as a test). For trigger changes, the convergence edge cases below serve as the regression set. *Done when:* the test result is documented; on failure, step back to step 7.

---

## Auto-Trigger Substrate

The skill activates silently (no explicit invocation needed), **including mid-conversation after a phase transition** (analogous to Continuous Routing Axis 2 in CLAUDE.md).

**Definition (TRIGGER):** A user message triggers the skill when its primary concern is to change the **structures, rules, mechanics, or taxonomies** of the Second Brain — not to **use or fill its contents**.

**Boundary (NO-TRIGGER):** Pure content work (writing, filling, answering), capture (filing notes), query (consulting knowledge), lint (checking the quality of the existing structure). Also NO-TRIGGER: escalating a lesson into an **existing** rule level (e.g. adding a rule to the existing CLAUDE.md rule block). TRIGGER only when an escalation creates a **new** level (e.g. first-time creation of a rules directory) or changes the structure itself.

**Decision rule on mixed signals:** Is the structural signal the **frame** of the request or only **context**?

- **Frame** ("we need a skill for X", "change the promotion path") → TRIGGER, the upgrade takes precedence.
- **Context** ("write a concept about our promotion path") → NO-TRIGGER, `/produce` applies; keep an upgrade bookmark in mind but do not actively start.

**Signal domains (TRIGGER, follows directly from the definition):** CLAUDE.md rules, skills (new or rewrite), retrieval logic (any change to HOW Claude searches or finds — mechanics changes are structure even when they sound purely technical, e.g. "run grep and cluster entry in parallel"), write permissions, promotion path, frontmatter schemas, folder types, architecture refactors, learning formulations with structural consequence.

**Convergence edge cases (with expected outcome — doubling as the regression set for trigger changes):**

| # | User message | Expectation |
|---|---|---|
| A | "We should rebuild retrieval so that grep and cluster entry run in parallel." | **TRIGGER** (retrieval mechanics are structure — "sounds merely technical" is the classic misclassification) |
| C | "Is Claude actually allowed to write into `knowledge/wiki/` now?" | **TRIGGER** (write permission, even when phrased as a question) |
| D | "Let's sharpen the strategy cluster — a new entry line for the trade-off question." | **NO-TRIGGER** (wiki content maintenance inside the existing mechanism; a `/knowledge-query` refinement, not an upgrade) |
| F | "A learning from our conversation today — we lose the base principles during upgrades." | **TRIGGER** (learning formulation leading to a structural intervention — exactly this skill) |

The unambiguous cases (a clear structural assignment → TRIGGER; a concept assignment, capture, or query → NO-TRIGGER) follow from the definition and decision rule and need no example list.

---

## Canonical Output — what the skill visibly produces

At the end of the checklist run (workflow step 4), the skill gives the user a **compact six-row table** — not a prose section. Format:

```markdown
### Upgrade check: <short title of the change>

| # | Question | Answer | Open clarification |
|---|---|---|---|
| Q0 | Existing before new? | New build needed because <closest mechanism> does not cover <reason> / existing suffices | — or a question for the user |
| Q1 | Fixed or hypothesis? | fixed / hypothesis | — or a question for the user |
| Q2 | One place or distributed? | one / distributed + location | — or a migration note |
| Q3 | Backward compatible? | yes / no | — or affected files |
| Q4 | Both views served? | The user gains X. Claude gains Y. | — or the missing view |
| Q5 | Logging & verification? | Log location + smoke test in one sentence | — |

**Proposal/result:** <1–2 sentences or transition to plan mode>
```

This table is the visible baton: it shows the user that the check really ran, and gives them a clear point to correct course before implementation begins.

---

## Edge Cases

- **The skill itself is an upgrade** — it should be maintained according to its own workflow. Every change to this file runs through the checklist (Q0–Q5) and is logged in `ops/chronicle.md`.
- **Creeping structural change** — when several small content edits cumulatively change a rule (e.g. three cluster refinements that in sum tip the retrieval behavior): on the third occurrence, treat it as an upgrade trigger, not as routine refinement.
- **No rule applies** — if workflow step 2(c) finds none of the Non-Negotiable Rules applicable, state it explicitly ("None of the rules directly affected — infrastructure only") and document it, instead of forcing a fitting rule.

---

## Stop — what this skill never does

- Never opens Knowledge write permissions or softens the promotion path: the asymmetry (Knowledge flows freely into Ops; the reverse only via explicit promotion) stays untouched in every upgrade (Part 0; CLAUDE.md Rules 3 and 4).
- Never implements before the Q0–Q5 checklist has visibly run (Canonical Output table) and open Q1/Q4 points are clarified with the user.
- Never emits the plan only in chat: the plan file is the authoritative spec, with no trailing remnants of previous content (Part 4, step 6).
- Never frames a fixed decision as a hypothesis ("if this proves itself" on an already-made decision is a documented failure pattern, Part 2).
- Never copies a rule into multiple files: the normative statement lives in exactly one place, everywhere else references it (Part 2, Q2).
- Never reports a retrieval, trigger, or routing change as verified via author self-check: the smoke test runs cold through a fresh read-only subagent (Part 4, step 9).
- Never restructures during a scheduled or unattended run: such a run only reports and proposes.

## Related Skills

- `/knowledge-query` — when only knowledge is sought, no structural change
- `/knowledge-ingest` — when new sources are processed (content, not upgrade)
- `/knowledge-lint` — when the quality of the existing structure is checked
- `/produce` — when a deliverable is written (even when its topic is structural)
- `/new` — when pure capture takes place
