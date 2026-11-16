---
name: specify-requirements
description: Write atomic functional requirements and measurable non-functional requirements into a story's tables, with evidence and source decisions. Use when elaborating story behavior and constraints.
---

Derive requirements from the story and its Confirmed decisions. Read the story file and `DECISIONS.md`. If the story is being altered, invoke `impact-analysis` first (see `write-user-story`).

## Procedure

1. **FRs**: one observable behavior per row, under stated conditions, in business words. Atomic: if the row contains "and", split it. No design prescriptions without a reason.
2. **NFRs**: each has metric, target, workload, environment, verification method and accountable source. A quality word without a number ("fast", "secure") is not an NFR. Without a confirmed number keep it **Pending**; invent no thresholds.
3. **Source each row** with a DEC ID and status. A behavior no one decided is **Proposed** with an open DEC.
4. **Sweep** for what is usually missing: permissions, empty states, failures, limits, audit, data retention, accessibility. Add only what the sources support; raise the rest as Pending questions.

## Done

Every FR is atomic and sourced; every NFR is measurable or Pending; no requirement duplicates another.

## Next steps

End with `➡️ **Next step:** ...`. Normally invoke `define-acceptance-criteria`. Missing decisions: invoke `grilling`. Terms unclear: invoke `domain-modeling`.
