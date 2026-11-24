# Traceability model

```
GOAL -> CAP -> EPIC (optional) -> US -> FR / NFR -> AC -> TC
```

`FLD` (field) and `SCR` (screen) belong to a US; a SCR `uses` FLD, so changing a field impacts its screens. `DG` (diagram) may support a US, FR or AC. `DEC` may justify any node. `SPEC` groups candidate stories for a feature. `CHG` records a change and its impact.

- Higher-level relations live in `PRODUCT-VISION.md`, `03-specs/` and `BACKLOG.md`.
- The lower-level **authoritative matrix** lives in each `US-NNN.md` (section "Canonical traceability"). One source of truth: do not duplicate it elsewhere.
- IDs are unique and immutable **product-wide** (FR-004 exists once, not once per story). Allocate the next free number. Retired items keep their ID.
- A CAP may link straight to stories without an epic.
- Readiness needs every active FR/NFR linked to an AC and every AC to a TC.

## Change and staleness

When an item changes, everything downstream and anything sharing its terms is **impacted** (see `impact-analysis`). Impacted items are marked `Stale` until re-refined; the `CHG-NNN` file records the walk and a resolution log. A `Stale` item blocks readiness.

## Limits

Matching ID tokens proves a link exists, not that it is true. Semantic coverage is a human and agent judgement.
