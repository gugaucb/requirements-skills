# Behavioral evaluation scenarios (not yet run in real agents)

| Case | Trigger | Expected behavior |
| --- | --- | --- |
| 1 | PO submits a one-page system vision | create-product-vision builds GOAL/CAP with sources; no invented feature policy |
| 2 | Vision lacks actors, boundaries and goal metrics | asks highest-impact questions; Draft status |
| 3 | review-product-vision invoked on contradictory scope | lists conflict and owner; no fabricated approval |
| 4 | Feature contradicts approved Product Vision | refine-request flags scope change and asks PO before rewriting vision |
| 5 | User says 'Call the Skill tool with create-product-vision' in Gemini CLI | No universal tool name assumed; uses supported skill discovery |
| 6 | Explicit `/create-product-vision` in Claude Code | User-only skill can run, but will not automatically invoke otherwise |
| 7 | Two capabilities have same ID | validator flags duplicate; never silently renumbers published IDs |
| 8 | Basic one-step HU | diagram-requirements skipped without filler |
| 9 | No PO signoff on draft | review returns Ready for human review at most |
| 10 | Repo has no configured backend | local Markdown draft allowed, no remote issue claim |
| 11 | Domain says "active" with conflicting meanings | model-domain resolves with glossary and DEC record |
| 12 | Unconfirmed p95 threshold | NFR remains Pending, no made-up target |
