---
name: write-user-story
description: Create or revise a classic As a / I want / So that user story file with explicit scope, exclusions and links to goals and capabilities. Use when expressing a user outcome or when an existing story is altered.
---

Write one story as the single source for its requirements, Gherkin, tests and matrix. Read `docs/agents/requirements-workflow.md` (language, ID scope), `GLOSSARY.md` and the linked `CAP`/`EPIC`/spec.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/requirements-workflow.md`
- `<artifact-root>/02-backlog/BACKLOG.md` (the story row)
- `<artifact-root>/01-vision/PRODUCT-VISION.md`
- `<artifact-root>/shared/GLOSSARY.md`
- `<artifact-root>/shared/DECISIONS.md`

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Create

1. Take the story's row from `BACKLOG.md`. If none exists, the request is not yet sliced: tell the user to run `/split-backlog`.
2. Write `As a <role>, I want <observable capability>, so that <business value>.` Use glossary terms; the role is a real actor.
3. **Decide Screens** (below), then fill the **Fields** table (one row per data field the story reads or writes: name, description, required, type, size, rules citing DEC/FR IDs); write `No fields` when the story handles no data. Fill **Scope and rules** with Confirmed decisions (cite DEC IDs) and **Pending** questions; list explicit exclusions.
4. Save `<artifact-root>/04-stories/US-NNN.md` from [USER-STORY-TEMPLATE.md](USER-STORY-TEMPLATE.md). Never recycle an ID. Status `Draft`.

A story that is a task list, a screen, or a technical layer is not a story. Technical-only stories need an explicit enablement purpose agreed by stakeholders.

### Minimal examples (full rules in [SCREEN-FORMAT.md](SCREEN-FORMAT.md))

| ID | NAME | Description | Required | Type | Size | Rules |
| --- | --- | --- | --- | --- | --- | --- |
| FLD-001 | orderId | Identifier of the order | Yes | String | 36 | Must belong to the signed-in owner (FR-002) |

```md
### SCR-001: Order status page
**Actor:** Owner | **Entry:** "My orders", then select an order
| Order | Group | Field | Label | Control | Mask / format | Editable | Visible when | Notes |
| 1 | Order | FLD-001 | Order number | text | | No | always | Copy button |
| Action | Label | Enabled when | Result |
| Back | Back to my orders | always | Returns to the list |
| State | Condition | Behavior and message |
| Not found | order not owned by the signed-in owner | shows "Order not found" and no data |
```

Lifecycle header on every story: `status: draft | review | approved | deprecated` and `version: X.Y.Z` in the YAML frontmatter. It is the coarse lifecycle; the detailed `**Status:**` line keeps its values and must agree:

| Frontmatter `status` | `**Status:**` values it covers |
| --- | --- |
| `draft` | Draft, Blocked, Needs changes, Stale |
| `review` | Ready for human review |
| `approved` | Ready (team agreement) |
| `deprecated` | Retired |

`version` starts at `0.1.0`. Bump the patch for wording, the minor when behavior is added or changed (a new or changed FR or AC), the major when scope or actor change; `1.0.0` at first approval. Record each bump in the change history. `req-graph.py validate` reports a mismatch or a malformed version as a `[PARSE-WARNING]`.

## Decide Screens

Read **Screens policy** in `docs/agents/requirements-workflow.md` (`ask` by default). The decision belongs to the human; you propose.

- Policy `never`: write `No screens: policy`. Policy `always`: a story with a human actor and interface gets a screen.
- Policy `ask`: apply the triggers and **propose** `Required`, `Not needed` or `Pending`, with one line of reasoning; the user confirms or overrides.

**Include** when a human uses an interface to fill in or read data (form, list with filters, dashboard, multi-step flow), when Fields has user-facing inputs or outputs, or when the story will be built or generated from this text. **Do not include** for API, batch, integration or background work, for pure rules or calculations, or when the screen already exists (reference its `SCR-` ID and describe the difference). If triggers conflict, write `Pending: <question>` and ask.

Write the section using [SCREEN-FORMAT.md](SCREEN-FORMAT.md). Fields come first: every field a screen shows has a `FLD-` row.

## Revise (change mode)

Before editing an existing story, invoke the `impact-analysis` skill unless a CHG for this change already exists in the session. Then edit in place: keep the ID, retire replaced content as `Superseded by`, add a line to **Change history** with the CHG reference, and set affected downstream rows to `Stale`.

## Done

The story has role, capability, benefit, serves-links, scope, exclusions, a Fields table, a Screens decision (screens, `No screens` or a Pending question) and a status; no rule lacks a source or a Pending tag.

## Next steps

End with `➡️ **Next step:** ...`. Normally invoke `specify-requirements`. If the story is too big: `/split-backlog`. If rules are undecided: invoke `grilling`.
