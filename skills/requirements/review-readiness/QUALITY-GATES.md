# Quality gates

## Story gates

| Gate | Pass condition | Return to when it fails |
| --- | --- | --- |
| G1 Story | Meaningful As a / I want / So that; real actor; scope and exclusions stated | `write-user-story` |
| G2 Serves | Links to an existing CAP and GOAL; not scope-changing, or the DEC is Confirmed | `/grill-with-docs`, then `/split-backlog` or `/create-product-vision` |
| G3 Requirements | FRs atomic and sourced; NFRs measurable or explicitly Pending | `specify-requirements` |
| G4 Acceptance | Every active FR/NFR has an AC; ACs are externally observable Gherkin | `define-acceptance-criteria` |
| G5 Tests | Every active AC has a TC with data, action, expected result, evidence; executable in principle | `design-test-scenarios` |
| G6 Consistency | Diagrams, text, glossary terms agree; no duplicate or dangling IDs | `domain-modeling` |
| G7 Freshness | No `Stale` upstream; open CHG items for this story are resolved | `refine-story` or `/apply-spec` |
| G8 Decisions | Every rule traces to a DEC; Pending decisions are listed with owner | `/grill-with-docs` |
| G10 Screens | Screens decision recorded: screens specified, `No screens: <reason>`, never left `Pending`; screen fields exist in Fields; ACs do not duplicate the form | `write-user-story` |
| G9 Human | Approval recorded before Ready (team agreement) | the PO (record the approval as a DEC) |

## Vision gates

GOAL/CAP IDs unique; Confirmed statements cite PO evidence; scope, goals and audience coherent; success criteria not invented; downstream impact of revisions documented in a CHG.

## Statuses

`Draft` → `Ready for human review` → `Ready (team agreement)`. Side states: `Blocked`, `Needs changes`, `Stale` (upstream changed, see CHG), `Retired`. Neither local readiness nor the Product Vision is a mandatory Scrum artifact.

## Verdicts

`PASS`, `NEEDS CHANGES` (mechanical fix, status `Needs changes`) and `BLOCKED` (a decision or input is missing, status `Blocked`). Every non-PASS finding names its return route; the route is also tabulated in `docs/FLOW.md`.
