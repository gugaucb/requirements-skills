---
name: refine-request
description: Refine one story, or one small well-scoped request, end to end into requirements, acceptance criteria, tests and traceability. Run it per story in a fresh context.
disable-model-invocation: true
argument-hint: "US-NNN or the request"
---

Refine **one** story (an `US-NNN` from `BACKLOG.md`, or a small request that fits one story) from "As a / I want" to Ready for human review. Decide what is needed; never run skills mechanically.

Read `docs/agents/requirements-workflow.md`, `GLOSSARY.md`, `DECISIONS.md`, the vision, and the story's linked `GOAL`/`CAP`/spec. With the graph enabled (`docs/agents/graph.md`), load context narrowly instead: `req-graph.py affected <artifact-root> US-NNN --up` lists exactly the goals, capabilities, spec and decisions this story depends on; read only those sections. Fresh context per story stays cheap.

## Process

1. **Classify** the request against the vision: _aligned_, _unclear_, or _scope-changing_. Unclear or scope-changing: log a pending DEC and ask the PO; do not rewrite the vision.
2. **Check size.** If it needs several stories, stop and tell the user to run `/to-spec` then `/split-backlog`. Refine one story only.
3. **Change mode.** If the story already exists (it has a file, ACs or tests, or a `Stale` status), invoke the `impact-analysis` skill first and get the user's go-ahead on its report.
4. **Close open decisions.** When PO decisions or terms are missing, invoke the `grilling` skill and the `domain-modeling` skill. Skip when the request is fully specified.
5. **Build, in order, as needed:**
   1. `write-user-story`
   2. `specify-requirements`
   3. `define-acceptance-criteria`
   4. `design-test-scenarios`
   5. `diagram-requirements` (only for real branching or states)
6. **Verify.** Invoke `audit-traceability`, then `review-readiness`. If the graph is enabled, invoke `graph-sync` afterwards.
7. **Deliver** actionable partial drafts with explicit blockers rather than waiting for perfection.

If you refined a `Stale` story, append a line to its change history and to the CHG resolution log.

## Done

The story file holds FR/NFR, AC and TC with a complete matrix; status is at most **Ready for human review**; blockers and PO decisions are listed.

## Next steps

End with `➡️ **Next step:** ...`.

- Another unblocked story in `BACKLOG.md`: `/refine-request US-NNN` in a fresh context.
- More Stale stories from a CHG: continue in dependency order.
- All stories of a spec are Ready for human review: ask the PO to review and record the approval as a DEC, then publish through `/split-backlog` if the tracker needs it.
- Pattern of rework or missing terms: `/retro`.
