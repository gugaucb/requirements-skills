---
name: design-test-scenarios
description: Derive implementation-independent test scenarios with setup, action, expected evidence and negative cases from acceptance criteria and requirements. Use when verifying criteria and requirements.
---

Read the story's AC, FR and NFR. If the story is being altered, invoke `impact-analysis` first.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `<artifact-root>/04-stories/US-NNN.md` with FR, NFR and AC

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Procedure

1. Derive `TC-NNN` rows from each AC and NFR: preconditions, **representative data**, action, expected result, evidence. Cover the AC's negative and boundary cases.
2. For performance and other NFRs, record the real metric, workload and measurement method; do not invent targets.
3. One TC may prove several rows, but every AC needs at least one TC. Add no TC just to fill the matrix.
4. Stay implementation-independent: describe what is observed, not how code is tested.
5. Update the canonical matrix. Leave known gaps visible with a reason.

## Done

Every active AC and NFR has at least one TC; no TC lacks an expected result and evidence.

## Next steps

End with `➡️ **Next step:** ...`. Branching or state logic is hard to read: invoke `diagram-requirements`. Otherwise invoke `audit-traceability`, then `review-readiness`.
