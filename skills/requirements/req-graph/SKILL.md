---
name: req-graph
description: Ask the requirements graph in plain words: rebuild it, open the viewer, find what depends on an item, search, trace how two items connect, see the backlog progress or a spec's plan.
disable-model-invocation: true
argument-hint: "e.g. what depends on DEC-003 | open | frontier | plan SPEC-001"
---

A thin front door to `req-graph.py`, so nobody has to remember commands. Invoke the `graph-sync` skill for the details, then pick the command from what the user asked.

Read-only commands work even when the graph is switched off in `docs/agents/graph.md` (they read the Markdown). `build` and `view` write under `<artifact-root>/graph/`: when the graph is off, say so and ask before writing.

| The user says | Run (`python3 <graph-sync-dir>/scripts/req-graph.py <command> <artifact-root> ...`) |
| --- | --- |
| rebuild, update, refresh the graph | `build --view` |
| open, show, see the graph | `build --view`, then give the path of `graph/req-graph.html` |
| what depends on X, what breaks if X changes | `affected X --no-weak` |
| what does X depend on, where does X come from | `affected X --up --no-weak` |
| find or search something in words | `query "<words>"` (add `--type US,FR` or `--status Stale` when asked) |
| how are A and B related | `path A B` (add `--all` if no path is found) |
| tell me about X | `explain X` |
| what is ready, what is next | `frontier` |
| what is stale, what needs rework | `stale` |
| backlog progress, status of the stories | `backlog` |
| plan or progress of a spec | `plan SPEC-NNN` |
| check the canvas rules | `python3 <project-canvas-dir>/scripts/canvas-check.py <artifact-root>` |
| check IDs | `python3 <audit-traceability-dir>/scripts/check-ids.py <artifact-root>` |

An ID typed without its prefix is not guessed: ask. When a command prints a warning (unresolved IDs, mismatched progress), repeat it plainly and name the owner skill that fixes it. The graph proposes; it never decides.

## Preflight (Pré-condições / Insumos Obrigatórios)

Check that these exist before doing anything else:

- an artifact root with at least one artifact

If any of them is missing, **stop**. Do not invent, assume or reconstruct the missing data. Tell the user which inputs are missing and which skill produces each (`/setup-requirements-repo` for configuration, `/project-canvas` or `/create-product-vision` for the vision, `/split-backlog` for the backlog, `/spec-req` for specs, `/grill-with-docs` or `/to-questionnaire` for missing decisions); when several are missing or the way forward is unclear, tell the user to run `/wayfinder`.

## Next steps

End with `➡️ **Next step:** ...` chosen from the result.

- Stories on the frontier: `/refine-request US-NNN`. Stale items: `/refine-request` on each, or `/apply-spec` if they come from a spec.
- A plan line is next: `/apply-spec`. All plan lines closed: `/review-spec`.
- Unresolved or duplicate IDs: invoke `audit-traceability`.
- Unsure where you are: `/ask-req`.
