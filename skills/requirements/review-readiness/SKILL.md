---
name: review-readiness
description: Audit story clarity, requirements, tests, acceptance coverage and recorded human decisions against local readiness rules. Use when doing the final refinement review; never to impersonate PO signoff.
---

Read [QUALITY-GATES.md](QUALITY-GATES.md) and the configured workflow in `docs/agents/requirements-workflow.md` (team Definition of Ready, if any), then the story.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/04-stories/US-NNN.md`
- [QUALITY-GATES.md](QUALITY-GATES.md)

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Procedure

0. **Run the evidence commands** (see Evidence below) and keep their output.
1. Invoke `audit-traceability` on the story; its gaps are readiness gaps.
2. Check each gate in QUALITY-GATES.md, in two axes: **Standards** (clarity, atomicity, measurability, language) and **Alignment** (serves a real CAP, respects the vision and Confirmed decisions, no Stale upstream).
3. Choose the **verdict** and the status. `BLOCKED` (status `Blocked`): a gate cannot pass without a decision or a missing input. `NEEDS CHANGES` (status `Needs changes`): a mechanical fix is enough. `PASS` (status `Ready for human review`). `Ready (team agreement)` only with recorded human confirmation. Never claim PO approval.
4. List findings as a table: gate, verdict, finding, owner, **return to**. The return route comes from the "Return to" column of [QUALITY-GATES.md](QUALITY-GATES.md); after the fix, run this review again.

| If this fails | Return to |
| --- | --- |
| Tests missing or not derivable from the AC (G5) | `design-test-scenarios`, or `define-acceptance-criteria` if the AC is ambiguous |
| FR or NFR without AC (G4) | `define-acceptance-criteria` |
| Requirements not atomic or no metric (G3) | `specify-requirements` |
| Glossary or rule inconsistency (G6) | `domain-modeling` |
| Stale upstream (G7) | `refine-story` (or `/apply-spec` for a spec) |
| Rule without decision (G8) | `/grill-with-docs` |
| Screens undecided or form duplicated in ACs (G10) | `write-user-story` |

Definition of Ready is a team agreement; it is not the Scrum Definition of Done.

## Evidence (run before answering)

You **must** run the script below in a terminal **before** you write your answer, and paste its trimmed output, with the exit code, under a `### Evidence` heading in your report. If you cannot execute commands, say so and mark the verdict **Unverified**. Never describe a result you did not obtain.

```bash
python3 <graph-sync-dir>/scripts/req-graph.py validate <artifact-root>
python3 <graph-sync-dir>/scripts/req-graph.py backlog <artifact-root>   # checklist vs status
```


## Done

A status is set with evidence, and every unresolved PO decision is listed with an owner.

## Next steps

End with `➡️ **Next step:** ...`.

- Needs changes or Blocked: `/refine-request US-NNN` again, or `/grill-with-docs` for decisions.
- Ready for human review: ask the PO to review; record approval as a DEC; update status to Ready (team agreement).
- Whole spec ready: continue the frontier in `BACKLOG.md`.
