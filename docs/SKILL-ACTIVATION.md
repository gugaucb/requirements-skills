# Skill activation audit — platform-specific triggers

The literal phrase **`Call the Skill tool with "..."` is not a portable invocation API**. Never put it in a shared SKILL.md or tell every agent to call a tool named `Skill`.

- **Shared Agent Skills specification:** `name` (directory-matching kebab-case) and `description` (what and when) in YAML frontmatter, with the instructions following. This is portable discovery metadata.
- **Claude Code:** `/create-product-vision` or other `/skill-name` explicitly invokes a skill. Claude can infer applicability from descriptions for model-invocable skills. `disable-model-invocation: true` is a Claude-specific extension, used on repository setup and creating a vision to keep high-impact creation user-controlled. A Claude wrapper is a discovery adapter; its relative reference must resolve.
- **Gemini CLI:** internally discovers and activates applicable skills using `activate_skill` and user consent. Never command the model to invent a universal `Skill` tool. Use natural language naming and verify discovery in the actual CLI.
- **Codex:** locate available workspace skills under `.agents/skills`; request them by their skill names in conversation. Do not hard-code an undocumented universal tool call.

## Trigger policy

Explicit/manual: `setup-requirements-repo`, `create-product-vision` (constructing a vision requires PO framing and approval). Automatically relevant: review, refinement, domain, story, requirements, tests, diagrams, traceability; no auto-approval. For Claude, `disable-model-invocation: true` is enforced by the platform. For others, source text still instructs the agent to ask for user intent before writes.

A skill should reference another by **its canonical name and purpose** (e.g. "Use audit-traceability when necessary") rather than a brittle internal tool string. Handoffs do not bypass consent or pretend a skill ran.

References: https://agentskills.io/specification · https://code.claude.com/docs/en/skills · https://geminicli.com/docs/cli/skills/ · https://developers.openai.com/codex/skills
