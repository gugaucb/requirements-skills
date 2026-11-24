# Phase boundaries

A **phase** is a chunk of work inside a session: a grilling, a spec, a refinement of one story. It ends when you think "ok, we are done with that". The **boundary** between two phases is the only place this decision belongs. Mid-phase, continue, or split what is left into sub-agents.

## The five options

| Option | What it does |
| --- | --- |
| **Continue** | Stay in the session. No context switch. |
| **Clear** | Start a new session from nothing (the old one stays resumable). |
| **`/handoff`** | Write a portable file and seed a session anywhere with it. |
| **Sub-agent** | Send a tightly scoped task to its own context and get a report back. |
| **Compact** | Summarise this context in place and carry on from the summary. |

## The tree

Work top to bottom at the boundary. The first **yes** wins.

1. **Can you continue?** Yes if the next phase needs this one as a **primary source** (grilling to spec to stories: the stories want the reasoning verbatim) or enough context window remains. Continue costs nothing; rule it out first.
2. **Is everything here disposable?** Then **clear**. One-way: clearing relevant context loses the why.
3. **Is something travelling?** A new harness, a new directory, a colleague, or a side task forked mid-phase: `/handoff`. It buys portability only.
4. **Can it run AFK?** Tightly scoped, no steering needed (an audit, a review, research): **sub-agent**.
5. **Otherwise compact**, with an instruction ("we are going to refine US-004 next"). It is the default at the bottom, not the first reach: summaries flatten decisions.

## Requirements-specific defaults

- `/grill-with-docs` to `/spec-req` to `/split-backlog`: **continue** in one context.
- Between stories in `/refine-request`: **clear**. Each story is self-contained; the artifacts are the memory.
- After a change (CHG): continue until the impact report is confirmed, then **clear** before re-refining each Stale story.
- `/retro`: run it in the session it looks back on, before clearing.

Primary sources become secondary sources at every move except Continue: the trade is information for room.
