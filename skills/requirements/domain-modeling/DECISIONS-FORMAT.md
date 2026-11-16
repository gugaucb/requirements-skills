# DECISIONS.md format

A decision is a business choice that shapes scope, rules or quality. It is a row, not an essay.

```md
| ID | Question / decision | Status | Accountable | Evidence | Affected IDs |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | Which order statuses exist? | Confirmed | Ana (PO), 2026-05-02 | meeting notes, ticket link | CAP-001, US-001 |
| DEC-002 | Is partial cancellation allowed? | Pending | PO | | US-003 |
```

Rules:

- IDs are unique and immutable. Never delete; a reversed decision gets `Superseded by DEC-NNN`.
- **Confirmed** needs the accountable human and a source. An AI inference is at most **Proposed**.
- Record the _why_ in one sentence when the choice is hard to reverse, surprising without context, and a real trade-off. Otherwise the row is enough.
- Detail stays where it lives (a wayfinder ticket, a CHG file, a questionnaire). The row points there.
