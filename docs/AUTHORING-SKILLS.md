# Authoring skills

Condensed from Matt Pocock's `writing-for-agents`, adapted for requirements work.

1. **Context pointers decide invocation.** A skill's `description` is the pointer. Front-load the leading word, one trigger per distinct branch, cut identity the body already carries.
2. **Two loads.** Always-loaded text (descriptions, `AGENTS.md`) costs context every turn; the number of skills a human must remember costs cognition. Spend each deliberately. `ask-req` exists to spend cognition for the human.
3. **Information hierarchy.** In-file steps first, in-file reference next, disclosed reference (a sibling file behind a pointer) last. Inline what every branch needs; disclose what only some need.
4. **Every step ends on a completion criterion** that is checkable and exhaustive ("every FR has an AC"), not "understanding reached".
5. **Single source of truth.** One authoritative place per meaning. Do not restate what the environment already says. A rule repeated in 15 skills is a bug: put it in `docs/agents/requirements-workflow.md`.
6. **Prune no-ops.** If the model already does it by default, delete the sentence.
7. **Prompt the positive.** "Write one-line comments", not a list of bans. Keep prohibitions only for hard guardrails, paired with the positive target.
8. **Mechanical checks beat rules.** If a violation is mechanical (duplicate ID, dangling link), extend `check-ids.py` or the validator instead of writing a rule.
9. **User-invoked versus model-invoked.** Test: could the model usefully reach for this alone? Reviews, writers and analysers: yes. Orchestrators and anything that publishes or approves: no.
10. **Handoffs.** Every skill ends with `## Next steps`. Operative calls only to model-invoked skills.
11. **No em-dashes** in prose; rewrite the sentence.
12. **Scope bar.** Add a skill only for an observed failure in a real session, and only if it does not compose from existing skills.
