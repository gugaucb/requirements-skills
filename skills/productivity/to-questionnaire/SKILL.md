---
name: to-questionnaire
description: Turn a decision you cannot answer alone into a questionnaire for a stakeholder to fill in.
disable-model-invocation: true
---

Turn something the user cannot answer alone into a **questionnaire**: a Markdown document they hand to one person (PO, legal, operations, customer) to fill in async or together in a meeting. The recipient holds knowledge the user lacks.

**Grill the send, not the subject.** Interview the user only about the _send_.

1. **Who is it going to?** Ask in one exchange: role, expertise, relationship. Done when you know who the recipient is and what they know that the user does not.
2. **What do you need back?** Ask in one exchange: the decisions or facts needed, and the IDs they unblock (DEC, CAP, US). Done when you hold a concrete list.
3. **Write it** to `to-questionnaire-<slug>.md` under the product root (or the current directory), using the template below. Done when every item from step 2 is covered by a question.

<questionnaire-template>

# <Questionnaire title>

**Purpose:** why it exists and the decision riding on it (cite DEC/CAP/US IDs).

**From:** <user>, **To:** <recipient>, **How your answers will be used:** <where they go>

## Preflight (Pré-condições / Insumos Obrigatórios)

No file is required: it works from the conversation; it reads the glossary if one exists.

## Context

One paragraph for a recipient who was not in the user's head.

## How to answer

Deadline and rough effort. Partial answers and "I don't know" are useful.

## <Theme>

Questions most-important-first. One idea per question, answer stub beneath, and a one-line _why this matters_ only where the question could be misread.

### <Question>

_Why this matters: ..._

>

## Anything else?

What did we not ask that we should know?

</questionnaire-template>

Answers from the document are **evidence from the named person**. Record them in `DECISIONS.md` as Confirmed only when the accountable person answered.

## Next steps

When answers come back: `/grill-with-docs` to absorb them, `/spec-req` if they complete a feature, or resolve the originating `/wayfinder` ticket.
