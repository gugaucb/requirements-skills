# GLOSSARY.md format

```md
# <Product or context name>

<One or two sentences: what this context is and why it exists.>

## Language

**Order**:
A request by a customer to receive goods. _Status: Confirmed (PO, 2026-05-02)_
_Avoid_: Purchase, transaction

**Active order**:
An order that is neither delivered nor cancelled. _Status: Proposed_
_Avoid_: Open order, current order
```

Rules:

- Be opinionated: pick one word per concept, list the others under `_Avoid_`.
- One or two sentences. Define what it **is**.
- Tag every entry **Confirmed** (with who), **Proposed** or **Pending**.
- Only terms specific to this product's business. General technical words do not belong.
- Group under subheadings when clusters emerge. Multi-context: a root `GLOSSARY-MAP.md` lists contexts and relationships.
