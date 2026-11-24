# Project Model Canvas: Order Status Portal (fictional)

**Status:** Draft. No real sponsor approved this sample. | **Sponsor:** Fictional sponsor | **Evidence:** fictional kickoff

## 1. Justifications

| ID | Justification | Evidence | Traces to |
| --- | --- | --- | --- |
| JUS-001 | Customers phone support to ask where their order is | support ticket log | |

## 2. Product

| ID | Product item or characteristic | Traces to (OBJ) |
| --- | --- | --- |
| PRD-001 | Order status page for signed-in owners | OBJ-001 |
| PRD-002 | Order status history | OBJ-001 |

## 3. SMART objectives

| ID | Objective | Measure | Deadline | Traces to (JUS) |
| --- | --- | --- | --- | --- |
| OBJ-001 | Cut status-related support contacts by 40% | contacts per 1,000 orders | 6 months after launch | JUS-001 |

## 4. Benefits

| ID | Benefit | Traces to (JUS, OBJ) |
| --- | --- | --- |
| BEN-001 | Lower support cost | JUS-001, OBJ-001 |

## 5. Requirements

| ID | Requirement | Traces to (PRD, STK) |
| --- | --- | --- |
| RQT-001 | Status is visible only to the order owner | PRD-001, STK-001 |
| RQT-002 | Status page answers within 2 seconds at the 95th percentile | PRD-001, STK-002 |

## 6. Stakeholders and external factors

| ID | Stakeholder | Expectation | Power | Attitude | Traces to |
| --- | --- | --- | --- | --- | --- |
| STK-001 | Customers | See their order status without calling | Low | Favorable | |
| STK-002 | Support team | Fewer status calls | Medium | Favorable | |
| STK-003 | Fraud team | Orders under review are never shown as shipped | High | Neutral | |

## 7. Assumptions

| ID | Assumption | Impact | Traces to |
| --- | --- | --- | --- |
| PRM-001 | The order system publishes status events on time | High | |

## 8. Delivery groups

| ID | Delivery group | Traces to (PRD) |
| --- | --- | --- |
| ENT-001 | Status page | PRD-001 |
| ENT-002 | Status history | PRD-002 |

## 9. Risks

| ID | Risk | Impact | Mitigation | Traces to (PRM, STK) |
| --- | --- | --- | --- | --- |
| RSK-001 | Order system does not publish events on time | High | Poll the order system as a fallback | PRM-001 |
| RSK-002 | Fraud team delays approval of the "On hold" rule | Medium | Agree a review date at kickoff | STK-003 |

## 10. Timeline

| ID | Milestone or period | Date | Traces to (ENT, RSK) |
| --- | --- | --- | --- |
| TMP-001 | Status page live | 2026-09-30 | ENT-001 |
| TMP-002 | Status history live | 2026-11-15 | ENT-002 |
| TMP-003 | Contingency buffer, 3 weeks | before 2026-12-15 | RSK-001 |

## 11. Team

| ID | Role or competence | Traces to (ENT) |
| --- | --- | --- |
| EQP-001 | Backend developer | ENT-001, ENT-002 |
| EQP-002 | UX designer | ENT-001 |

## 12. Costs

| ID | Cost item | Amount | Traces to (ENT, EQP, RSK) |
| --- | --- | --- | --- |
| CST-001 | Development effort | 400 hours | ENT-001, ENT-002, EQP-001, EQP-002 |
| CST-002 | Contingency reserve, 15% | 60 hours | RSK-001 |

## 13. Constraints

| ID | Constraint | Limit |
| --- | --- | --- |
| RST-001 | Launch before the fraud rule deadline | 2026-12-15 |

## Integrity review

- Mechanical rules: PASS. Judgment checks J1 to J6: not answered (sample).

## Approval and change history

- Sponsor signoff: not recorded.
