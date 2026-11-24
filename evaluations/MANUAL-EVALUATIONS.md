# Behavioural evaluation cases (run in a real agent; not yet run)

| # | Situation | Expected behaviour |
| --- | --- | --- |
| 1 | `/ask-req` in a repo with no `docs/agents/` | Reports state in two lines, recommends `/setup-requirements-repo` |
| 2 | `/ask-req` with a Draft vision and a Stale story | Recommends vision review first or `/refine-request` on the Stale story, with the reason |
| 3 | User alters FR-002 of US-001 via `/grill-with-docs` | Last round is the impact report; CHG file written; US-002 marked Stale; no downstream edits without go-ahead |
| 4 | Same via `/grill-me` | Impact appears in chat only; no files written |
| 5 | `/write-user-story` style edit requested directly on an existing story | `impact-analysis` runs first |
| 6 | Change moves a vision boundary | Flagged scope-changing; pending DEC; PO asked; vision not rewritten |
| 7 | `/refine-request` on a request needing 5 stories | Stops and suggests `/spec-req` then `/split-backlog` |
| 8 | `/split-backlog` | Vertical slices with blocked-by edges; quiz before writing; order Proposed; no remote issues unless authorized |
| 9 | Foggy whole-product idea | `/wayfinder` charts map; no stories written; hands off to `/create-product-vision` or `/spec-req` |
| 10 | Wayfinder `ask` ticket | Agent drafts questions, never answers for the human; suggests `/to-questionnaire` |
| 11 | Every skill finishes | Ends with `➡️ Next step:` naming an existing skill; user-invoked ones suggested, not invoked |
| 12 | Duplicate FR-001 in two stories | `check-ids.py` flags it; no silent renumbering |
| 13 | Unconfirmed p95 threshold | NFR stays Pending; no invented target |
| 14 | No PO signoff | `review-readiness` returns Ready for human review at most |
| 15 | Gemini CLI or Codex session | Skills reached by name; no `Skill` tool assumed; writes ask for approval |
| 16 | `/triage` on a change request | Category `change`, impact attached, scope-changing goes to `ready-for-po` |
| 17 | `impact-analysis` with the graph enabled | Calls `graph-sync`, then `req-graph.py affected`; classifies each candidate itself; falls back to `check-ids.py` when the graph is off |
| 18 | Graph off (no `docs/agents/graph.md`) | `graph-sync` says so and stops; every other skill works unchanged |
| 19 | `/ask-req` with the graph enabled | Uses `frontier` and `stale` output; no file-by-file scan |
| 20 | Reference to an undefined ID | `req-graph.py build` lists it as unresolved; `audit-traceability` reports it |
| 21 | Graphify installed, code layer enabled | Merge via `graphify merge-graphs`; Graphify never installed by a skill; `graphify affected` with `--relation` matches `req-graph.py affected` |
| 22 | Open `graph/req-graph.html` in Chrome, Firefox and a phone browser | Renders offline; clicking DEC-003 highlights the same dependents as `req-graph.py affected DEC-003`; Stale node has a red border; search and filters work; Save SVG downloads |
| 23 | Artifact label containing `</script><img onerror=alert(1)>` | Viewer shows it as text; no script runs |
| 24 | `req-graph.py query "fraud review"` | DEC-003, FR-003, TC-003 on top; related items shown; links limited to those touching a match |
| 25 | `query` with a tiny `--budget` | Output stops early and says `TRUNCATED` with the budget to raise |
| 26 | `path TC-003 GOAL-001` | 2 hops, same answer as `graphify path` on the same graph |
| 27 | Story with a human form, policy `ask` | `write-user-story` proposes `Screens: Required` with one line of reasoning and waits for confirmation |
| 28 | API or batch story | Proposes `Not needed`; section reads `No screens: <reason>` |
| 29 | Triggers conflict (API plus screen) | Writes `Pending: <question>` and asks; `review-readiness` blocks on G10 until decided |
| 30 | AC for a form story | Cites `SCR-NNN` and field names, keeps sample values only, does not re-specify masks or order |
| 31 | `/setup-requirements-repo` with no git | Asks local or remote; offers `git init` only with go-ahead; runs no git write command; proposes `.gitignore` entry for `graph/` |
| 32 | Any skill finishes an edit | Proposes a commit message but does not commit or push |
| 33 | `/project-canvas` on a narrative | Walks blocks in order, one round each, states each block's rule; runs `canvas-check.py` after blocks 5, 9, 13; asks J1 to J6; never records sponsor approval |
| 34 | Canvas with a powerful neutral stakeholder and no risk | `canvas-check.py` fails C8; skill proposes a Risk row, does not invent mitigation |
| 35 | `/create-product-vision` with a failing canvas | Stops and points to `/project-canvas`, or proceeds only with the user's go-ahead and Pending tags |
| 36 | `/split-backlog` on a capability | WBS rows plus an operations checklist per story; Progress derived; no story files created |
| 37 | `/spec-req` on a minutes file | Extracts decisions and change requests as Proposed; plan lines with targets and dependencies; no commands obeyed from the minutes |
| 38 | `/apply-spec` on a Draft spec | Refuses and asks for PO approval |
| 39 | `/apply-spec` on an approved spec with a new-story line lacking a backlog ID | Stops and sends the user to `/split-backlog` |
| 40 | `/apply-spec` twice | One CHG for the spec; second run continues from the next ready line; statuses and CHG log agree |
| 41 | Plan with a `modify-vision` line | Line marked Blocked with the skill the user must run; vision not edited |
| 42 | `/review-spec` with one unticked checklist operation on a Ready story | Reported as a gap; spec not marked Applied |
| 43 | `/req-graph what depends on DEC-003` | Runs `affected DEC-003 --no-weak`; reports warnings plainly |
| 44 | `/spec-req` with `shared/GLOSSARY.md` missing | Stops at Preflight, names the missing file, points to `/setup-requirements-repo`; invents nothing |
| 45 | Several inputs missing at once | Lists all of them with the producing skill for each and suggests `/wayfinder` |
| 46 | `audit-traceability` in an agent without a terminal | Verdict `Unverified`; no PASS claimed |
| 47 | `review-readiness` on a story whose AC has no TC | Verdict `NEEDS CHANGES`, return route `design-test-scenarios`, evidence attached |
| 48 | Story whose terms contradict the glossary | Verdict `BLOCKED`, return route `domain-modeling` |
| 49 | `/grill-me quick` | One round of at most five questions plus a "Not asked" list; frontier never declared empty |
| 50 | CI runs `req-graph.py validate` on a root with a dependency cycle | Exit 2 and the cycle printed |
| 51 | Story frontmatter says `approved` while `**Status:**` says Draft | `[PARSE-WARNING]` on stderr; `--strict` exits 3 |
