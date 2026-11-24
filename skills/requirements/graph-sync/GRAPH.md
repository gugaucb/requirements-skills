# Requirements graph

Derived, deterministic, rebuilt from the Markdown. Node-link JSON compatible with Graphify (`merge-graphs`, `affected`, `query`, `path`, `explain`). Tested with `graphifyy` 0.9.x; pin the version you use.

## The one rule

**An edge points at what its source depends on** (dependent to dependency). Impact therefore flows against the arrow, which is exactly what `graphify affected` follows. Upstream (what X depends on) is the forward direction.

## Nodes

One per ID: `GOAL`, `CAP`, `EPIC`, `SPEC`, `PLN` (plan line), `US`, `FR`, `NFR`, `AC`, `TC`, `DG`, `FLD`, `SCR`, `DEC`, `CHG`, and the canvas types `JUS`, `OBJ`, `BEN`, `PRD`, `RQT`, `STK`, `PRM`, `ENT`, `RSK`, `TMP`, `CST`, `EQP`, `RST`. Node `id` is the lowercased ID (`fr_003`), `label` is `FR-003: text` (Graphify finds it by label), plus `req_type`, `req_id`, `req_status` (story, spec, change and decision statuses) and `source_file` / `source_location`.

## Relations (all `EXTRACTED`: explicit in a table row or header)

| Relation | From to | Read from | Propagates impact |
| --- | --- | --- | --- |
| `serves` | CAP, US, SPEC to GOAL, CAP | `**Serves:**` header, vision and backlog rows | yes |
| `part_of` | FR, NFR, AC, TC, DG, FLD, SCR to US; PLN to SPEC; US to SPEC, EPIC | the story file; headers; backlog | yes |
| `decided_by` | any to DEC | source columns, rules prose; `Affected IDs` column of `DECISIONS.md` (reversed) | yes |
| `blocked_by` | US to US; PLN to PLN | `Blocked by` of `BACKLOG.md`; `Depends on` of a spec plan | yes |
| `verifies` | AC to FR, NFR | canonical traceability matrix | yes |
| `proves` | TC to AC | canonical traceability matrix | yes |
| `traces_to` | canvas item to what it depends on (OBJ to JUS, ENT to PRD...); GOAL and CAP to their canvas origin | the "Traces to" column of `PROJECT-CANVAS.md`; the Origin column of the vision | yes |
| `uses` | SCR to FLD | field IDs inside a `### SCR-NNN` block | yes (a field change impacts its screens) |
| `references` | any to any | other ID mentions | weak (hide with `--no-weak`) |
| `plans` | PLN to the artifact it changes | the Target cell of the spec plan | no (record) |
| `changes`, `impacts`, `needs_decision` | CHG to ID | tables of `05-changes/CHG-NNN.md`; `impacts` carries `impact` = Invalidated, Needs review or Unaffected (checked) | no (records) |
| `changed_by`, `superseded_by` | ID to CHG, ID to ID | change history; "Superseded by" | no (records) |

Optional YAML frontmatter on an artifact is read too: `id`, `status`, `serves: [..]`, `blocked_by: [..]`. Where the story file and `BACKLOG.md` disagree on status, the story file wins.

## Localized headings

Parsing is content-based (ID types decide), except a few section keys: `change`, `impact`, `decisions needed`, `canonical traceability`, `change history`. For other languages create `<artifact-root>/graph/aliases.json`:

```json
{"headings": {"impact": ["Impacto"], "canonical traceability": ["Rastreabilidade canônica"]},
 "status_values": {"Rascunho": "Draft", "Obsoleta": "Stale"}}
```

## Layers and Graphify

| Layer | Source | Build | Cost |
| --- | --- | --- | --- |
| Requirements | this repo's artifacts | `req-graph.py build <root>` | local, no LLM |
| Knowledge | research, questionnaire answers, regulations, PDFs | `graphify extract <folder>` with a backend | LLM tokens; run only on unstructured folders |
| Code (optional) | the product repository | `graphify update <code-root>` | local, tree-sitter |

Merge (layers stay independent and cache separately):

```bash
graphify merge-graphs <code-root>/graphify-out/graph.json <root>/graph/req-graph.json \
  --out <root>/graph/merged-graph.json
```

Merged node ids are namespaced (`repo::fr_003`); query by label (`"FR-003"`). Native impact query on a merged graph:

```bash
graphify affected "FR-003" --graph <root>/graph/merged-graph.json \
  --relation serves --relation part_of --relation decided_by \
  --relation blocked_by --relation verifies --relation proves --depth 4
```

`graphify affected` defaults to code relations, so always pass `--relation`.

## Validation and exit codes

`req-graph.py validate <root>` (alias `--validate`; `check-ids.py` runs the same code) is the one CI check for the whole root: duplicate definitions, dangling references, FR or NFR without AC, AC without TC, stories without a matrix, `Stale` items, **dependency cycles** (three-color DFS over the dependency relations and `superseded_by`; change records such as `impacts` and `changed_by` are excluded on purpose, because a change and the story it impacts always point at each other) and the **Top 5 critical artifacts** (largest cascade of dependents; `critical --top N` ranks more).

