---
name: apply-spec
description: Apply an approved spec's plan of changes to the artifacts, one line at a time in dependency order, recording each in a single change report. Resumable.
disable-model-invocation: true
argument-hint: "SPEC-NNN [how many lines, default 1 story]"
---

Phase 4. Turn the approved plan of a spec into real changes in the stories, backlog, glossary and decisions. It is **resumable**: each run applies the next ready plan line(s), records them, and stops, so context stays small and a human can review between runs.

Read `docs/agents/requirements-workflow.md`. Never run on a spec that is not approved.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/03-specs/SPEC-NNN-slug.md` with status `Approved by <person, date>`
- `<artifact-root>/02-backlog/BACKLOG.md`
- `<artifact-root>/shared/GLOSSARY.md`
- `<artifact-root>/shared/DECISIONS.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Contract

- **Reads:** the approved `03-specs/SPEC-NNN`, `BACKLOG.md`, the graph, the artifacts named by the plan.
- **Writes:** the artifacts the plan names, `04-stories/US-NNN.md` for new stories, one `05-changes/CHG-NNN.md` for the whole spec, the plan statuses and backlog checklists.
- **Gate:** the PO reviews the result; `/review-spec` checks it against the spec.

## Process

1. **Check the gate.** The spec status must read `Approved by <person, date>`. If it is `Draft` or `Ready for human review`, stop and tell the user to get the PO approval first. If a `new-story` line points at no backlog story, stop and tell the user to run `/split-backlog`.
2. **One change record per spec.** If the spec header has no `**Change:** CHG-NNN` line, invoke the `impact-analysis` skill once for the **whole plan** (all targets together), write the CHG with source `SPEC-NNN`, mark impacted items `Stale`, and add `**Change:** CHG-NNN` to the spec. On later runs reuse it.
3. **Pick the work.** Run `req-graph.py plan <artifact-root> SPEC-NNN`. Take the lines marked NEXT (ready and in dependency order). Default: the next **one story** and any non-story lines that do not depend on it; the user may ask for more.
4. **Apply each line by kind:**
   - `modify-story`, `new-story`: invoke the `refine-story` skill for that story (change mode for modify). Keep IDs; retire replaced content as `Superseded by`.
   - `modify-glossary`, `new-decision`: invoke the `domain-modeling` skill. A decision is Confirmed only if the accountable human answered.
   - `modify-backlog`: edit `BACKLOG.md` rows or checklists; never delete or renumber.
   - `modify-vision`, `modify-canvas`: these skills are run by the user. Mark the line `Blocked (needs /create-product-vision)` or `Blocked (needs /project-canvas)` and tell the user.
5. **Record.** Set the line's Status to `Done (CHG-NNN)`, or `Skipped (reason)` / `Blocked (reason)`. Append a resolution line to the CHG. If the graph is enabled, invoke `graph-sync`.
6. **Stop and report:** lines closed, lines left, what is blocked and by whom. Suggest clearing context before the next run.

## Rules

- Change only what the plan names. A needed change outside the plan is a new plan line: stop and put it to the PO.
- Never edit an artifact whose upstream is unapproved. Never mark anything approved.
- Never commit or push; propose the commit message per `docs/agents/versioning.md`.

## Done

For the run: every line attempted has a status; the CHG log and the plan agree; nothing outside the plan changed.

## Next steps

End with `➡️ **Next step:** ...`.

- Lines left: clear context and run `/apply-spec SPEC-NNN` again.
- Only blocked lines left: `/create-product-vision`, `/project-canvas` or the missing PO decision.
- All lines closed: `/review-spec SPEC-NNN`.
