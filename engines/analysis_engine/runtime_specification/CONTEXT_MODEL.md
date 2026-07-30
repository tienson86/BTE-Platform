# Analysis Runtime Context Model

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document defines Runtime Context and Shared Context contracts used during analysis execution.

---

# 2. Context Layers

```text
Input AnalysisContext
        │
        ▼
Runtime Context (request-scoped execution state)
        │
        ├── KnowledgeSession handle (frozen)
        ├── StageResult accumulator
        ├── ExecutionMetadata accumulator
        ├── Diagnostic channel
        └── Policy profile references
```

---

# 3. Input AnalysisContext

Produced by upstream Calendar / BaZi completion.

Contains chart facts and identifiers required for analysis.

Immutable as input snapshot for the request.

---

# 4. Shared Context

Shared Context is the evolving analytical state visible to stages.

It includes:

- base input facts
- published prior StageResults
- frozen knowledge references for the request
- non-semantic runtime diagnostics as allowed

Stage modules read Shared Context and return new StageResults.

Stages must not rewrite prior StageResults.

---

# 5. Runtime Context

Runtime Context holds orchestration state not part of domain StageResult contracts, including:

- current stage pointer
- knowledge session bind info
- cache keys for the request
- error state
- timing/metrics slots

Runtime Context must not be required by Interpretation Engine.

---

# 6. Context Readiness Rules

Before stage N executes, Shared Context must contain all prerequisite StageResults declared for stage N.

Missing prerequisites fail closed.

---

# 7. Explainability in Context

Context retains KnowledgeReferences and RuleEvidence emitted by stages to support explainability in AnalysisResult.

---

# 8. Isolation

Each request has an isolated Runtime Context.

Cross-request context sharing of mutable analytical state is forbidden.

---

# 9. Acceptance Criteria

Context Model is accepted when layers, immutability/append rules, readiness, and isolation are complete.
