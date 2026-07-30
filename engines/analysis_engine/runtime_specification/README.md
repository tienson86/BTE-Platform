# Analysis Runtime Specification

| Field | Value |
|-------|-------|
| Spec ID | analysis_runtime |
| Document Type | Constitutional Analysis Runtime Specification |
| Version | 1.0.0 |
| Status | Frozen Runtime Baseline |

---

# 1. Purpose

This specification defines the runtime architecture for the Analysis Engine.

It is the runtime contract for every analysis module (stage engine).

It describes how analysis executes at runtime after the Knowledge Foundation is available through the Knowledge SDK.

This set does **not** implement runtime code.

---

# 2. Core Principle

```text
Knowledge SDK provides WHAT analysis may know.
Analysis Runtime defines HOW analysis executes.
Analysis Modules compute stage results.
Interpretation Engine consumes published AnalysisResult only.
```

---

# 3. Architectural Relationship

```text
Knowledge SDK
        │
        ▼
Analysis Runtime            ← this specification
        │
        ▼
Analysis Modules
 (Strength … Luck … Summary)
        │
        ▼
Interpretation Engine
```

Analysis Modules shall not access Knowledge Modules, Registry, or Loader directly.

All knowledge access occurs through Knowledge SDK under Analysis Runtime control.

---

# 4. Scope

In scope:

- Runtime Context
- Execution Pipeline
- Execution Order
- Module Dependencies
- Shared Context
- Shared Result
- Error Recovery
- Performance Strategy
- Caching Strategy
- Validation Strategy
- Explainability
- Deterministic Execution

Out of scope:

- Knowledge content authoring
- Interpretation narrative generation
- Report rendering
- Implementation source code

---

# 5. Document Set

| # | Document |
|---|----------|
| 01 | README.md |
| 02 | ARCHITECTURE.md |
| 03 | RUNTIME_PIPELINE.md |
| 04 | EXECUTION_MODEL.md |
| 05 | MODULE_LIFECYCLE.md |
| 06 | CONTEXT_MODEL.md |
| 07 | RESULT_MODEL.md |
| 08 | ERROR_MODEL.md |
| 09 | CACHE_MODEL.md |
| 10 | PERFORMANCE.md |
| 11 | VALIDATION.md |
| 12 | PUBLIC_API.md |
| 13 | GOVERNANCE.md |
| 14 | CHANGELOG.md |

---

# 6. Design Principles

- Deterministic
- Sequential stage execution
- Immutable context/result progression
- SDK-only knowledge access
- Fail-closed validation and integrity
- Explainable evidence
- Version-aware knowledge freeze per request
- Backward compatible within V1.x runtime contracts

---

# 7. Version

| Item | Value |
|------|-------|
| Spec Version | 1.0.0 |
| Status | Frozen Runtime Baseline |

Breaking runtime-contract changes require a major version increment.
