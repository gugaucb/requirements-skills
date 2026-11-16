# BACKLOG.md format

```md
# Backlog: <product>

| Order | Goal | Capability | Epic | Story | Outcome | Blocked by | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Proposed 1 | GOAL-001 | CAP-001 | | US-001 | Customer sees status of an owned order | None | Draft |
| Proposed 2 | GOAL-001 | CAP-001 | | US-002 | Customer sees status history | US-001 | Draft |
```

Rules:

- Order stays **Proposed** until the PO confirms it (then `PO-confirmed <date>`).
- `Blocked by` lists story IDs or `None`. The frontier is every story whose blockers are all Ready or done.
- Status values: Draft, Stale, Blocked, Needs changes, Ready for human review, Ready (team agreement), Retired.
- Rows are never deleted. A retired story keeps its ID and gets `Retired` plus the reason.
