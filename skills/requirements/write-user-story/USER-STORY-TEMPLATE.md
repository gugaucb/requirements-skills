---
id: US-XXX
status: draft      # draft | review | approved | deprecated
version: 0.1.0     # X.Y.Z
---
# US-XXX: Outcome

**Serves:** GOAL-XXX, CAP-XXX (optional EPIC-XXX, SPEC-XXX)
**Status:** Draft

> As a [role], I want [observable capability], so that [business value].

## Scope and rules

[Confirmed decisions with DEC IDs, and explicit Pending questions.]

**Out of scope:** [Explicit exclusions.]

## Fields

| ID | NAME | Description | Required | Type | Size | Rules |
| --- | --- | --- | --- | --- | --- | --- |
| FLD-XXX | [field name] | [what it holds] | [Yes/No] | [String, Number, Date, Enum...] | [max length or range] | [validation, format, DEC or FR IDs] |

## Screens

> Optional, decided per story (see `write-user-story`). Describe behavior, not visual design. Write `No screens: <reason>` for a story without a user interface, or `Pending: <question>` while undecided.

### SCR-XXX: [Screen name]

**Actor:** [role] | **Entry:** [how the user gets here]

| Order | Group | Field | Label | Control | Mask / format | Editable | Visible when | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [group] | FLD-XXX | [label shown] | [text, select, date, file...] | [mask] | [Yes/No] | [always / condition] | [help text] |

| Action | Label | Enabled when | Result |
| --- | --- | --- | --- |
| [Submit] | [button text] | [all required fields valid] | [FR-XXX, AC-XXX] |

| State | Condition | Behavior and message |
| --- | --- | --- |
| [Empty / Error / Success / Loading] | [when it shows] | [what the user sees] |

## Functional requirements

| ID | Behavior | Source / status |
| --- | --- | --- |
| FR-XXX | [Observable behavior under conditions] | [DEC-XXX, Confirmed] |

## Non-functional requirements

| ID | Metric / limit | Workload, environment, method | Source / status |
| --- | --- | --- | --- |
| NFR-XXX | [Agreed metric, or "No story-specific NFR"] | [Conditions] | [Pending] |

## Acceptance criteria

**AC-XXX**
```gherkin
Scenario: Verifiable outcome
  Given a documented condition
  When an action occurs
  Then the expected result is observable
```

## Test scenarios

| ID | Setup / data | Action | Expected result / evidence |
| --- | --- | --- | --- |
| TC-XXX | [Setup] | [Event] | [Assertion] |

## Canonical traceability

| US | Requirement | AC | TC | Coverage rationale |
| --- | --- | --- | --- | --- |
| US-XXX | FR-XXX | AC-XXX | TC-XXX | [Evidence] |

## Diagrams and decisions

[Link, or "Not needed".]

## Change history

| Date | CHG | What changed | Status effect |
| --- | --- | --- | --- |

## Readiness and signoff

Draft; human validation not recorded.
