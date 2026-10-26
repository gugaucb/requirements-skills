# Skill flow and decision gates

```mermaid
flowchart TD
 A[User-approved repository setup] --> B[Product context or PO brief]
 B --> C[create-product-vision]
 C --> D[review-product-vision]
 D --> E{PO confirms vision?}
 E -->|No| C
 E -->|Yes| F[refine-request]
 F --> G[interview-product-owner as needed]
 F --> H[model-domain as needed]
 F --> I[split-backlog when broad]
 I --> J[write-user-story]
 F --> J
 J --> K[specify-requirements]
 K --> L[define-acceptance-criteria]
 L --> M[design-test-scenarios]
 M --> N[diagram-requirements if useful]
 M --> O[audit-traceability]
 N --> O
 O --> P[review-readiness]
```

The diagram is a routing model, not a requirement to invoke every skill. A small, fully specified request may skip interview, modeling, epics and diagrams. A draft vision may support exploratory stories if explicitly labeled and accepted as provisional. No automatic approval. A scope-changing feature is escalated to the PO and traced back to vision revisions.
