# Flow and decision gates

Skills in rounded boxes are user-invoked (you type them); plain boxes are model-invoked. The diagram is a routing model, not a pipeline: skip what the work does not need. Each skill ends by suggesting the next step.

## Main flow

```mermaid
flowchart TD
  SETUP("/setup-requirements-repo<br/>once per repo") --> GRILL
  GRILL("/grill-with-docs<br/>stateful interview: glossary, decisions")
  GRILL --> VISION("/create-product-vision")
  VISION --> RVIS["review-product-vision"]
  RVIS --> PO1{"PO approves vision?<br/>recorded as DEC"}
  PO1 -- "no" --> VISION
  PO1 -- "yes" --> SPEC("/to-spec<br/>no interview")
  SPEC --> SLICE("/split-backlog<br/>vertical slices and blocking edges")
  SLICE --> REFINE("/refine-request US-NNN<br/>one story, fresh context")
  REFINE --> WUS["write-user-story"]
  WUS --> SREQ["specify-requirements"]
  SREQ --> AC["define-acceptance-criteria"]
  AC --> TC["design-test-scenarios"]
  TC --> DG["diagram-requirements<br/>only if useful"]
  TC --> AUDIT["audit-traceability<br/>check-ids.py then semantics"]
  DG --> AUDIT
  AUDIT --> READY["review-readiness"]
  READY --> PO2{"PO review"}
  PO2 -- "needs changes" --> REFINE
  PO2 -- "approved" --> NEXT{"more frontier stories?"}
  NEXT -- "yes" --> REFINE
  NEXT -- "no" --> RETRO("/retro")
```

## On-ramps and change flow

```mermaid
flowchart TD
  ASK("/ask-req<br/>reads artifact state, recommends")
  TRIAGE("/triage<br/>incoming and change requests")
  WAY("/wayfinder<br/>huge foggy effort")
  QUEST("/to-questionnaire<br/>answer sits with someone else")
  RES["research<br/>primary sources"]
  GRILL("/grill-with-docs")
  IMPACT["impact-analysis<br/>CHG-NNN, items marked Stale"]
  REFINE("/refine-request")
  VISION("/create-product-vision")
  SPEC("/to-spec")
  ASK -.-> TRIAGE
  ASK -.-> WAY
  TRIAGE -- "new" --> SPEC
  TRIAGE -- "change" --> GRILL
  TRIAGE -- "foggy" --> WAY
  WAY -- "ask ticket" --> QUEST
  WAY -- "research ticket" --> RES
  WAY -- "map clear: vision" --> VISION
  WAY -- "map clear: feature" --> SPEC
  QUEST --> GRILL
  RES --> GRILL
  GRILL -- "change mode: final impact round" --> IMPACT
  IMPACT -- "impacted stories are Stale" --> REFINE
  IMPACT -- "scope-changing" --> PO{"PO decision"}
  PO --> GRILL
```

## Status machine of a story

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Ready_for_human_review: review-readiness passes
  Ready_for_human_review --> Needs_changes: PO feedback
  Needs_changes --> Draft: refine-request
  Ready_for_human_review --> Ready_team_agreement: human approval recorded
  Draft --> Blocked: open PO decision
  Blocked --> Draft: decision confirmed
  Draft --> Stale: upstream changed (CHG)
  Ready_for_human_review --> Stale: upstream changed (CHG)
  Ready_team_agreement --> Stale: upstream changed (CHG)
  Stale --> Draft: refine-request closes the CHG item
  Draft --> Retired
  Ready_team_agreement --> Retired
```

Gates: no automatic approval; a scope-changing request goes to the PO as a DEC and is traced to a vision revision; `Stale` blocks readiness.

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
  MG --> Q2["graphify affected, query, path"]
  RJ --> Q3["ask-req<br/>frontier and stale"]
  RG --> VW["req-graph.html<br/>offline viewer"]
```

Rule: every edge points at what its source depends on, so `graphify affected X` returns everything impacted by X. Rebuild with the `graph-sync` skill after any skill that writes artifacts.
