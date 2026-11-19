# Changelog

## 2.4.0

- User story template: optional `## Screens` section (after Fields) with `SCREEN-FORMAT.md`: field groups, actions and states per screen (`SCR-NNN`), referencing `FLD-` fields. Behavior, not visual design.
- Decision rule: team **Screens policy** (`ask`, `always`, `never`) in `requirements-workflow.md`; `write-user-story` proposes Required, Not needed or Pending from triggers and the human confirms. New gate G10 in `review-readiness`; `define-acceptance-criteria` cites the screen instead of repeating the form.
- New ID types `FLD-` and `SCR-` in the vocabulary, `check-ids.py`, the graph (`part_of`, new `uses` relation) and the viewer.
- `setup-requirements-repo` section G **Versioning** (git local or remote, layout, branching and review, commit convention, what is versioned, authorization) with seed `versioning.md`; operating rule: no commit, push or PR unless asked.

## 2.3.1

- User story template: new `## Fields` table (ID, NAME, Description, Required, Type, Size, Rules); `write-user-story` fills it; example US-001 updated. `FLD-` IDs are not tracked by the graph yet.

## 2.3.0

- `req-graph.py query` (ranked free-text search with `--type`, `--status`, `--depth`, `--budget`, `--json`), `path` (shortest connection between two IDs) and `explain` (links, source line and dependents of one ID). Accent-insensitive, no LLM, no Graphify. Graphify is now only needed for code and document layers.
- `graph-sync` and `triage` use them first.

## 2.2.0

- `req-graph.py view` and `build --view`: self-contained offline HTML viewer (`graph/req-graph.html`), no CDN and no Graphify needed. Layered layout, impact highlighting identical to `affected`, status on the border, search, type and relation filters, redundant skip-level links hidden, pan and zoom, Save SVG. Deterministic output, rewritten only when artifacts change. Inspired by the feature set of `graphify export html`; code written from scratch.

## 2.1.0

- New model-invoked skill `graph-sync` and `graph-sync/scripts/req-graph.py` (`build`, `affected`, `frontier`, `stale`): deterministic typed graph of every ID, node-link JSON compatible with Graphify (`merge-graphs`, `affected`, `query`, `path`).
- Direction rule: an edge points at what its source depends on, so `graphify affected` equals downstream impact. Relations: `serves`, `part_of`, `decided_by`, `blocked_by`, `verifies`, `proves`, `references`; records: `changes`, `impacts`, `needs_decision`, `changed_by`, `superseded_by`.
- Graph-first paths in `impact-analysis`, `refine-request`, `ask-req`, `audit-traceability`, `triage`, `retro`; writers invoke `graph-sync` afterwards. All with fallbacks when the graph is off.
- `setup-requirements-repo` section F (graph: off or local, optional Graphify layers); seeds `graph.md` and `graphifyignore.template`.
- Localized section headings via `graph/aliases.json`; optional YAML frontmatter (`id`, `status`, `serves`, `blocked_by`).
- Docs: GRAPH.md, FLOW graph overlay, De/Para section 4. 27 skills.

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
