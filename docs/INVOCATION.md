# Invocation across harnesses

The skills are written once, harness-neutral. Only the way a human or a model **reaches** a skill differs.

## The convention

| Writing | Meaning |
| --- | --- |
| "Invoke the `x` skill" | Operative step. Use your harness's skill mechanism; if none, read `skills/**/x/SKILL.md` and follow it. Only for **model-invoked** skills. |
| "Tell the user to run `/x`" | Suggestion. For **user-invoked** skills; no skill can fire another one. |
| `/x` in router prose | A plain label for a user-invoked skill. |

The phrase "Call the Skill tool with ..." is banned: it names a tool that only some harnesses have. Matt Pocock's repo uses it; this repo deliberately does not.

## How harnesses discover skills

| Harness | Discovery | Manual call | Block model auto-use |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/<name>/SKILL.md` | `/name` | `disable-model-invocation: true` in frontmatter |
| Codex | `.agents/skills/<name>/SKILL.md` | name the skill in the prompt | `agents/openai.yaml` `policy.allow_implicit_invocation: false` (generated) |
| Gemini CLI | `.agents/skills/` (or `gemini skills install`) | name the skill; the CLI activates with approval | frontmatter flag is ignored; the SKILL.md text still asks before writes |
| Others (Cursor, OpenCode, ...) | their skills directory | `/name` or by name | the SKILL.md text |

`scripts/install.sh <dest>` flattens the buckets into `<dest>/<skill>/SKILL.md`. Verify discovery in your own CLI; behaviour is documented by each vendor and changes.

## Why the next-step suggestions do not depend on a tool

Every skill ends with `## Next steps`: plain text naming the next skill and why. A human reads it; a model may offer it. Nothing in it needs a tool call, so it works in every harness.

References: https://agentskills.io/specification, https://code.claude.com/docs/en/skills, https://geminicli.com/docs/cli/skills/, https://developers.openai.com/codex/skills
