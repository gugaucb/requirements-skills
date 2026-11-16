# Quality gates

## Story gates

| Gate | Pass condition |
| --- | --- |
| G1 Story | Meaningful As a / I want / So that; real actor; scope and exclusions stated |
| G2 Serves | Links to an existing CAP and GOAL; not scope-changing, or the DEC is Confirmed |
| G3 Requirements | FRs atomic and sourced; NFRs measurable or explicitly Pending |
| G4 Acceptance | Every active FR/NFR has an AC; ACs are externally observable Gherkin |
| G5 Tests | Every active AC has a TC with data, action, expected result, evidence; executable in principle |
| G6 Consistency | Diagrams, text, glossary terms agree; no duplicate or dangling IDs |
| G7 Freshness | No `Stale` upstream; open CHG items for this story are resolved |
| G8 Decisions | Every rule traces to a DEC; Pending decisions are listed with owner |
| G9 Human | Approval recorded before Ready (team agreement) |

## Vision gates

GOAL/CAP IDs unique; Confirmed statements cite PO evidence; scope, goals and audience coherent; success criteria not invented; downstream impact of revisions documented in a CHG.

## Statuses

`Draft` → `Ready for human review` → `Ready (team agreement)`. Side states: `Blocked`, `Needs changes`, `Stale` (upstream changed, see CHG), `Retired`. Neither local readiness nor the Product Vision is a mandatory Scrum artifact.
