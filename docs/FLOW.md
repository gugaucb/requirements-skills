# Flow and decision gates

Skills in rounded boxes are user-invoked (you type them); plain boxes are model-invoked. The output of each phase is the input of the next. The diagrams are routing models, not pipelines: skip what the work does not need. Each skill ends by suggesting the next step, and `/ask-req` reads your artifacts to say where you are.

## The five phases

| Phase | Skill | Reads | Writes | Human gate |
| --- | --- | --- | --- | --- |
| 1 | `/project-canvas`, `/create-product-vision` | narrative, minutes | `00-canvas/`, `01-vision/` | sponsor approves the vision |
| 2 | `/split-backlog` | CAPs of the vision | `02-backlog/` | PO confirms the order |
| 3 | `/spec-req` | a backlog story, a conversation, or minutes | `03-specs/` | PO approves the spec |
| 4 | `/apply-spec` | the approved spec | artifacts, `04-stories/`, `05-changes/` | PO reviews |
| 5 | `/review-spec` | spec, changes, graph | review in the spec | PO signs |

```mermaid
flowchart TD
  SETUP("/setup-requirements-repo<br/>once per repo") --> CANVAS
  CANVAS("/project-canvas<br/>13 blocks, integration rules") --> VISION("/create-product-vision<br/>goals and capabilities with origin")
  VISION --> RVIS["review-product-vision"]
  RVIS --> PO1{"Sponsor approves<br/>the vision?"}
  PO1 -- "no" --> VISION
  PO1 -- "yes" --> SPLIT("/split-backlog<br/>WBS: capability, epic, story<br/>operations checklist")
  SPLIT --> SPEC("/spec-req<br/>strategy and plan of changes")
  SPEC --> PO2{"PO approves<br/>the spec?"}
  PO2 -- "no" --> SPEC
  PO2 -- "yes" --> APPLY("/apply-spec<br/>next ready plan line, one CHG")
  APPLY --> STORY["refine-story<br/>write-user-story, specify-requirements,<br/>define-acceptance-criteria, design-test-scenarios,<br/>diagram-requirements, audit, readiness"]
  STORY --> APPLY
  APPLY -- "all lines closed" --> REVIEW("/review-spec<br/>conformance to the spec")
  REVIEW --> PO3{"PO signs?"}
  PO3 -- "gaps" --> APPLY
  PO3 -- "yes" --> RETRO("/retro")
```

## On-ramps and change flow

```mermaid
flowchart TD
  ASK("/ask-req<br/>reads phase and state, recommends")
  TRIAGE("/triage<br/>incoming and change requests")
  WAY("/wayfinder<br/>huge foggy effort")
  QUEST("/to-questionnaire<br/>answer sits with someone else")
  RES["research<br/>primary sources"]
  MIN["meeting minutes<br/>inputs/minutes"]
  GRILL("/grill-with-docs")
  IMPACT["impact-analysis<br/>CHG-NNN, items marked Stale"]
  REFINE("/refine-request<br/>one story, no spec")
  CANVAS("/project-canvas")
  VISION("/create-product-vision")
  SPEC("/spec-req")
  SPLIT("/split-backlog")
  ASK -.-> TRIAGE
  ASK -.-> WAY
  TRIAGE -- "new" --> SPEC
  TRIAGE -- "change" --> GRILL
  TRIAGE -- "foggy" --> WAY
  MIN --> SPEC
  WAY -- "ask ticket" --> QUEST
  WAY -- "research ticket" --> RES
  WAY -- "map clear: new system" --> CANVAS
  WAY -- "map clear: vision" --> VISION
  WAY -- "map clear: feature" --> SPEC
  QUEST --> GRILL
  RES --> GRILL
  GRILL -- "change mode: final impact round" --> IMPACT
  IMPACT -- "one change: stories are Stale" --> REFINE
  IMPACT -- "many changes" --> SPEC
  IMPACT -- "scope-changing" --> PO{"PO decision"}
  PO --> GRILL
  SPEC -- "new stories without IDs" --> SPLIT
```

## Status machine of a story

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Ready_for_human_review: review-readiness passes
  Ready_for_human_review --> Needs_changes: PO feedback
  Needs_changes --> Draft: refine-story
  Ready_for_human_review --> Ready_team_agreement: human approval recorded
  Draft --> Blocked: open PO decision
  Blocked --> Draft: decision confirmed
  Draft --> Stale: upstream changed (CHG)
  Ready_for_human_review --> Stale: upstream changed (CHG)
  Ready_team_agreement --> Stale: upstream changed (CHG)
  Stale --> Draft: refine-story closes the CHG item
  Draft --> Retired
  Ready_team_agreement --> Retired
