---
name: review-readiness
description: Audit story clarity, requirements, tests, acceptance coverage and recorded human decisions against local readiness rules. Use when doing the final refinement review; never to impersonate PO signoff.
---

Read [QUALITY-GATES.md](QUALITY-GATES.md) and the configured workflow in `docs/agents/requirements-workflow.md` (team Definition of Ready, if any), then the story.

## Procedure

1. Run `audit-traceability` on the story; its gaps are readiness gaps.
2. Check each gate in QUALITY-GATES.md, in two axes: **Standards** (clarity, atomicity, measurability, language) and **Alignment** (serves a real CAP, respects the vision and Confirmed decisions, no Stale upstream).
3. Choose the status: `Draft`, `Blocked`, `Needs changes`, `Ready for human review`. `Ready (team agreement)` only with recorded human confirmation. Never claim PO approval.
4. List findings as a table: gate, finding, owner, action.

Definition of Ready is a team agreement; it is not the Scrum Definition of Done.

## Done

A status is set with evidence, and every unresolved PO decision is listed with an owner.

## Next steps

End with `➡️ **Next step:** ...`.

- Needs changes or Blocked: `/refine-request US-NNN` again, or `/grill-with-docs` for decisions.
- Ready for human review: ask the PO to review; record approval as a DEC; update status to Ready (team agreement).
- Whole spec ready: continue the frontier in `BACKLOG.md`.
