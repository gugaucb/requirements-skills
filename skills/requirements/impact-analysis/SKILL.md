---
name: impact-analysis
description: Analyse the downstream, upstream and sideways impact of a change to a user story, requirement, acceptance criterion, capability, goal, decision or glossary term. Use before editing any artifact that already has IDs, when a story is altered, when a rule or term is redefined, or when a grilling session is in change mode.
---

Make the effect of a change visible **before** it is applied. Impact is derived by walking the traceability model, not by keyword luck.

Read `docs/agents/requirements-workflow.md` for the artifact root, then the traceability model in [TRACEABILITY.md](../audit-traceability/TRACEABILITY.md).

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- the artifact being changed (an ID that exists under the artifact root)

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

Also read, when relevant: `docs/agents/graph.md` (graph-first path).

## Procedure

1. **State the change.** Which IDs, from what to what, why, who asked, status (Proposed or Confirmed). Classify it: `rule`, `scope`, `actor`, `metric`, `term`, `priority`, `removal`. Done when each changed ID has a one-line before and after.

2. **Walk downward.** For every changed ID list what hangs under it: `US → FR/NFR → AC → TC`, diagrams (DG), and `BACKLOG.md` rows. **Graph first:** when `docs/agents/graph.md` exists, invoke the `graph-sync` skill, then run `python3 <skill-dir>/../graph-sync/scripts/req-graph.py affected <artifact-root> <ID> --no-weak`. It lists dependents and sideways candidates in one call (`--up` gives the upstream walk of step 3). Without a graph, run `check-ids.py` from `audit-traceability` or read the story matrices. The list is a set of candidates; you still classify each one.

3. **Walk upward.** Does the change still serve its `CAP` and `GOAL`? Does it contradict `PRODUCT-VISION.md` scope or an approved `DEC`? A change that moves a boundary is **scope-changing**: stop and put it to the PO as a pending decision before anything else.

4. **Walk sideways.** Search the artifact root for other items sharing the same term, rule, actor, capability, state or number: sibling stories, `BACKLOG.md` dependencies ("Blocked by"), `GLOSSARY.md` entries, other `DEC` rows, open questionnaires or wayfinder tickets.

5. **Classify every touched item** (use the exact words):
   - **Invalidated**: now wrong, must be rewritten or retired.
   - **Needs review**: may still hold, a human or `refine-request` must re-check.
   - **Unaffected (checked)**: looked at, still holds. List these too; silence reads as "not looked at".

A minimal impact table (full format in [CHANGE-IMPACT-FORMAT.md](CHANGE-IMPACT-FORMAT.md)):

| ID | Relation | Classification | Action |
| --- | --- | --- | --- |
| AC-012 | downstream of FR-007 | Invalidated | Rewrite |
| US-004 | sideways (same term "active") | Needs review | Check rule R3 |
| CAP-002 | upstream | Unaffected (checked) | Still served |

6. **Write the report** with [CHANGE-IMPACT-FORMAT.md](CHANGE-IMPACT-FORMAT.md) to `<artifact-root>/05-changes/CHG-NNN.md` (stateful callers) or present it in chat (stateless callers). Done when every touched ID is classified and the report names the PO decisions it needs.

7. **Mark, do not rewrite.** For stateful callers, set impacted downstream items to status `Stale` and add one line to their change history pointing at the CHG file. Do not edit downstream content without the user's go-ahead. Then, if the graph is enabled, invoke `graph-sync` so the `Stale` statuses and the new CHG are in it. Keep IDs; a retired item is marked `Superseded by <ID>` or `Retired`, never deleted or renumbered.

## Rules

- A change with no recorded impact is not ready to apply.
- Impact is a proposal. Severity and acceptance belong to the PO and the team.
- If the change is already applied, run the same walk and mark the report `Retroactive`.

## Next steps

End with `➡️ **Next step:** ...`.

- Scope-changing: record a pending DEC and ask the PO (`/grill-with-docs` to settle it).
- Impacted stories exist: tell the user to run `/refine-request` on each, in dependency order.
- Vision or capability touched: invoke `review-product-vision` and, after approval, update `PRODUCT-VISION.md` through `/create-product-vision`.
- Everything re-refined: invoke `audit-traceability`, then `review-readiness`.
- Graph enabled: `/ask-req` reads the Stale frontier from it.
