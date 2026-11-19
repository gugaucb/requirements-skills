---
name: ask-req
description: Ask which requirements skill or flow fits your situation. A router over every skill in this repo, aware of the current state of your artifacts.
disable-model-invocation: true
---

# Ask Req

You do not remember every skill, so ask.

Before stating what a skill does or recommending a step be skipped, read that skill's SKILL.md: the summaries here are for orientation only.

A **flow** is a path through the skills. Most work travels one **main flow**; on-ramps merge onto it; the rest is standalone or a vocabulary layer underneath. Each skill ends with a suggested **next step**, so after the first skill you can simply follow the suggestions.

## Read the state first

Do not ask the user what they already have. Look at the artifact root (see `docs/agents/requirements-workflow.md`) and route by what you find:

| You find | Recommend |
| --- | --- |
| No `docs/agents/` config | `/setup-requirements-repo` |
| No `PRODUCT-VISION.md`, idea is small enough to say in a page | `/grill-with-docs`, then `/create-product-vision` |
| No vision, idea is huge or foggy | `/wayfinder` |
| Vision Draft | `review-product-vision`, then PO approval recorded as a DEC |
| Approved vision, no spec for the capability | `/to-spec` |
| Spec, no sliced backlog | `/split-backlog` |
| Backlog with unblocked stories | `/refine-request US-NNN` (frontier first) |
| Any item `Stale`, or an open `CHG` | `/refine-request` on each, blockers first |
| Stories Ready for human review | PO review; then publish or hand to the team |
| Raw requests waiting | `/triage` |
| A change to an existing story or capability | the change flow below |

Report what you found in two lines, then recommend one next step.

If `docs/agents/graph.md` exists, ask the graph instead of scanning files: invoke the `graph-sync` skill, then `req-graph.py frontier <artifact-root>` (stories ready to refine) and `req-graph.py stale <artifact-root>` (stories to re-refine). Without a graph, read `BACKLOG.md` and the story statuses.

## The main flow: idea to ready requirements

1. **`/setup-requirements-repo`** once per repo.
2. **Vision.** **`/grill-with-docs`** sharpens the PO's idea and records `GLOSSARY.md` and `DECISIONS.md` as it goes. **`/create-product-vision`** writes `PRODUCT-VISION.md` with `GOAL-` and `CAP-` IDs; the `review-product-vision` skill checks it. The PO approves (recorded as a DEC). Humans approve; skills recommend.
3. **Spec.** **`/to-spec`** synthesises the conversation into `SPEC-NNN`: problem, outcome, candidate stories, rules, out of scope. No interview.
4. **Slice.** **`/split-backlog`** cuts the spec into thin vertical stories with **blocking edges**, quizzes you, and records `BACKLOG.md` (or publishes to the tracker on your say-so).
5. **Refine, one story at a time.** **`/refine-request US-NNN`** drives the model-invoked skills as needed: `write-user-story`, `specify-requirements`, `define-acceptance-criteria`, `design-test-scenarios`, `diagram-requirements`, then `audit-traceability` and `review-readiness`. Run it on each frontier story in a **fresh context**; the artifacts are the memory.
6. **Approve.** The PO reviews stories Ready for human review and records approval. `Ready (team agreement)` needs that recorded human confirmation.
7. **`/retro`** closes the loop: it suggests improvements to the requirements environment, not to the requirements.

### Context hygiene

Keep steps 2 to 4 in **one unbroken context** so the grilling, spec and backlog build on the same reasoning. Clear between stories in step 5. See [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered decision at each boundary (continue, clear, handoff, sub-agent, compact).

## The change flow: altering an existing story

When a story, capability, goal, decision or glossary term **changes**, the cost is downstream. Do not edit first.

1. **`/grill-with-docs`** (or `/grill-me` if stateless) on the change. In **change mode** the interview ends with an **impact round**: the `impact-analysis` skill walks downstream (FR, AC, TC), upstream (CAP, GOAL, vision) and sideways (siblings sharing the term or rule), and classifies each item Invalidated, Needs review or Unaffected (checked).
2. The report is stored as `changes/CHG-NNN.md`; impacted items become `Stale`.
3. **`/refine-request`** on each Stale story, blockers first. Then `audit-traceability` confirms the CHG is closed.

`write-user-story`, `specify-requirements`, `define-acceptance-criteria` and `design-test-scenarios` also invoke `impact-analysis` before editing existing items, so the guard holds even when you skip the grilling.

## On-ramps

- **Raw requests piling up, or a change request arriving** → **`/triage`**. Moves items through roles (`needs-triage`, `needs-info`, `ready-for-refinement`, `ready-for-po`, `out-of-scope`), checks impact for changes, writes a refinement-ready brief, and merges onto the main flow at `/to-spec`, `/split-backlog` or `/refine-request`. Do not triage what `/split-backlog` produced.
- **A huge, foggy effort: a whole product, a regulation, a new business line** → **`/wayfinder`**, the most demanding flow. It charts a **shared map** of **decision tickets** (research, sketch, grilling, ask, task) and resolves them one at a time: **decisions, not deliverables**. When the map clears it **hands off, it does not specify**: to `/create-product-vision` or `/to-spec`.
- **The knowledge sits with someone else** → **`/to-questionnaire`**. It interviews you about the _send_ and writes the stakeholder a questionnaire. Answers return to `/grill-with-docs`, `/to-spec` or a wayfinder ticket.
- **A fact outside the repo** (law, contract, existing system) → the `research` skill, run in a background agent, leaves a cited file.

## Standalone

- **`/grill-me`**: the same relentless interview, **stateless**: it saves nothing. Use it when there is no repo under the idea. In a repo, `/grill-with-docs` leaves a paper trail and is strictly better.
- The **`grilling`** skill is the interview primitive: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-me`, `/grill-with-docs`, `/triage`, `/wayfinder` and `/create-product-vision` run it.
- **`/wait-what`**: the corrective for a message that did not land. The agent re-pitches it in plain language with `GLOSSARY.md` vocabulary.
- **`/handoff`**: a portable file so another agent, harness or colleague continues. Narrow: see Phase boundaries.
- **`/retro`**: after a session, especially one that went sideways.

## Vocabulary underneath

- The **`domain-modeling`** skill sharpens business language: challenges a fuzzy term, resolves an overloaded word, records decisions in `DECISIONS.md`. It is the active discipline `/grill-with-docs` drives.
- `docs/agents/requirements-vocabulary.md` is the shared **process** vocabulary (IDs, statuses). Business terms live in `GLOSSARY.md`; do not mix them.

## Graph

The `graph-sync` skill keeps a deterministic graph of every ID and link (`serves`, `part_of`, `decided_by`, `blocked_by`, `verifies`, `proves`) and answers "what depends on X" without reading every file. Optional; enabled in `/setup-requirements-repo`; merges with a Graphify code or knowledge graph.

## Checks

The `audit-traceability` skill runs a deterministic ID check first (duplicate, dangling, uncovered), then judges semantics. `review-readiness` applies the quality gates. Use both before anyone says "ready".

## Precondition

**`/setup-requirements-repo`** before the first flow, to configure artifact root, tracker, language and triage roles.

## Next steps

Finish every routing answer with `➡️ **Next step:** ...`: one recommended skill (for example `/refine-request`) and why, then at most two alternatives. If the user is mid-flow, point at the next step of that flow; if the state is ambiguous, ask one question.
