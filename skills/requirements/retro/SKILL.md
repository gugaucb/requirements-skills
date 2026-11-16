---
name: retro
description: Conduct a retrospective on a refinement session and suggest improvements to the requirements environment.
disable-model-invocation: true
---

You are suggesting improvements to the **environment** that produced the requirements, not to the requirements themselves. Read the primary sources for the session (the conversation, or the logs the user points at; default to the current one) and the artifacts it touched.

Look for candidates, most severe first:

- **Vocabulary**: terms defined mid-session that were missing from `GLOSSARY.md`; words used inconsistently.
- **Repeated questions**: the same PO question asked across stories. Fix with a decision recorded once, a questionnaire template, or a line in `requirements-workflow.md`.
- **Rework**: stories that went Stale or Needs changes. Was the impact missed, or was a decision unconfirmed too long?
- **Mechanical errors**: duplicate or dangling IDs, uncovered FR/AC. Fix with a deterministic check (extend `check-ids.py`) before writing a rule.
- **Readiness rules**: quality gates too loose or too tight; a Definition of Ready worth tightening.
- **Navigation**: how long it took to find the right artifact; whether a pointer in `AGENTS.md` or the `## Agent skills` block would help.
- **Skill gaps**: a handoff that nobody suggested, or a flow step with no skill.

Present the candidates to the user in order of severity. Judgement calls go to quality gates or the workflow doc; mechanical ones go to checks.

## Next steps

Apply accepted items; for changes to skills, follow `docs/AUTHORING-SKILLS.md`. To continue work, run `/ask-req`.
