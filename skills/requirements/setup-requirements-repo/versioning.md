# Versioning

**Mode:** <git local | git remote>
**Remote:** <host and remote name, or "none">
**Layout:** <artifacts in the product repo | dedicated requirements repo>
**Branching:** <trunk | branch per story | branch per change (CHG)>
**Review step:** <none | pull or merge request>

## Commit convention

`req(<IDs>): <summary>`, for example `req(US-001,CHG-001): add On hold status`. One commit per story refinement or per change.

## What is versioned

- Versioned: everything under the artifact root, `.graphifyignore`, `docs/agents/`.
- Derived, not versioned: `<artifact-root>/graph/` (add to `.gitignore`).

## Rules

- Skills never commit, push, open a PR or rewrite history unless the user asks in that turn. They propose the message.
- A merged pull or merge request is human approval only when the PO records it as a DEC that cites it.
- Versioning is independent of the issue tracker (`issue-tracker.md`).
