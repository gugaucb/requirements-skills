---
name: handoff
description: Compact the current conversation into a handoff document so another agent or colleague can continue.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to the OS temporary directory (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows), not the workspace.

Include:

- **Where we are**: current flow step (see `/ask-req`), product, active IDs, and statuses (Confirmed, Proposed, Pending, Stale).
- **Open PO decisions** and who owns each.
- **Suggested skills**: the skills the next agent should invoke first, by name.

Do not duplicate content that lives in artifacts (vision, specs, stories, DECISIONS.md, CHG files, tracker issues). Reference them by path or URL. Redact secrets and personal data. If the user passed arguments, tailor the document to that focus.

## Next steps

Tell the user the path of the file and how to seed the new session with it. In the new session, `/ask-req` re-orients from the artifacts.
