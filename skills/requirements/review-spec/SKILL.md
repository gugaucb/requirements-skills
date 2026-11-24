---
name: review-spec
description: Phase 5 review. Check that the artifacts changed as the approved spec planned, nothing else changed, nothing stays Stale, and the touched stories pass the quality gates.
disable-model-invocation: true
argument-hint: "SPEC-NNN"
---

Phase 5. Confirm that what was built matches what the spec asked for, and report gaps. It never signs for the PO.

Read `docs/agents/requirements-workflow.md`, the spec, its plan, its CHG, and the touched artifacts.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `<artifact-root>/03-specs/SPEC-NNN-slug.md` with a Plan of changes
- `<artifact-root>/05-changes/CHG-NNN.md`
- `<artifact-root>/02-backlog/BACKLOG.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Contract

- **Reads:** `03-specs/SPEC-NNN`, `05-changes/CHG-NNN`, the touched artifacts, the graph.
- **Writes:** the `## Review` section of the spec; nothing else.
- **Gate:** the PO signs; the spec status then moves to `Applied`, backed by a DEC.

## Process

1. **Plan closure.** Run `req-graph.py plan <artifact-root> SPEC-NNN`. Every line must be `Done (CHG-NNN)` or `Skipped (reason)` with a reason the PO can read. Open or Blocked lines are gaps.
2. **Conformance, line by line.** Open each target and judge whether the change says what the plan line and the spec's Strategy and Business rules asked. Record the evidence (file and section, or ID). A line that was applied differently from the plan is a gap, not a pass.
3. **Nothing extra.** Compare the CHG impact list and the files that changed with the plan. A change outside the plan is flagged for the PO.
4. **Nothing stale.** Run `req-graph.py stale <artifact-root>`: any item still `Stale` from this CHG is a gap.
5. **Quality gates.** For every touched story invoke `audit-traceability`, then `review-readiness`. Include the operations checklist (`req-graph.py backlog`): a story marked Ready whose checklist is incomplete is a gap.
6. **Report** in the spec's `## Review`: a table of line, verdict (Conforms, Gap), evidence, owner; then an overall verdict. State plainly that PO review is still required.

## Evidence (run before answering)

You **must** run the script below in a terminal **before** you write your answer, and paste its trimmed output, with the exit code, under a `### Evidence` heading in your report. If you cannot execute commands, say so and mark the verdict **Unverified**. Never describe a result you did not obtain.

```bash
python3 <graph-sync-dir>/scripts/req-graph.py validate <artifact-root>
python3 <graph-sync-dir>/scripts/req-graph.py plan <artifact-root> SPEC-NNN
python3 <graph-sync-dir>/scripts/req-graph.py stale <artifact-root>
python3 <graph-sync-dir>/scripts/req-graph.py backlog <artifact-root>
```


## Done

Every plan line has a verdict with evidence, and every gap names an owner and the skill that fixes it.

## Next steps

End with `➡️ **Next step:** ...`.

- Gaps: `/apply-spec SPEC-NNN` for unfinished lines, `/refine-request US-NNN` for a story that fails its gates, `/grill-with-docs` for a missing decision.
- Clean: ask the PO to review and sign; record the approval as a DEC and set the spec to `Applied`. Then `/retro` if the effort was rough, or `/ask-req` for the next piece of work.
