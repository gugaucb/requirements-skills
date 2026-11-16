# Behavioural evaluation cases (run in a real agent; not yet run)

| # | Situation | Expected behaviour |
| --- | --- | --- |
| 1 | `/ask-req` in a repo with no `docs/agents/` | Reports state in two lines, recommends `/setup-requirements-repo` |
| 2 | `/ask-req` with a Draft vision and a Stale story | Recommends vision review first or `/refine-request` on the Stale story, with the reason |
| 3 | User alters FR-002 of US-001 via `/grill-with-docs` | Last round is the impact report; CHG file written; US-002 marked Stale; no downstream edits without go-ahead |
| 4 | Same via `/grill-me` | Impact appears in chat only; no files written |
| 5 | `/write-user-story` style edit requested directly on an existing story | `impact-analysis` runs first |
| 6 | Change moves a vision boundary | Flagged scope-changing; pending DEC; PO asked; vision not rewritten |
| 7 | `/refine-request` on a request needing 5 stories | Stops and suggests `/to-spec` then `/split-backlog` |
| 8 | `/split-backlog` | Vertical slices with blocked-by edges; quiz before writing; order Proposed; no remote issues unless authorized |
| 9 | Foggy whole-product idea | `/wayfinder` charts map; no stories written; hands off to `/create-product-vision` or `/to-spec` |
| 10 | Wayfinder `ask` ticket | Agent drafts questions, never answers for the human; suggests `/to-questionnaire` |
| 11 | Every skill finishes | Ends with `➡️ Next step:` naming an existing skill; user-invoked ones suggested, not invoked |
| 12 | Duplicate FR-001 in two stories | `check-ids.py` flags it; no silent renumbering |
| 13 | Unconfirmed p95 threshold | NFR stays Pending; no invented target |
| 14 | No PO signoff | `review-readiness` returns Ready for human review at most |
| 15 | Gemini CLI or Codex session | Skills reached by name; no `Skill` tool assumed; writes ask for approval |
| 16 | `/triage` on a change request | Category `change`, impact attached, scope-changing goes to `ready-for-po` |
