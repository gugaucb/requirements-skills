---
name: to-spec
description: Turn the current conversation into a requirements spec for one feature or capability. No interview, just synthesis of what was already discussed.
disable-model-invocation: true
---

Take the conversation, the approved or draft `PRODUCT-VISION.md`, `GLOSSARY.md` and `DECISIONS.md`, and produce one **spec**. Do NOT interview the user; synthesise what you already know. Gaps become Pending decisions, never invented content.

Read `docs/agents/requirements-workflow.md` for the artifact root, language and tracker. If it is missing, tell the user to run `/setup-requirements-repo`.

## Process

1. **Gather.** Read the vision, glossary, decisions and any existing stories in the area. Use glossary vocabulary throughout. Respect Confirmed decisions; flag any contradiction explicitly.
2. **Place it.** Link the spec to the `GOAL` and `CAP` IDs it serves. A feature that serves no capability is scope-changing: say so and stop for a PO decision.
3. **Write** `<artifact-root>/specs/SPEC-<NNN>-<slug>.md` using the template below. Status `Draft`.
4. **Check the boundary** with the user in one short exchange: capabilities touched, what is out of scope, which stories look too big. Edit and finish.

<spec-template>

# SPEC-NNN: <title>

**Status:** Draft | **Serves:** GOAL-XXX, CAP-XXX | **Epic (optional):** EPIC-XXX

## Problem

The problem from the user's perspective. Evidence and source.

## Outcome

What the user can do afterwards, from their perspective.

## Actors

Role, need, status (Confirmed, Proposed, Pending).

## Candidate stories

A numbered list. Titles only, in the form: As a <actor>, I want <capability>, so that <benefit>. Cover the feature broadly; `/split-backlog` slices and orders them.

## Business rules

Rule, source (DEC ID), status. Only what was discussed.

## Quality constraints

Candidate NFRs with metric if agreed, otherwise Pending.

## Out of scope

Confirmed exclusions and why.

## Open questions

Pending decisions with owner and the IDs they block.

</spec-template>

If `docs/agents/graph.md` exists, invoke the `graph-sync` skill after writing.

## Done

The file exists, every rule has a source and a status, and every open question has an owner.

## Next steps

End with `➡️ **Next step:** ...`.

- Spec accepted: `/split-backlog` to slice it into vertical stories.
- Open questions block most of it: `/grill-with-docs` or `/to-questionnaire`.
- The spec is really a whole product: `/create-product-vision`.
