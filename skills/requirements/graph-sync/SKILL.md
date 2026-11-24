---
name: graph-sync
description: Rebuild and query the requirements knowledge graph (typed links between GOAL, CAP, SPEC, US, FR, NFR, AC, TC, DEC and CHG). Use when docs/agents/graph.md exists and artifacts changed, or when you need the dependents, dependencies or frontier of an ID without reading every file.
---

Keep a deterministic graph of the requirements artifacts in step with the Markdown, and use it to answer "what depends on X" cheaply. The Markdown stays the source of truth; the graph is derived and disposable.

Read `docs/agents/graph.md` for the artifact root and which layers are enabled. If it does not exist, the graph is off: say so and stop; the other skills work without it.

Relations, direction rule and Graphify commands: [GRAPH.md](GRAPH.md).

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- `docs/agents/graph.md` with the graph enabled
- an artifact root with at least one artifact

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Procedure

1. **Rebuild** (idempotent, no LLM, milliseconds; skips when nothing changed):

   ```bash
   python3 <this-skill-dir>/scripts/req-graph.py build <artifact-root> --view
   ```

   It writes `<artifact-root>/graph/req-graph.json` and `graph/req-graph.html` (an interactive viewer; see GRAPH.md) and lists **unresolved IDs** (referenced but never defined). Treat unresolved IDs as findings, not noise.
2. **Merge the other layers** only if enabled in `docs/agents/graph.md` and the `graphify` CLI exists: update the code layer, then merge (recipe in GRAPH.md). Never install Graphify yourself.
3. **Answer the question** with the cheapest query:
   - Dependents of an ID: `req-graph.py affected <artifact-root> <ID> --no-weak` (add `--up` for what it depends on).
   - Whole-root consistency (CI): `req-graph.py validate <artifact-root>`: exit 0 consistent, 1 orphans or untested rules, 2 cycles, 3 critical failure; also prints the Top 5 critical artifacts. `critical <artifact-root> --top N` ranks more.
   - Next stories to refine: `req-graph.py frontier <artifact-root>`. Stale stories: `req-graph.py stale <artifact-root>`.
   - Backlog progress from the operations checklists: `req-graph.py backlog <artifact-root>`. The work queue of a spec in dependency order: `req-graph.py plan <artifact-root> SPEC-NNN`.
   - Free-text question: `req-graph.py query <artifact-root> "<question>" [--type US,FR] [--status Stale] [--depth N] [--budget TOKENS]`. IDs inside the text are exact seeds.
   - How two items connect: `req-graph.py path <artifact-root> <ID> <ID>`. Everything about one item: `req-graph.py explain <artifact-root> <ID>` (links, source line, dependents).
   - Only when code or knowledge layers are merged (that is what Graphify adds): `graphify affected`, `graphify query`, `graphify path` on `merged-graph.json`.
4. **Point the user at the viewer** when they want to see the graph: `graph/req-graph.html` opens in any browser, offline.
5. **Report** counts, unresolved IDs and what changed since the last build.

The graph proposes; it does not judge. A listed dependent is a **candidate** for review, not a verdict. Statuses (`Stale`, Ready) still come from the Markdown and the humans.

## Done

The graph file is current, unresolved IDs are listed, and any answer names the IDs and the relation that links them.

## Next steps

End with `➡️ **Next step:** ...`.

- Unresolved or duplicate IDs: invoke `audit-traceability`.
- Impact of a change wanted: invoke `impact-analysis`, which uses this graph first.
- Stories on the frontier: `/refine-request US-NNN`. Unsure where you are: `/ask-req`.
