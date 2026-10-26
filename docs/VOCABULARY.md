# Vocabulary underneath — shared requirements language

| Term | Definition | Not the same as |
| --- | --- | --- |
| Product Vision | PO-aligned description of problem, audience, desired future and scope, evolving with evidence | Fixed technical specification |
| Product Goal (`GOAL-`) | Named objective a product seeks to meet; unique in the product | Individual feature |
| Capability (`CAP-`) | Coherent business ability the proposed product must enable | UI screen or component |
| Epic (`EPIC-`) | Optional grouping of user stories delivering a broader outcome | Mandatory Scrum artifact |
| User Story (`US-`) | Negotiable slice of end-user value in As a / I want / So that format | Task list |
| Functional Requirement (`FR-`) | Observable behavior under conditions | Implementation instruction |
| Non-functional Requirement (`NFR-`) | Measurable quality constraint with verification conditions | Vague adjective |
| Acceptance Criterion (`AC-`) | Verifiable business acceptance expressed as Gherkin scenario | Test case |
| Test Case (`TC-`) | Preconditions, operation and evidence proving an AC | AC itself |
| Diagram (`DG-`) | Optional visual clarification of confirmed behavior | Source of invented rules |
| Decision (`DEC-`) | Human-approved or explicitly pending business choice | AI inference |
| Traceability | Verifiable relationship between upstream intention and downstream acceptance | Simple keyword overlap |
| Definition of Ready | Optional team agreement about suitability for refinement/planning | Official required Scrum commitment |
| Definition of Done | Scrum quality commitment for a product Increment | Review status of a HU |

IDs are unique and immutable within the configured product scope. A source must carry its status (`Confirmed`, `Proposed`, `Pending`) and origin. A product's own business vocabulary lives in `GLOSSARY.md`; this file is the shared **process** vocabulary, not a substitute for it.
