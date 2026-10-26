# Requirements Skills v1.2.0

A **documentation-first**, portable Agent Skills repository for Claude Code, Codex, and Gemini CLI. Transforms PO system vision into goals and capabilities, then incrementally refines requests into Scrum-friendly user stories, requirements, Gherkin, test scenarios and Mermaid diagrams. **Does not generate application source code.** Independent work inspired by [Matt Pocock's skills](https://github.com/mattpocock/skills), without affiliation.

## Start here

1. Install the repository in a workspace, keeping hidden `.agents/` and `.claude/` folders.
2. Explicitly request **`setup-requirements-repo`** to configure tracker, paths, language, IDs and local policy; confirm changes before writes.
3. Explicitly request **`create-product-vision`** using a PO narrative or document. Output `PRODUCT-VISION.md` with `GOAL-` and `CAP-` identifiers.
4. Run **`review-product-vision`** and collect PO decisions; then **`refine-request`** for a concrete feature or capability.
5. Use focused skills on demand; run **`audit-traceability`** and **`review-readiness`** before claiming readiness.

### Skill catalog (15)

| Skill | Purpose |
| --- | --- |
| [`setup-requirements-repo`](.agents/skills/setup-requirements-repo/SKILL.md) | Configure repository-level requirements documentation: tracker, artifact location, labels, output language, ID conventions and team workflow. Use only when the user explicitly requests repository setup or changes to setup. |
| [`initialize-requirements`](.agents/skills/initialize-requirements/SKILL.md) | Initialize product-specific Markdown request, backlog, glossary and decision files using confirmed repository settings. Use when starting documentation for a new product. |
| [`create-product-vision`](.agents/skills/create-product-vision/SKILL.md) | Turn a Product Owner vision statement, informal idea, brief or existing vision document into a structured PRODUCT-VISION.md with goals, actors, capabilities, boundaries and unresolved questions. Use at product inception or on explicit vision updates. |
| [`review-product-vision`](.agents/skills/review-product-vision/SKILL.md) | Review a product vision for consistent vocabulary, unapproved assumptions, scope contradictions, measurable goals and coverage of capabilities. Use when asked to assess or approve a draft vision for human review. |
| [`refine-request`](.agents/skills/refine-request/SKILL.md) | Orchestrate refinement of a specific Product Owner request into user stories, requirements, Gherkin, tests and traceability. Use on concrete feature requests, respecting the approved product vision. |
| [`interview-product-owner`](.agents/skills/interview-product-owner/SKILL.md) | Ask dependency-ordered questions to resolve unknown business rules, target users, scope, quality constraints or acceptance behavior. Use when PO decisions are missing. |
| [`model-domain`](.agents/skills/model-domain/SKILL.md) | Define and reconcile business vocabulary, aliases, actors and lifecycle states in a shared glossary and decision log. Use when domain terms are unclear or contradictory. |
| [`split-backlog`](.agents/skills/split-backlog/SKILL.md) | Split a product capability or epic into small, vertically valuable user stories, with explicit dependencies and PO-owned ordering. Use when backlog items are too broad. |
| [`write-user-story`](.agents/skills/write-user-story/SKILL.md) | Create or revise classic As a / I want / So that user stories, including explicit scope and links to goals and capabilities. Use when expressing a user outcome. |
| [`specify-requirements`](.agents/skills/specify-requirements/SKILL.md) | Write atomic functional and measurable non-functional requirements in Markdown tables, with evidence and source decisions. Use when elaborating story behavior and constraints. |
| [`define-acceptance-criteria`](.agents/skills/define-acceptance-criteria/SKILL.md) | Write externally observable acceptance criteria in Gherkin Given / When / Then using the configured locale. Use for defining acceptance of story requirements. |
| [`design-test-scenarios`](.agents/skills/design-test-scenarios/SKILL.md) | Derive implementation-independent test scenarios with setup, action, expected evidence and negative cases. Use to verify criteria and requirements. |
| [`diagram-requirements`](.agents/skills/diagram-requirements/SKILL.md) | Create Mermaid flow, state or sequence diagrams when necessary to clarify a user journey or business rule. Use only for meaningful complexity. |
| [`audit-traceability`](.agents/skills/audit-traceability/SKILL.md) | Verify links from product goals and capabilities through epics, stories, functional and non-functional requirements, acceptance criteria and tests. Use after changes or before reviews. |
| [`review-readiness`](.agents/skills/review-readiness/SKILL.md) | Audit story clarity, requirements, tests, acceptance coverage and human decisions under local readiness rules. Use for final refinement review, never to impersonate PO signoff. |

## Artifact structure

```text
artifacts/<product>/
├── PRODUCT-VISION.md    # Product goals and capabilities
├── REQUEST.md           # Incoming PO demand
├── BACKLOG.md           # CAP/EPIC/US relationships
├── GLOSSARY.md          # Business vocabulary
├── DECISIONS.md         # Explicit human decisions
├── US-001.md            # FR, NFR, Gherkin, TC and canonical matrix
└── diagrams/
```

[Vision template](templates/PRODUCT-VISION.md) · [Story template](templates/USER-STORY.md) · [Shared vocabulary](docs/VOCABULARY.md) · [Skill activation audit](docs/SKILL-ACTIVATION.md) · [Flow](docs/SKILL-FLOW.md) · [Traceability](docs/TRACEABILITY.md) · [Quality gates](docs/QUALITY-GATES.md) · [Fictional example](examples/vision/PRODUCT-VISION.md)

## Invocation and compatibility

The wording **`Call the Skill tool with "..."` is not portable**. Agent Skills standard discovery relies on YAML `name`/`description`. In Claude Code, users may enter `/skill-name`; Gemini CLI internally discovers and calls `activate_skill` with approval; Codex should be asked in natural language to use an available skill. The package uses platform-specific adapters only where necessary and never invents a universal tool API. See [audit](docs/SKILL-ACTIVATION.md).

## Principles

Small and composable; evidence before assumptions; human PO signoff; lean Markdown; one authoritative matrix; no forced epics or diagrams; stable IDs; shared vocabulary without conflating domain terms and workflow jargon. Product Vision is revisable and is not a mandatory Scrum artifact.

## Validate

```bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -v
```

Static checks are not a substitute for **live CLI skill-activation tests** or PO review. See [manual evaluations](evaluations/MANUAL-EVALUATIONS.md).

## Distribution

MIT license ([LICENSE](LICENSE)); [contribute](CONTRIBUTING.md); [publishing](PUBLISHING.md). Support for the three agents is based on their documented skill discovery locations; runtime behavior must be tested locally.

[Repository setup templates](templates/setup/requirements-workflow.md) — project settings must be confirmed before writing.
