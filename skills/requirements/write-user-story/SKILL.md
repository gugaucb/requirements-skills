---
name: write-user-story
description: Create or revise a classic As a / I want / So that user story file with explicit scope, exclusions and links to goals and capabilities. Use when expressing a user outcome or when an existing story is altered.
---

Write one story as the single source for its requirements, Gherkin, tests and matrix. Read `docs/agents/requirements-workflow.md` (language, ID scope), `GLOSSARY.md` and the linked `CAP`/`EPIC`/spec.

## Create

1. Take the story's row from `BACKLOG.md`. If none exists, the request is not yet sliced: tell the user to run `/split-backlog`.
2. Write `As a <role>, I want <observable capability>, so that <business value>.` Use glossary terms; the role is a real actor.
3. Fill **Scope and rules** with Confirmed decisions (cite DEC IDs) and **Pending** questions; list explicit exclusions.
4. Save `<artifact-root>/stories/US-NNN.md` from [USER-STORY-TEMPLATE.md](USER-STORY-TEMPLATE.md). Never recycle an ID. Status `Draft`.

A story that is a task list, a screen, or a technical layer is not a story. Technical-only stories need an explicit enablement purpose agreed by stakeholders.

## Revise (change mode)

Before editing an existing story, invoke the `impact-analysis` skill unless a CHG for this change already exists in the session. Then edit in place: keep the ID, retire replaced content as `Superseded by`, add a line to **Change history** with the CHG reference, and set affected downstream rows to `Stale`.

## Done

The story has role, capability, benefit, serves-links, scope, exclusions and a status; no rule lacks a source or a Pending tag.

## Next steps

End with `➡️ **Next step:** ...`. Normally invoke `specify-requirements`. If the story is too big: `/split-backlog`. If rules are undecided: invoke `grilling`.
