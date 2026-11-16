---
name: design-test-scenarios
description: Derive implementation-independent test scenarios with setup, action, expected evidence and negative cases from acceptance criteria and requirements. Use when verifying criteria and requirements.
---

Read the story's AC, FR and NFR. If the story is being altered, invoke `impact-analysis` first.

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
