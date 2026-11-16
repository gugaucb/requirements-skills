---
name: diagram-requirements
description: Create Mermaid flow, state or sequence diagrams when needed to clarify a user journey or business rule. Use only for meaningful complexity.
---

Prefer no diagram for a simple single outcome; write `Not needed` in the story. Draw when branches, states or actor hand-offs cause ambiguity.

## Procedure

1. Pick the form: `flowchart` (decisions, journeys), `stateDiagram-v2` (lifecycle), `sequenceDiagram` (actor interactions).
2. Draw only **Confirmed or Proposed** behavior from the story. Never add a business branch nobody stated; an unclear branch is a Pending question.
3. Label with IDs (`FR-003`, `AC-004`) and glossary terms. Save as `DG-NNN` in the story or under `diagrams/`.
4. Check the Mermaid syntax and resolve contradictions between text and diagram.

## Done

Every branch or state in the diagram traces to a requirement or AC, and nothing in the diagram is missing from the text.

## Next steps

End with `➡️ **Next step:** ...`. Invoke `audit-traceability`, then `review-readiness`.
