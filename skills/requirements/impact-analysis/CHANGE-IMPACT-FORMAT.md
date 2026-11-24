# CHG-NNN format

One file per change at `<artifact-root>/05-changes/CHG-NNN.md`. IDs are never reused.

```md
# CHG-NNN: <short title>

**Status:** Proposed | Confirmed by <person, date> | Rejected | Retroactive
**Requested by:** <person or source>
**Type:** rule | scope | actor | metric | term | priority | removal
**Scope-changing:** yes | no (yes means a DEC is pending)

## Change

| ID | Before | After | Why |
| --- | --- | --- | --- |
| FR-007 | <old text> | <new text> | <reason, DEC link> |

## Impact

| ID | Relation | Classification | Action |
| --- | --- | --- | --- |
| AC-012 | downstream of FR-007 | Invalidated | Rewrite |
| TC-020 | downstream of AC-012 | Needs review | Re-derive |
| US-004 | sideways (same term "active") | Needs review | Check rule R3 |
| CAP-002 | upstream | Unaffected (checked) | Still served |

## Decisions needed

| DEC | Question | Owner |
| --- | --- | --- |
| DEC-009 | <question> | PO |

## Resolution log

- <date>: US-004 re-refined, status back to Draft.
```

Rules: list every touched ID, including Unaffected (checked). The Resolution log is appended as impacted items are re-refined; the change is closed when no row is `Stale` or `Needs review` without an entry.
