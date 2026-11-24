---
name: refine-story
description: Take one story through the refinement pipeline (decisions, story text, requirements, acceptance criteria, tests, diagram, audit, readiness) and tick its operations checklist. Use when a story must be refined or re-refined, from refine-request or apply-spec.
---

The shared pipeline behind `/refine-request` (one story) and `/apply-spec` (a plan of changes). It decides what the story needs; it never runs steps mechanically.

Read `docs/agents/requirements-workflow.md`, `GLOSSARY.md`, `DECISIONS.md`, the story's `CAP`, `EPIC` and spec, and its row and operations checklist in `BACKLOG.md`. With the graph enabled, load context narrowly: `req-graph.py affected <artifact-root> US-NNN --up` lists the goals, capabilities, spec and decisions the story depends on; read only those sections.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/02-backlog/BACKLOG.md` (the story row and its operations checklist)
- `<artifact-root>/01-vision/PRODUCT-VISION.md`
- `<artifact-root>/shared/GLOSSARY.md`
- `<artifact-root>/shared/DECISIONS.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Procedure

1. **Close open decisions.** When PO decisions or terms are missing, invoke the `grilling` skill and the `domain-modeling` skill. Skip if the story is fully specified.
2. **Build, in order, as needed:** `write-user-story` (including the Fields and Screens decision), `specify-requirements`, `define-acceptance-criteria`, `design-test-scenarios`, `diagram-requirements` (only for real branching or states). In change mode the writers invoke `impact-analysis` first.
3. **Tick the operations checklist.** For each line of the story's checklist in `BACKLOG.md` (`- [ ] operation`), when a FR, AC and TC cover it, mark `[x]` and append the IDs: `- [x] edit customer (FR-004, AC-004, TC-004)`. Leave an operation with no coverage unchecked and say why. Add a line for an operation the requirements reveal that the checklist missed, tagged Proposed.
4. **Update Progress** in the story's `BACKLOG.md` row from the checklist: `Pending` (none ticked), `In progress`, `Done` (all ticked). Progress is derived; the lifecycle **Status** column is not touched here.
5. **Verify.** Invoke `audit-traceability`, then `review-readiness`. If the graph is enabled, invoke `graph-sync` afterwards.
6. **Close the change item.** If the story was `Stale`, append a line to its change history and to the CHG resolution log.

## Done

The story file holds FR/NFR, AC and TC with a complete matrix; its checklist reflects the coverage; status is at most **Ready for human review**; blockers and open PO decisions are listed.

## Next steps

Return to the caller: `/refine-request` suggests the next frontier story, `/apply-spec` takes the next plan line. Standalone: another frontier story (`/req-graph frontier`), or `/review-spec` when the story closes the last line of a spec.
