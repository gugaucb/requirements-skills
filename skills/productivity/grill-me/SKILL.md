---
name: grill-me
description: A relentless, stateless interview to sharpen a plan, requirement or change. Writes nothing.
disable-model-invocation: true
argument-hint: "quick | exhaustive (default)"
---

Invoke the `grilling` skill in the mode the user asked for (`quick`: one round of at most five questions; `exhaustive`, the default: until the frontier is empty). Stay stateless: create and edit no files. When the subject changes an existing requirement, the impact round appears in chat only.

## Preflight (Pré-condições / Insumos Obrigatórios)

No file is required: it is stateless and reads only the conversation.

## Next steps

When the interview ends, suggest `/grill-with-docs` if the work lives in a repo and the answers should be kept, `/spec-req` if a feature emerged, or `/ask-req` if the user is unsure what comes next.
