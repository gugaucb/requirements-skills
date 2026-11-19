---
name: write-user-story
description: Create or revise a classic As a / I want / So that user story file with explicit scope, exclusions and links to goals and capabilities. Use when expressing a user outcome or when an existing story is altered.
---

Write one story as the single source for its requirements, Gherkin, tests and matrix. Read `docs/agents/requirements-workflow.md` (language, ID scope), `GLOSSARY.md` and the linked `CAP`/`EPIC`/spec.

## Create

1. Take the story's row from `BACKLOG.md`. If none exists, the request is not yet sliced: tell the user to run `/split-backlog`.
2. Write `As a <role>, I want <observable capability>, so that <business value>.` Use glossary terms; the role is a real actor.
3. **Decide Screens** (below), then fill the **Fields** table (one row per data field the story reads or writes: name, description, required, type, size, rules citing DEC/FR IDs); write `No fields` when the story handles no data. Fill **Scope and rules** with Confirmed decisions (cite DEC IDs) and **Pending** questions; list explicit exclusions.
4. Save `<artifact-root>/stories/US-NNN.md` from [USER-STORY-TEMPLATE.md](USER-STORY-TEMPLATE.md). Never recycle an ID. Status `Draft`.

A story that is a task list, a screen, or a technical layer is not a story. Technical-only stories need an explicit enablement purpose agreed by stakeholders.

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
