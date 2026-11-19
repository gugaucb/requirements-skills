# Screens format

One block per screen inside `## Screens` of the story. A screen describes **what the user can see and do**, so a developer or an AI can build it. It is not visual design: no colors, pixels or layout engines.

```md
### SCR-NNN: Submit billing document

**Actor:** Supplier | **Entry:** Menu "Billing" then "New submission"

| Order | Group | Field | Label | Control | Mask / format | Editable | Visible when | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Contract | FLD-010 | Linked contract | select | | Yes | always | Only active contracts |
| 2 | Document | FLD-011 | Document number | text | digits only | Yes | always | |

| Action | Label | Enabled when | Result |
| --- | --- | --- | --- |
| Submit | Submit | all required fields valid and file attached | FR-021, AC-072 |

| State | Condition | Behavior and message |
| --- | --- | --- |
| Error | file fails antivirus scan | shows "File rejected"; keeps the form data |
| Success | protocol issued | shows the protocol number and a receipt download button |
```

Optional sketch (keep it under 25 lines; the tables are the contract):

```text
+-----------------------------+
| Linked contract  [ v ]      |
| Document number [        ]  |
| [Attach file]   [ Submit ]  |
+-----------------------------+
```

## Rules

- **Reference fields by `FLD-` ID.** Type, size and validation live in `## Fields`; do not repeat them here. Add only what belongs to the screen: order, group, label, control, mask, editable, visibility.
- **One source of truth.** ACs cite the screen (`SCR-NNN`) and field names, and keep only the scenario's sample values. They do not re-specify the form.
- **States** cover at least empty, error and success where they apply.
- Labels and messages are written in the configured output language.
- A screen that already exists from another story is referenced by its `SCR-` ID; describe only the difference.
- IDs are product-wide and immutable; a retired screen is marked `Retired`.
