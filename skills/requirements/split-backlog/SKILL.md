---
name: split-backlog
description: Break a spec, capability or epic into thin vertical user stories, each declaring its blocking edges, and record them in BACKLOG.md or the configured tracker.
disable-model-invocation: true
---

Break a spec, capability, epic or the current conversation into **stories**: thin vertical slices of user value, each declaring the stories that **block** it. This is the tracer-bullet idea applied to requirements.

Read `docs/agents/requirements-workflow.md` and `docs/agents/issue-tracker.md`. If missing, tell the user to run `/setup-requirements-repo`.

## Process

### 1. Gather context

Use the conversation. If the user passes a reference (a spec path, `CAP-NNN`, an issue), read it fully. Read `BACKLOG.md` so you do not duplicate or renumber existing stories.

### 2. Draft vertical slices

<slicing-rules>

- Each story is a narrow but COMPLETE path of business value: an actor, an outcome, observable by the PO. Not a screen, a table, or a technical layer.
- A finished story is demoable or verifiable on its own.
- Each story fits one refinement session (`/refine-request` in a fresh context).
- Order by real dependency, not preference. Prefer enabling rules first ("make the change easy, then make the easy change").
- Technical-only stories exist only with an explicit quality or enablement purpose that stakeholders agree.
- Epics are optional: group only when a real collection of value exists.

</slicing-rules>

Give each story its **Blocked by** edges: stories that must be done first. No blockers means it can start now.

### 3. Quiz the user

Present a numbered list. For each: **Title**, **Serves** (GOAL/CAP/EPIC), **Blocked by**, **What it delivers**. Ask:

- Does the granularity feel right (too coarse, too fine)?
- Does each story depend only on stories that genuinely gate it?
- Should any be merged or split?

Iterate until the user approves. Priority and sprint assignment are PO-owned: record order as **Proposed** and never invent sprints.

### 4. Record

Write rows to `BACKLOG.md` (format in [BACKLOG-FORMAT.md](BACKLOG-FORMAT.md)), allocating `US-NNN` IDs without recycling. Create no story files yet; `write-user-story` does that lazily.

Publish to the tracker only when the user explicitly asks and the tracker doc allows it: one issue per story in dependency order (blockers first), native blocking links where the tracker has them, label `ready-for-refinement`. Never close or edit a parent issue.

If `docs/agents/graph.md` exists, invoke the `graph-sync` skill afterwards so the `blocked_by` frontier is queryable.

## Done

Every candidate story is in `BACKLOG.md` with serves-links, blockers and a Proposed order, and the user approved the breakdown.

## Next steps

End with `➡️ **Next step:** ...`.

- Start with the first story that has no blockers: `/refine-request US-NNN`. Work the frontier (all blockers done), a fresh context per story.
- Broad stories remain after the quiz: run `/split-backlog` again on them.
