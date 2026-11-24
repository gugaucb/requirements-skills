---
name: refine-request
description: Refine one story, or one small well-scoped request, end to end into requirements, acceptance criteria, tests and traceability. Run it per story in a fresh context.
disable-model-invocation: true
argument-hint: "US-NNN or the request"
---

Refine **one** story (an `US-NNN` from `BACKLOG.md`, or a small request that fits one story) from "As a / I want" to Ready for human review. It decides whether the story is ready to refine, then hands the work to the `refine-story` pipeline. For a batch of changes from a spec, use `/apply-spec`.

Read `docs/agents/requirements-workflow.md`, `GLOSSARY.md`, `DECISIONS.md`, the vision, and the story's linked `GOAL`/`CAP`/spec.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/02-backlog/BACKLOG.md` (the story row)
- `<artifact-root>/01-vision/PRODUCT-VISION.md`
- `<artifact-root>/shared/GLOSSARY.md`
- `<artifact-root>/shared/DECISIONS.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Contract

- **Reads:** the story's backlog row and operations checklist, its file if any, the vision, glossary, decisions, graph.
- **Writes:** `04-stories/US-NNN.md`, its checklist ticks and progress in `BACKLOG.md`; a CHG when in change mode.
- **Gate:** the PO reviews stories that reach `Ready for human review`.

## Process

1. **Classify** the request against the vision: _aligned_, _unclear_, or _scope-changing_. Unclear or scope-changing: log a pending DEC and ask the PO; do not rewrite the vision.
2. **Check size.** If it needs several stories, stop and tell the user to run `/spec-req` then `/split-backlog` (or `/split-backlog` alone when a capability already exists). Refine one story only.
3. **Change mode.** If the story already exists (it has a file, ACs or tests, or a `Stale` status), invoke the `impact-analysis` skill first and get the user's go-ahead on its report. If the change comes from an approved spec, stop: `/apply-spec` owns it.
4. **Refine.** Invoke the `refine-story` skill.
5. **Deliver** actionable partial drafts with explicit blockers rather than waiting for perfection.

## Done

The story file holds FR/NFR, AC and TC with a complete matrix; its operations checklist is ticked where covered; status is at most **Ready for human review**; blockers and PO decisions are listed.

## Next steps

End with `➡️ **Next step:** ...`.

- Another unblocked story in `BACKLOG.md` (`/req-graph frontier`): `/refine-request US-NNN` in a fresh context.
- More Stale stories from a CHG: continue in dependency order, or `/apply-spec` if they come from a spec.
- All stories of a spec are Ready for human review: `/review-spec SPEC-NNN`, then PO review.
- Pattern of rework or missing terms: `/retro`.