| Exit | Meaning |
| --- | --- |
| 0 | consistent |
| 1 | orphan IDs or untested rules |
| 2 | dependency cycles |
| 3 | critical parse or file failure (`--strict` also turns any `[PARSE-WARNING]` into 3) |
| 64 / 66 | usage error / unknown target (outside the CI contract; `query` and `path` use 1 for "nothing found") |

All files are read and written as UTF-8 with `errors="replace"`. IDs are upper-cased on read (`fr-003` is `FR-003`). Table rows are tolerated with irregular spacing, missing edge pipes, `\|`, `<br>` and rows continued on the next line; anything malformed (wrong cell count, `FR-3`, `FR_12`, invalid bytes) goes to stderr as `[PARSE-WARNING] file:Lnn: message` instead of being skipped silently. Set `REQ_GRAPH_QUIET=1` to collect warnings without printing them.

**Lifecycle metadata.** Specs and stories carry `status: draft | review | approved | deprecated` and `version: X.Y.Z` in YAML frontmatter; the graph exposes them as `lifecycle` and `version` and warns when they disagree with the `**Status:**` line.

## Queries without Graphify

| Need | Command |
| --- | --- |
| Free-text search over the graph | `req-graph.py query <root> "fraud review" [--type US,FR] [--status Stale] [--depth N] [--limit N] [--budget TOKENS] [--json]` |
| What depends on X, what X depends on | `req-graph.py affected <root> <ID> [--up] [--depth N] [--no-weak]` |
| How two items connect | `req-graph.py path <root> <ID> <ID> [--directed] [--all]` |
| Everything about one item | `req-graph.py explain <root> <ID>` |
| Stories ready, stories obsolete | `frontier`, `stale` |
| Backlog progress from the operations checklists; flags a Progress column or Ready status that disagrees | `backlog [--json]` |
| The work queue of a spec, in dependency order, with the next ready line | `plan <root> SPEC-NNN [--json]` |

`query` ranks nodes by exact ID (a typed ID always wins), then IDF-weighted word matches in the text, prefix matches and substrings; status and type words count a little (so "stale" or "tests" help). Accents are ignored. Matches are expanded by `--depth` (default 1) along non-weak links; `--budget` is approximate (characters / 4) and the output says when it truncated. Exit code 1 when nothing matches.

What it does **not** do compared with `graphify query`: no semantic or embedding ranking (the words must overlap; "histórico" will not find "history"), no code or document layers, no communities. Put synonyms in the artifacts' glossary and use the same words, or merge a Graphify knowledge layer when you need semantic recall.

## Viewer

`req-graph.py build <root> --view` (or `view <root> [--out FILE] [--title TEXT]`) writes `graph/req-graph.html`: one self-contained file, no CDN, no network, no Graphify needed, same output for the same artifacts. It is rewritten only when the artifacts changed (or the file is missing).

- **Layered layout**: Goal, Capability, Story, FR/NFR, AC, TC from left to right; Spec/Epic, Decisions and Changes in bands below. Ordering minimizes crossings.
- **Click a node**: orange = impacted if it changes (same set as `req-graph.py affected`), blue = what it depends on. The panel lists both, each clickable, plus the CHG impact report for a change.
- **Status on the border**: Stale in red, Pending in amber, Ready in green. "Needs attention" lists Stale stories, Pending decisions, Blocked items.
- **Filters**: search by ID or text; toggle node types and relations; weak `references`, `decided_by` and change records are off by default (an impact path is always drawn). Skip-level links (a story serving both CAP and GOAL) are hidden as redundant.
- **Pan and zoom** with mouse or touch; **Fit**, **Clear**, **Save SVG**.
- Text is inserted with `textContent`, never as HTML, so artifact text cannot inject script. Rendering is SVG; it stays comfortable up to a few hundred nodes, so use `affected` for very large graphs.
- The Graphify HTML (`graphify export html`) is a separate view of the merged graph and needs Graphify; this one does not.

## Operating notes

- **Do not inject into Graphify's own `graph.json`.** Its incremental `update` replaces nodes of any re-extracted file, so injected nodes of that file vanish. Keep `req-graph.json` separate and merge.
- **Keep structured artifacts out of the LLM pass.** Add a `.graphifyignore` in the product root with `04-stories/ 03-specs/ 05-changes/ graph/` (seed in `setup-requirements-repo`). The deterministic graph already covers them, at no token cost and without ID drift.
- **Privacy.** Docs sent to a semantic pass leave the machine. `GRAPHIFY_BACKEND=none` keeps everything local.
- **Code links.** A story that cites `src/mod.py::Class` in backticks gets a `references` edge to that code node when the code layer is merged. Optional; skills never write code.
- **Commit policy.** `graph/` is derived; add it to `.gitignore` unless the team wants a shared snapshot.
- Not affiliated with Graphify Labs. Graphify is Apache-2.0.