```

Progress is separate from status: it is derived from the operations checklist of the story in `BACKLOG.md` (`Pending`, `In progress`, `Done`).

## Status machine of a spec and its plan lines

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Ready_for_human_review: spec-req complete
  Ready_for_human_review --> Approved: PO approval recorded as DEC
  Approved --> Applying: apply-spec first run (CHG created)
  Applying --> Applying: next plan line (Pending to Done, Skipped or Blocked)
  Applying --> Reviewed: review-spec finds no gaps
  Reviewed --> Applied: PO signs
```

Gates: nothing is approved automatically; `/apply-spec` refuses an unapproved spec; a scope-changing request goes to the PO as a DEC; `Stale` blocks readiness; a change outside the plan is a new plan line, not a silent edit.

## Graph overlay (optional)

```mermaid
flowchart LR
  MD["Markdown artifacts<br/>source of truth"] --> RG["req-graph.py build<br/>deterministic, no LLM"]
  RG --> RJ[("graph/req-graph.json")]
  CODE["product code"] -.-> GU["graphify update<br/>tree-sitter, local"]
  DOCS["research, regulations, PDFs"] -.-> GE["graphify extract<br/>LLM, unstructured only"]
  GU --> MG["graphify merge-graphs"]
  GE --> MG
  RJ --> MG
  RJ --> Q1["impact-analysis<br/>req-graph.py affected"]
  RJ --> Q3["ask-req<br/>frontier, stale, backlog, plan"]
  RG --> VW["req-graph.html<br/>offline viewer"]
  RQ("/req-graph<br/>ask in plain words") -.-> RG
```

Rule: every edge points at what its source depends on, so `graphify affected X` and `req-graph.py affected X` return everything impacted by X. Rebuild with the `graph-sync` skill after any skill that writes artifacts.

## Return routes (when a quality gate blocks)

A gate never ends the work; it names where to go back. `BLOCKED` means a decision or an input is missing; `NEEDS CHANGES` means a mechanical fix is enough. After the fix, run the failed check again.

| Signal | Verdict | Return to |
| --- | --- | --- |
| G1 story unclear (role, scope, benefit) | BLOCKED | `write-user-story` |
| G2 serves no capability, or scope-changing | BLOCKED | `/grill-with-docs` (PO decision), then `/split-backlog` or `/create-product-vision` |
| G3 requirements not atomic, NFR without a metric | NEEDS CHANGES | `specify-requirements` |
| G4 FR or NFR without AC | NEEDS CHANGES | `define-acceptance-criteria` |
| G5 AC without TC, test not derivable or failing | NEEDS CHANGES | `design-test-scenarios` (or `define-acceptance-criteria` if the AC is ambiguous) |
| G6 glossary term inconsistent, contradictory rules | BLOCKED | `domain-modeling` |
| G7 `Stale` upstream | BLOCKED | `refine-story` (`/apply-spec` when it came from a spec) |
| G8 rule without a decision, decision Pending | BLOCKED | `/grill-with-docs` |
| G10 screens undecided, form repeated in ACs | NEEDS CHANGES | `write-user-story` |
| `canvas-check.py` rule C1 to C10 or R | NEEDS CHANGES | `/project-canvas` |
| `validate` exit 1, duplicate ID | BLOCKED | stop and ask the user; never renumber |
| `validate` exit 1, dangling reference | NEEDS CHANGES | define the ID or fix the reference |
| `validate` exit 2, dependency cycle | BLOCKED | `/grill-with-docs`: decide which dependency is wrong |
| `validate` exit 3, parse or file failure | BLOCKED | fix the file or input named in the output |
| `/review-spec` gap on an unfinished line | NEEDS CHANGES | `/apply-spec SPEC-NNN` |
| `/review-spec` gap on a story | NEEDS CHANGES | `/refine-request US-NNN` |

```mermaid
flowchart LR
  GATE{"gate or check"} -- "PASS" --> NEXT["next step"]
  GATE -- "NEEDS CHANGES" --> FIX["return route: the skill that owns the failed part"]
  GATE -- "BLOCKED" --> DEC["decision or missing input: /grill-with-docs, /to-questionnaire, /wayfinder"]
  FIX --> GATE
  DEC --> GATE
```
