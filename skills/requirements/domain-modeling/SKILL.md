---
name: domain-modeling
description: Build and sharpen a product's business vocabulary, actors, lifecycle states and recorded decisions. Use when business terms are unclear, overloaded or contradictory, when writing or editing GLOSSARY.md or DECISIONS.md, or when a term used by existing stories is being redefined.
---

Actively build the product's business language as you work: challenge terms, invent edge-case scenarios, and write the glossary and decisions down the moment they crystallise. Merely _reading_ `GLOSSARY.md` is a one-line habit any skill can do; this skill is for when you are changing the language.

The product glossary holds **business** terms. The process vocabulary (`US`, `FR`, `Ready`, ...) lives in `docs/agents/requirements-vocabulary.md`. Never copy one into the other.

## Files

Single context: `GLOSSARY.md` and `DECISIONS.md` under the product root. If `GLOSSARY-MAP.md` exists the repo has several contexts; the map says where each lives. Create files lazily, when the first term or decision is resolved.

## During the session

- **Challenge against the glossary.** When a term conflicts with an entry, say so at once: "The glossary defines 'active order' as X, but you seem to mean Y. Which is it?"
- **Sharpen fuzzy language.** For vague or overloaded words ("account", "customer"), propose one canonical term and list the rest under _Avoid_.
- **Stress-test with scenarios.** Invent concrete cases that probe boundaries between concepts and force precision.
- **Check the artifacts.** When the user states a rule, check whether existing stories, requirements and criteria agree. Surface contradictions: "US-003 allows partial cancellation, you just said it does not."
- **Model lifecycle states** only when they change acceptance (a status machine, allowed transitions).
- **Update inline.** The moment a term resolves, edit `GLOSSARY.md` using [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md). The moment a business decision is made, add a row to `DECISIONS.md` using [DECISIONS-FORMAT.md](DECISIONS-FORMAT.md). Do not batch.
- **Redefining a term in use.** If existing artifacts use the term, invoke the `impact-analysis` skill before changing the entry.

`GLOSSARY.md` is a glossary and nothing else: no requirements, no implementation detail, no scratch notes.

## Done

Every term the session touched is defined, listed under _Avoid_, or explicitly Pending; every decision has an owner and a status.

## Next steps

End with `➡️ **Next step:** ...`. Return to the calling flow (grilling, `/refine-request`, `/to-spec`). If a term change touched existing IDs, suggest `/refine-request` on the Needs review items.
