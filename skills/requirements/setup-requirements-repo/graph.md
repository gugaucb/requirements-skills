# Knowledge graph

**Status:** <off | local>
**Artifact root:** `artifacts/<product>/`

## Layers

| Layer | Enabled | How |
| --- | --- | --- |
| Requirements | <yes/no> | `python3 <graph-sync>/scripts/req-graph.py build <artifact-root>` (deterministic, no LLM) |
| Code (Graphify) | <yes/no> | `graphify update <code-root>`, then `graphify merge-graphs` (see graph-sync/GRAPH.md) |
| Knowledge (Graphify) | <yes/no> | `graphify extract <research-folder>`; sends documents to the configured LLM backend |

## Rules

- Markdown artifacts remain the source of truth; the graph is derived and never edited by hand.
- Rebuild after any skill that writes artifacts (`graph-sync`).
- Structured artifacts stay out of the LLM pass (`.graphifyignore`).
- Pinned Graphify version: <e.g. graphifyy 0.9.x, or "not used">.
- Localized headings: `<artifact-root>/graph/aliases.json` (see GRAPH.md).
