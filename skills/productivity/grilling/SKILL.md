---
name: grilling
description: Grill the user relentlessly about a plan, requirement, decision or change until every branch of the design tree is resolved. Use when the user wants to stress-test their thinking, when PO decisions are missing, when an existing story or capability is being changed, or on any 'grill' trigger phrase.
---

Interview the user relentlessly until you reach a shared understanding. Map the subject as a **design tree**: every decision branches into the decisions that hang off it.

Reply in the user's language. Read `docs/agents/requirements-workflow.md` when it exists (output language, ID scope).

## Rounds

The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you have not heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the answers before the next round.

```
❓ **Q1** - **<question title>**: <question body, may include multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer. A question that depends on another open question in this round belongs to a later round. Order each round by impact: scope and eligibility first, then rules and exceptions, then quality constraints, then wording.

Question the business, not the solution: who, outcome, eligibility, exceptions, boundaries, volumes and limits, legal or contractual rules, what "done" looks like to the PO.

## Facts versus decisions

Finding _facts_ is your job. When a frontier question needs a fact from files, artifacts or tools, look it up yourself (delegate to a sub-agent with a fresh context window when the harness supports it) and ask only what remains. The _decisions_ belong to the human: put each to them and wait. Never answer your own question, and never mark a decision Confirmed on the user's behalf.

## Tag what you learn

Tag every substantive answer **Confirmed** (the accountable person said it), **Proposed** (your recommendation or a hypothesis) or **Pending** (open). Say who confirmed it. A hypothetical option stays Proposed.

## Change mode

When the subject is a **change to something that already has IDs** (a US, FR, AC, CAP, GOAL, DEC or a glossary term), finish the tree with an **impact round**: invoke the `impact-analysis` skill and present its report as the last round, for the user to confirm, narrow or reject. A change is not settled until its downstream effect is on the table.

If the caller is stateless (`grill-me`), report the impact in chat only and write nothing.

## Done

The session is done when the frontier is empty: every branch visited, nothing left silently assumed (and, in change mode, the impact round confirmed). Do not act on the result until the user confirms the shared understanding.

## Next steps

Suggest one, never auto-run. End with `➡️ **Next step:** ...`.

- Stateful session, decisions and terms need recording: tell the user to run `/grill-with-docs` next time, or record them now with the `domain-modeling` skill.
- Understanding is complete and a feature or capability emerged: tell the user to run `/to-spec`.
- The product itself is still undefined: tell the user to run `/create-product-vision`.
- An answer sits with someone who is not here: tell the user to run `/to-questionnaire`.
- A change was confirmed: tell the user to run `/refine-request` on each impacted story, blockers first.
