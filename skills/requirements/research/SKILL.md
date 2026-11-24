---
name: research
description: Investigate a question against high-trust primary sources (regulations, official documentation, existing system docs, contracts) and capture the findings as a cited Markdown file. Use when a decision waits on a fact outside the repo, or reading legwork can be delegated.
---

Run the research in a **background agent with a fresh context window** when the harness supports one, so the session keeps moving; otherwise do it inline.

Its job:

1. Investigate against **primary sources** (law text, official docs, contracts, existing system documentation, first-party APIs), not summaries of them. Follow each claim to the source that owns it.
2. Write findings to one Markdown file, citing every claim's source. Mark a claim **Confirmed** only when a primary source states it; everything else is **Proposed**.
3. Save under `<artifact-root>/inputs/research/` (match the repo's convention). Say where.

Research gives facts. It never replaces a PO decision: a finding that needs a business choice becomes a pending DEC.

## Preflight (Pré-condições / Insumos Obrigatórios)

No file is required: it works from the question and external primary sources.

## Next steps

Take the file into `/grill-with-docs`, or resolve the `/wayfinder` ticket that asked for it.
