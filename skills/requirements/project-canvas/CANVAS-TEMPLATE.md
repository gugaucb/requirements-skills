# Project Model Canvas: [Project]

**Status:** Draft (requires sponsor validation) | **Sponsor:** [person or Pending] | **Evidence:** [narrative, minutes]

Every post-it is a row with an ID. **Traces to** lists what the item depends on (its justification, product part, delivery...). A rule can be waived for one row with `[waive C5: reason]`; waivers need the sponsor's acknowledgement.

## 1. Justifications (the past: pain and problem)

| ID | Justification | Evidence | Traces to |
| --- | --- | --- | --- |
| JUS-001 | [problem or pain] | [data, ticket log] | |

## 2. Product (what will exist)

| ID | Product item or characteristic | Traces to (OBJ) |
| --- | --- | --- |
| PRD-001 | [part of the final product] | OBJ-001 |

## 3. SMART objectives (the future)

| ID | Objective | Measure | Deadline | Traces to (JUS) |
| --- | --- | --- | --- | --- |
| OBJ-001 | [specific, measurable, achievable, relevant, time-bound] | [metric] | [date] | JUS-001 |

## 4. Benefits (the value)

| ID | Benefit | Traces to (JUS, OBJ) |
| --- | --- | --- |
| BEN-001 | [concrete benefit] | JUS-001, OBJ-001 |

## 5. Requirements (attributes, service levels, compliance of the product)

| ID | Requirement | Traces to (PRD, STK) |
| --- | --- | --- |
| RQT-001 | [attribute of the final product, never an activity] | PRD-001, STK-001 |

## 6. Stakeholders and external factors

| ID | Stakeholder | Expectation | Power | Attitude | Traces to |
| --- | --- | --- | --- | --- | --- |
| STK-001 | [who] | [what they expect] | [High/Medium/Low] | [Favorable/Neutral/Opposed] | |

## 7. Assumptions

| ID | Assumption (taken as true, outside your control) | Impact | Traces to |
| --- | --- | --- | --- |
| PRM-001 | [assumption] | [High/Medium/Low] | |

## 8. Delivery groups (visual WBS)

| ID | Delivery group | Traces to (PRD) |
| --- | --- | --- |
| ENT-001 | [group of deliveries] | PRD-001 |

## 9. Risks

| ID | Risk | Impact | Mitigation | Traces to (PRM, STK) |
| --- | --- | --- | --- | --- |
| RSK-001 | [what may go wrong] | [High/Medium/Low] | [response plan] | PRM-001 |

## 10. Timeline

| ID | Milestone or period | Date | Traces to (ENT, RSK) |
| --- | --- | --- | --- |
| TMP-001 | [milestone] | [date] | ENT-001 |

## 11. Team

| ID | Role or competence | Traces to (ENT) |
| --- | --- | --- |
| EQP-001 | [competence] | ENT-001 |

## 12. Costs

| ID | Cost item | Amount | Traces to (ENT, EQP, RSK) |
| --- | --- | --- | --- |
| CST-001 | [item] | [value] | ENT-001, EQP-001 |

## 13. Constraints (non-negotiable limits)

| ID | Constraint | Limit |
| --- | --- | --- |
| RST-001 | [legal date, budget cap, hiring ban] | [value] |

## Integrity review

- Mechanical rules: `canvas-check.py` result and waivers acknowledged by: [person, date].
- Judgment checks (J1 to J6) answered with the sponsor: [notes].

## Approval and change history

- Sponsor signoff: not recorded.
