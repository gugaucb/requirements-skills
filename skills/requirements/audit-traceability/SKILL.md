---
name: audit-traceability
description: Verify links from product goals and capabilities through epics, stories, functional and non-functional requirements, acceptance criteria and tests, and detect Stale items after changes. Use after changes, before reviews, or when IDs may be duplicated or dangling.
---

Read [TRACEABILITY.md](TRACEABILITY.md) for the model.

## Procedure

1. **Run the deterministic check first** (mechanical errors belong to a script, not to judgement):

   ```bash
   python3 <this-skill-dir>/scripts/check-ids.py <artifact-root>
   ```

   It reports duplicate definitions, dangling references, FR/NFR without AC, AC without TC, stories with no matrix, and items marked `Stale`. If Python is unavailable, do the same by reading each story matrix.
2. **Graph checks** (when `docs/agents/graph.md` exists; invoke `graph-sync`): the build lists unresolved IDs; also look for a CAP with no story (nothing `part_of`/`serves` it), a story with no `serves`, and a DEC that most items hang on (many `decided_by` edges), which makes it a risk worth re-confirming.
3. **Judge what the script cannot.** Token overlap is not meaning. For each link, ask whether the AC really proves the FR and the CAP really justifies the story. Flag false semantic links.
4. **Check both directions:** `GOAL→CAP→EPIC (optional)→US→FR/NFR→AC→TC` and back. A CAP may link straight to a story; do not force an epic.
5. **Check change closure.** Every `CHG-NNN` has its Needs review items resolved or consciously accepted; no item stays `Stale` without an open CHG.
6. **Report** actual unique-ID counts, gaps, and the scope-change impact of anything open. Keep each story matrix normative and vision/backlog links as the higher-level path.

## Done

Every gap is listed with the ID and the action; counts come from the script or an explicit read, never from memory.

## Next steps

End with `➡️ **Next step:** ...`. Gaps in a story: `/refine-request US-NNN`. Clean: invoke `review-readiness`. Duplicate IDs: stop and ask the user; never renumber silently.
