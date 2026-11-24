# BACKLOG.md format

The backlog is the WBS (EAP) of the product: capability, optional epic, story. One table row per story, then one **operations** block per story.

```md
# Backlog: <product>

| Order | Capability | Epic | Story | Name | Blocked by | Status | Progress |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Proposed 1 | CAP-001 | EPIC-001 Customer registry | US-001 | Maintain customer | None | Draft | Pending |
| Proposed 2 | CAP-001 | EPIC-001 Customer registry | US-002 | Import customers | US-001 | Draft | Pending |

## Operations

### US-001: Maintain customer

- [ ] include customer: register a new customer with the mandatory data
- [ ] edit customer: change the data of an existing customer
- [ ] remove customer: deactivate a customer that has no open orders
- [ ] consult customer: search and view customers
```

When a requirement, criterion and test cover an operation, `refine-story` ticks it and records the IDs: `- [x] edit customer (FR-004, AC-004, TC-004)`.

## Rules

- **Status** is the lifecycle of the story: Draft, Stale, Blocked, Needs changes, Ready for human review, Ready (team agreement), Retired.
- **Progress** is derived from the checklist: `Pending` (nothing ticked), `In progress`, `Done` (all ticked). `req-graph.py backlog` recomputes it and flags a row whose Progress column or Ready status disagrees with its checklist.
- The first `US-` ID in a row owns the row; later `US-` IDs in the row are blockers. A `CAP-` in the row says which capability the story serves; an `EPIC-NNN Name` cell declares the epic on first use.
- Order stays **Proposed** until the PO confirms it (then `PO-confirmed <date>`).
- `Blocked by` lists story IDs or `None`. The frontier is every story whose blockers are all Ready or done.
- Rows are never deleted. A retired story keeps its ID and gets `Retired` plus the reason. Operations are never deleted; a dropped one is marked `[x] ~~operation~~ (dropped: reason)`.
