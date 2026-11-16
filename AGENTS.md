# Requirements Skills: instructions for agents and contributors

This repo ships agent skills for eliciting and documenting requirements. It never generates application code. `CLAUDE.md` and `GEMINI.md` only point here; the skills themselves are harness-neutral.

## Layout

- `skills/requirements/` the requirements flow. `skills/productivity/` general tools (`grilling`, `grill-me`, `handoff`, `wait-what`, `to-questionnaire`). `skills/deprecated/` renamed v1 skills (pointer only).
- Each skill is `skills/<bucket>/<name>/SKILL.md`, owns its reference files, and has a generated `agents/openai.yaml` (Codex UI metadata; run `python3 scripts/sync_adapters.py`).
- `docs/` repo-level docs. `examples/` a fictional product with a full trail. `evaluations/` manual behaviour cases.

## Invocation: two kinds of skill

- **User-invoked**: `disable-model-invocation: true`. Reachable only when the human types the name. Orchestrators and anything with side effects. `description` is human-facing, one line, no trigger lists.
- **Model-invoked**: the default. `description` is model-facing with "Use when..." triggers.
- A user-invoked skill may invoke model-invoked skills, never another user-invoked skill. For those it **suggests**: "tell the user to run `/name`".

## Invoking another skill (harness-neutral)

Write "Invoke the `name` skill". It means: use your harness's skill mechanism (slash command, `activate_skill`, or by name in conversation). If none is available, read `skills/**/<name>/SKILL.md` and follow it. Never write "Call the Skill tool with ...": no such universal tool exists. A skill named in a handoff is a suggestion, not proof it ran. See `docs/INVOCATION.md`.

## Next steps (every skill)

Every `SKILL.md` ends with `## Next steps`: situation-to-skill suggestions, one recommended, finishing the reply with `➡️ **Next step:** ...`. Suggest, never auto-run. `ask-req` is the router and must list every skill; when you add, rename, remove or re-route a skill, update `ask-req`, the README flow, `docs/FLOW.md` and `docs/DE-PARA.md` in the same change. A router that lies is worse than none.

## Writing rules

See `docs/AUTHORING-SKILLS.md`. Short version: one source of truth per meaning, no restating what the environment already says, positive instructions, every step ends on a completion criterion, no em-dashes in prose.

## Before requirements work

Read `docs/agents/requirements-workflow.md` if present (artifact root, language, rules), `GLOSSARY.md`, `DECISIONS.md` and `PRODUCT-VISION.md` when available. Humans decide: never invent PO decisions or approvals.

## Validate

```bash
python3 scripts/validate_repository.py && python3 -m unittest discover -s tests -v
```
