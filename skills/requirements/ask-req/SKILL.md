---
name: ask-req
description: Ask which requirements skill or flow fits your situation. A router over every skill in this repo, aware of the current phase and state of your artifacts.
disable-model-invocation: true
---

# Ask Req

You do not remember every skill, so ask.

Before stating what a skill does or recommending a step be skipped, read that skill's SKILL.md: the summaries here are for orientation only.

The work travels **five phases**. The output of each phase is the input of the next, and each skill ends by suggesting the next step, so after the first skill you can simply follow the suggestions.

| Phase | Skill | Reads | Writes | Human gate |
| --- | --- | --- | --- | --- |
| 1 | `/project-canvas`, then `/create-product-vision` | narrative, minutes | `00-canvas/`, `01-vision/` | sponsor approves the vision |
| 2 | `/split-backlog` | CAPs of the vision | `02-backlog/` (WBS, operations checklist) | PO confirms the order |
| 3 | `/spec-req` | a backlog story, a conversation, or minutes | `03-specs/` (strategy and plan of changes) | PO approves the spec |
| 4 | `/apply-spec` (drives `refine-story`) | the approved spec | updated artifacts, `04-stories/`, `05-changes/` | PO reviews |
| 5 | `/review-spec` | spec, changes, graph | review report in the spec | PO signs |

Setup comes once: **`/setup-requirements-repo`** configures artifact root, folders, tracker, language, versioning and the graph. Humans approve at every gate; skills recommend.

## Preflight (Pré-condições / Insumos Obrigatórios)

No file is required: it diagnoses what is missing and recommends the skill that produces it.

## Read the state first

Do not ask the user what they already have. Look at the artifact root (see `docs/agents/requirements-workflow.md`) and route by what you find:

| You find | Recommend |
| --- | --- |
| No `docs/agents/` config | `/setup-requirements-repo` |
| New system, no canvas, no vision | `/project-canvas` (small idea: `/grill-with-docs` then `/create-product-vision`; huge or foggy: `/wayfinder`) |
| Canvas Draft | finish it with `/project-canvas`; it checks its own integration rules |
| Canvas approved, no vision | `/create-product-vision` |
| Vision Draft | the `review-product-vision` skill, then sponsor approval recorded as a DEC |
| Approved vision, empty backlog | `/split-backlog` |
| Backlog stories, user wants detail or a change | `/spec-req US-NNN` |
| A meeting minute or a conversation with change requests | `/spec-req` on the minutes or the conversation |
| Spec Draft | PO approval (and `/split-backlog` if it plans new stories without IDs) |
| Spec Approved, plan lines Pending | `/apply-spec SPEC-NNN` |
| All plan lines Done | `/review-spec SPEC-NNN` |
| A single story to refine, no spec needed | `/refine-request US-NNN` |
| Any item `Stale`, or an open `CHG` | `/apply-spec` if it came from a spec, else `/refine-request` on each |
| Raw requests waiting | `/triage` |
| A change to an existing story, capability or term | the change flow below |

Report what you found in two lines, then recommend one next step.

If `docs/agents/graph.md` exists, ask the graph instead of scanning files: invoke the `graph-sync` skill, then `req-graph.py frontier`, `stale`, `backlog` and `plan SPEC-NNN`. Without a graph, read `BACKLOG.md`, the spec plan tables and the story statuses. The user can also type **`/req-graph`** and ask in plain words.

## Phase detail

1. **Canvas and vision.** `/project-canvas` walks the 13 blocks of the Project Model Canvas, enforces the integration rules (cause and effect, cross constraints, the reverse traceability test) and writes `PROJECT-CANVAS.md`. `/create-product-vision` derives goals (from objectives) and capabilities (from deliveries and product items) with their origin. For an existing system without a canvas, start from `/grill-with-docs` and `/create-product-vision`.
2. **WBS and backlog.** `/split-backlog` decomposes each capability into thin vertical stories with blocking edges and an **operations checklist** per story (for example include, edit, remove, consult). Status is the lifecycle; Progress is derived from the checklist.
3. **Spec.** `/spec-req` explains the strategy to meet a story or change and lists every artifact that must change as `PLN` lines (target, kind, change, reason, dependencies). It never interviews; minutes are evidence, extracted items stay Proposed.
4. **Apply.** `/apply-spec` runs only on an approved spec, one ready plan line at a time, in dependency order, with one change report for the whole spec. Stories go through `refine-story` (which uses `write-user-story`, `specify-requirements`, `define-acceptance-criteria`, `design-test-scenarios`, `diagram-requirements`, `audit-traceability`, `review-readiness`). Glossary and decisions go through `domain-modeling`. Vision and canvas lines wait for the user to run their skills.
5. **Review.** `/review-spec` checks plan closure, conformance line by line, nothing extra, nothing stale, quality gates; the PO signs.

