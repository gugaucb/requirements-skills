# Changelog

## 2.0.0

Breaking: skill layout, names and handoffs.

- New: `ask-req` (router that reads artifact state), `wayfinder`, `grill-me`, `grilling`, `grill-with-docs`, `to-spec`, `triage`, `impact-analysis`, `handoff`, `wait-what`, `to-questionnaire`, `research`, `retro` (26 skills).
- Change flow: `grilling` change mode ends with an impact round; `CHG-NNN` reports; `Stale` status blocks readiness; writers invoke `impact-analysis` before editing existing items.
- Every skill ends with `## Next steps`; `ask-req` lists every skill; validator enforces both.
- Renamed `model-domain` to `domain-modeling`; merged `interview-product-owner` into `grilling` and `initialize-requirements` into `setup-requirements-repo`; `split-backlog` now slices vertically with blocking edges and is user-invoked.
- New `audit-traceability/scripts/check-ids.py` deterministic check; product-wide unique IDs; new ID types `SPEC-` and `CHG-`.
- Skills are `skills/<bucket>/<name>/SKILL.md`; removed duplicated `.claude/skills` adapters and the 15-fold "Shared operating rules" block (now `docs/agents/requirements-workflow.md`); templates live inside their owning skill; `scripts/install.sh` installs into any harness.
- Docs: Portuguese De/Para, FLOW diagrams, INVOCATION, AUTHORING-SKILLS; new fictional example with a change.

## 1.2.0

Product vision skills, GOAL/CAP hierarchy, shared vocabulary, cross-agent trigger audit.
