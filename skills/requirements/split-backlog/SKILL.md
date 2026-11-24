---
name: split-backlog
description: Break a spec, capability or epic into thin vertical user stories, each declaring its blocking edges, and record them in BACKLOG.md or the configured tracker.
disable-model-invocation: true
---

Phase 2. Decompose the capabilities of the vision into a **WBS** (EAP): capability, optional epic, story. Break a spec, capability, epic or the current conversation into **stories**: thin vertical slices of user value, each declaring the stories that **block** it. This is the tracer-bullet idea applied to requirements.

Read `docs/agents/requirements-workflow.md` and `docs/agents/issue-tracker.md`. If missing, tell the user to run `/setup-requirements-repo`.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/01-vision/PRODUCT-VISION.md`
- `<artifact-root>/shared/GLOSSARY.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

Also read, when relevant: `<artifact-root>/02-backlog/BACKLOG.md` (to avoid duplicates); a spec, epic or capability to slice.

## Contract

- **Reads:** `01-vision/PRODUCT-VISION.md` (the CAPs), a spec or epic if given, `BACKLOG.md`.
- **Writes:** `02-backlog/BACKLOG.md`: a table (capability, epic, story, name, blocked by, status, progress) and, per story, an **operations checklist** (`- [ ] operation: what it does`). Publishes to the tracker only on request.
- **Gate:** the PO confirms the breakdown and the order.

## Process

### 1. Gather context

Use the conversation. If the user passes a reference (a spec path, `CAP-NNN`, an issue), read it fully. Read `BACKLOG.md` so you do not duplicate or renumber existing stories.

### 2. Draft vertical slices

<slicing-rules>

- Each story is a narrow but COMPLETE path of business value: an actor, an outcome, observable by the PO. Not a screen, a table, or a technical layer.
- A finished story is demoable or verifiable on its own.
- Each story fits one refinement session (`/refine-request` in a fresh context).
- Order by real dependency, not preference. Prefer enabling rules first ("make the change easy, then make the easy change").
- Technical-only stories exist only with an explicit quality or enablement purpose that stakeholders agree.
- Epics are optional: group only when a real collection of value exists.

</slicing-rules>

Give each story an **operations checklist**: the business operations it covers, one line each, in business language (for example "include customer", "edit customer", "remove customer", "consult customer"), each with a short description. The checklist is how progress is tracked; `refine-story` ticks a line when a requirement, criterion and test cover it.

Give each story its **Blocked by** edges: stories that must be done first. No blockers means it can start now.

### 3. Quiz the user

Present a numbered list. For each: **Title**, **Serves** (CAP/EPIC), **Blocked by**, **What it delivers**, **Operations**. Ask:

- Does the granularity feel right (too coarse, too fine)?
- Does each story depend only on stories that genuinely gate it?
- Should any be merged or split?

Iterate until the user approves. Priority and sprint assignment are PO-owned: record order as **Proposed** and never invent sprints.

### 4. Record

A minimal result (full format in [BACKLOG-FORMAT.md](BACKLOG-FORMAT.md)):

```md
| Order | Capability | Epic | Story | Name | Blocked by | Status | Progress |
| Proposed 1 | CAP-001 | EPIC-001 Registry | US-001 | Maintain customer | None | Draft | Pending |

### US-001: Maintain customer
- [ ] include customer: register a new customer with the mandatory data
- [ ] edit customer: change the data of an existing customer
```

Write rows and operations blocks to `02-backlog/BACKLOG.md` (format in [BACKLOG-FORMAT.md](BACKLOG-FORMAT.md)), allocating `US-NNN` IDs without recycling. Create no story files yet; `write-user-story` does that lazily. Called on stories a spec created, add only those rows.

Publish to the tracker only when the user explicitly asks and the tracker doc allows it: one issue per story in dependency order (blockers first), native blocking links where the tracker has them, label `ready-for-refinement`. Never close or edit a parent issue.

If `docs/agents/graph.md` exists, invoke the `graph-sync` skill afterwards so the `blocked_by` frontier is queryable.

## Done

Every candidate story is in `BACKLOG.md` with serves-links, blockers and a Proposed order, and the user approved the breakdown.

## Next steps

End with `➡️ **Next step:** ...`.

- Splitting for a spec: back to `/spec-req` to finish the plan, then the PO approves and `/apply-spec` runs.
- Start with the first story that has no blockers: `/refine-request US-NNN`. Work the frontier (all blockers done), a fresh context per story.
- Broad stories remain after the quiz: run `/split-backlog` again on them.
