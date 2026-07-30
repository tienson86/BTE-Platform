# Knowledge Pipeline

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Lifecycle Specification)

---

# 1. Purpose

This document defines the canonical knowledge lifecycle and the runtime consumption pipeline used by Engine Modules.

---

# 2. Pipeline Principles

The Knowledge Pipeline shall be:

- Deterministic
- Version-aware
- Immutable at runtime
- Validated before publication
- Storage-agnostic
- Traceable

---

# 3. Knowledge Lifecycle

```text
Author
  │
  ▼
Draft Knowledge Assets
  │
  ▼
Validate
  │
  ▼
Review / Approve
  │
  ▼
Package Knowledge Module
  │
  ▼
Publish Versioned Bundle
  │
  ▼
Register in Knowledge Registry
  │
  ▼
Consume by Engines
```

No asset may be consumed by production engines before publication.

---

# 4. Runtime Consumption Flow

```text
Engine Execution Starts
        │
        ▼
Resolve Required Knowledge Modules
        │
        ▼
Select Compatible Knowledge Versions
        │
        ▼
Load Abstract Knowledge Views
        │
        ▼
Validate Knowledge Completeness
        │
        ▼
Freeze Knowledge Snapshot for Request
        │
        ▼
Engine Matching / Scoring / Rendering
        │
        ▼
Attach KnowledgeReferences to Results
```

---

# 5. Analysis Engine Consumption

Analysis Engine stages consume Rule Knowledge through abstract modules:

```text
Strength Engine        → Strength Knowledge
Temperature Engine     → Temperature Knowledge
Pattern Engine         → Pattern Knowledge
Useful God Engine      → Useful God Knowledge
Ten Gods Engine        → Ten Gods Knowledge
Combination Engine     → Combination Knowledge
ShenSha Engine         → ShenSha Knowledge
Luck Engine            → Luck Knowledge
```

All consumption occurs through abstract Knowledge Module contracts.

---

# 6. Downstream Consumption

```text
Interpretation Engine → Interpretation Knowledge
Report Engine         → Report Knowledge
```

Interpretation and Report engines may reference analytical result contracts, but they never recompute analytical knowledge.

---

# 7. Snapshot Isolation

For one analysis request:

1. Knowledge versions are resolved once.
2. A request-scoped immutable snapshot is created.
3. All stages use the same snapshot.
4. Mid-request knowledge switching is prohibited.

This guarantees cross-stage consistency.

---

# 8. Failure Policy

Fatal knowledge failures include:

- required Knowledge Module unavailable;
- incompatible knowledge version;
- incomplete mandatory asset category;
- failed integrity validation;
- circular knowledge dependency.

Fatal failures stop engine execution.

No partial analytical publication is permitted when mandatory knowledge is missing.

---

# 9. Observability

Every knowledge resolution event shall record:

- module_id
- selected version
- resolution timestamp
- compatibility decision
- correlation identifier

Observability data must not alter analytical outcomes.

---

# 10. Completion Criteria

Knowledge consumption is complete when:

- all required modules are resolved;
- versions are compatible;
- snapshot is immutable;
- engines can attach KnowledgeReferences to published results.
