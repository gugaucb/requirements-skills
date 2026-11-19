---
name: define-acceptance-criteria
description: Write externally observable acceptance criteria in Gherkin Given / When / Then using the configured locale. Use for defining acceptance of story requirements.
---

Read the story, its FR/NFR and the configured output language in `docs/agents/requirements-workflow.md`. Gherkin keywords follow the locale (for pt-BR: `Funcionalidade`, `Cenário`, `Dado`, `Quando`, `Então`). If the story is being altered, invoke `impact-analysis` first.

## Procedure

1. Give each verifiable business condition a unique `AC-NNN` and one `Scenario`.
2. Cover, where material: the happy path, permission denial, empty state, failure, and boundary values. Use `Scenario Outline` with examples for rule variations.
3. Express **business outcomes**, observable from outside. No clicks, no endpoints, no database state.
   - When the story has `## Screens`, cite the screen (`SCR-NNN`) and fields by name and keep only the scenario's **sample values** in the AC. Do not re-specify the form (order, masks, visibility, enabled rules); that lives in the screen.
4. Every FR maps to at least one AC; every AC cites the FR/NFR it proves. Update the story's matrix.
5. Keep ACs consistent with requirements. A conflict is a Pending question, not a quiet fix. A proposed rule never reads as approved.

## Done

Each FR has an AC; each AC has Given/When/Then with concrete, checkable outcomes; negative cases are present or explicitly out of scope.

## Next steps

End with `➡️ **Next step:** ...`. Normally invoke `design-test-scenarios`. Rules contradict: invoke `grilling`.
