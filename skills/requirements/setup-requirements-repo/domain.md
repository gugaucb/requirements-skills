# Domain docs

How the requirements skills read business vocabulary and decisions.

## Before working, read

- `GLOSSARY.md` at the product root, or `GLOSSARY-MAP.md` if it exists (one `GLOSSARY.md` per context).
- `DECISIONS.md` for the area you touch.
- `PRODUCT-VISION.md` when present.

Missing files: proceed silently; `domain-modeling` creates them lazily.

## Use the glossary's vocabulary

Name concepts as the glossary does. Never drift to a term listed under `_Avoid_`. A missing concept is either invented language (reconsider) or a gap to hand to `domain-modeling`.

## Flag decision conflicts

If output contradicts a Confirmed DEC, say so explicitly rather than overriding it.