Context hygiene: keep `/grill-with-docs`, `/spec-req` and `/split-backlog` in one context when they build on the same reasoning; clear between runs of `/apply-spec` and between stories. See [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md).

## The change flow: altering an existing story

When a story, capability, goal, decision or glossary term **changes**, the cost is downstream. Do not edit first.

1. **`/grill-with-docs`** (or `/grill-me` if stateless) on the change. In **change mode** the interview ends with an **impact round** from the `impact-analysis` skill: downstream (FR, AC, TC, screens), upstream (CAP, GOAL, vision) and sideways items, each Invalidated, Needs review or Unaffected (checked).
2. For one change, the report is stored as `05-changes/CHG-NNN.md` and impacted items become `Stale`; `/refine-request` clears them. For many changes, write a spec with `/spec-req` and let `/apply-spec` apply it with a single change report.
3. `audit-traceability` and `/review-spec` confirm closure.

The writers (`write-user-story`, `specify-requirements`, `define-acceptance-criteria`, `design-test-scenarios`) also invoke `impact-analysis` before editing existing items, so the guard holds even when you skip the grilling.

## On-ramps

- **Raw requests piling up, or a change request arriving** → **`/triage`**. It moves items through roles, checks impact for changes, writes a refinement-ready brief, and merges onto the flow at `/spec-req`, `/split-backlog` or `/refine-request`. Do not triage what `/split-backlog` produced.
- **A huge, foggy effort** → **`/wayfinder`**: a shared map of decision tickets, resolved one at a time. When the map clears it **hands off, it does not specify**: to `/project-canvas`, `/create-product-vision` or `/spec-req`.
- **The knowledge sits with someone else** → **`/to-questionnaire`**. Answers return to `/grill-with-docs`, `/spec-req` or a wayfinder ticket.
- **A fact outside the repo** (law, contract, existing system) → the `research` skill leaves a cited file.

## Standalone

- **`/grill-me`**: the same relentless interview, **stateless**. In a repo, `/grill-with-docs` leaves a paper trail and is strictly better.
- The **`grilling`** skill is the interview primitive behind `/grill-me`, `/grill-with-docs`, `/triage`, `/wayfinder`, `/project-canvas` and `/create-product-vision`.
- **`/req-graph`**: ask the graph in plain words (rebuild, open the viewer, what depends on X, search, path, backlog progress, a spec's plan).
- **`/wait-what`**: re-pitch a message that did not land. **`/handoff`**: a portable file for another agent or colleague. **`/retro`**: improve the environment after a session.

## Vocabulary underneath

- The **`domain-modeling`** skill sharpens business language and records decisions in `DECISIONS.md`.
- `docs/agents/requirements-vocabulary.md` is the shared **process** vocabulary (IDs, statuses). Business terms live in `GLOSSARY.md`; do not mix them.

## Graph

The `graph-sync` skill keeps a deterministic graph of every ID and link and answers "what depends on X" without reading every file. Optional; enabled in `/setup-requirements-repo`; merges with a Graphify code or knowledge graph.

## Checks

The `audit-traceability` skill runs a deterministic ID check first, then judges semantics. `review-readiness` applies the quality gates. `/project-canvas` runs `canvas-check.py`. Use them before anyone says "ready".

## Next steps

Finish every routing answer with `➡️ **Next step:** ...`: one recommended skill (for example `/apply-spec`) and why, then at most two alternatives. If the user is mid-flow, point at the next step of that flow; if the state is ambiguous, ask one question.
