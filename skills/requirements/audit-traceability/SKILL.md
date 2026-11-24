---
name: audit-traceability
description: Verify links from product goals and capabilities through epics, stories, functional and non-functional requirements, acceptance criteria and tests, and detect Stale items after changes. Use after changes, before reviews, or when IDs may be duplicated or dangling.
---

Read [TRACEABILITY.md](TRACEABILITY.md) for the model.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- at least one `<artifact-root>/04-stories/US-NNN.md`
- the graph-sync scripts (`graph-sync/scripts/req-graph.py`, `reqmd.py`)

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Procedure

1. **Run the deterministic check first** (mechanical errors belong to a script, not to judgement); see Evidence below. It reports duplicate definitions, dangling references, FR/NFR without AC, AC without TC, stories with no matrix, items marked `Stale`, dependency cycles, and the Top 5 critical artifacts. Act on its **exit code**:

   | Exit | Meaning | What you do |
   | --- | --- | --- |
   | 0 | consistent | continue to the judgement steps |
   | 1 | orphan IDs or untested rules | list each finding with its return route (table in `docs/FLOW.md`); duplicate IDs: stop and ask, never renumber |
   | 2 | dependency cycle | stop; show the cycle; ask the user which dependency is wrong (`/grill-with-docs`) |
   | 3 | critical parse or file failure | report the file and the cause; do not continue until the input is fixed |

   `[PARSE-WARNING]` lines on stderr are findings too: a malformed row or ID was reported, not ignored.
2. **Graph checks** (when `docs/agents/graph.md` exists; invoke `graph-sync`): the build lists unresolved IDs; also look for a CAP with no story (nothing `part_of`/`serves` it), a story with no `serves`, and a DEC that most items hang on (many `decided_by` edges), which makes it a risk worth re-confirming.
3. **Judge what the script cannot.** Token overlap is not meaning. For each link, ask whether the AC really proves the FR and the CAP really justifies the story. Flag false semantic links.
4. **Check both directions:** `GOAL→CAP→EPIC (optional)→US→FR/NFR→AC→TC` and back. A CAP may link straight to a story; do not force an epic.
5. **Check change closure.** Every `CHG-NNN` has its Needs review items resolved or consciously accepted; no item stays `Stale` without an open CHG.
6. **Report** actual unique-ID counts, gaps, and the scope-change impact of anything open. Keep each story matrix normative and vision/backlog links as the higher-level path.

## Evidence (run before answering)

You **must** run the script below in a terminal **before** you write your answer, and paste its trimmed output, with the exit code, under a `### Evidence` heading in your report. If you cannot execute commands, say so and mark the verdict **Unverified**. Never describe a result you did not obtain.

```bash
python3 <graph-sync-dir>/scripts/req-graph.py validate <artifact-root>
# same result through the stable entry point: python3 <this-skill-dir>/scripts/check-ids.py <artifact-root>
```


## Done

Every gap is listed with the ID and the action; counts come from the script or an explicit read, never from memory.

## Next steps

End with `➡️ **Next step:** ...`. Gaps in a story: `/refine-request US-NNN` (or the return route of the finding). A cycle: `/grill-with-docs`. Clean: invoke `review-readiness`. Duplicate IDs: stop and ask the user; never renumber silently.
