---
name: review-product-vision
description: Review a product vision for consistent vocabulary, unapproved assumptions, scope contradictions, measurable goals and coverage of capabilities. Use when asked to assess or approve a draft vision for human review.
---

Inspect `PRODUCT-VISION.md`, `DECISIONS.md` and `GLOSSARY.md`, using the vision gates in `review-readiness/QUALITY-GATES.md`.

## Procedure

1. Check every GOAL and CAP for evidence, coherent scope, observable value, unanswered dependencies, overlap, duplicate IDs, contradictions and coverage (each goal has a capability; each capability serves a goal).
2. Check vocabulary against the glossary and every "Confirmed" claim against PO evidence.
3. Report a findings table: finding, ID, severity, PO decision needed.
4. Do not turn AI judgement into acceptance. When asked to fix, apply changes as **Proposed** with a version note, after `impact-analysis` if stories already exist.

## Done

Every finding names an ID and an owner; the report states plainly whether human approval is still required.

## Next steps

End with `➡️ **Next step:** ...`. Findings: `/grill-with-docs` to settle them, or `/create-product-vision` to revise. Clean: ask the PO to approve, record it as a DEC, then `/to-spec`.
