# Analysis Engine Architecture

**Module:** `engines/analysis_engine`

**Version:** V1.0.0

**Status:** Frozen

---

# 1. Purpose

This document defines the overall architecture of the Analysis Engine.

It specifies architectural boundaries, execution flow, dependency rules, shared contracts, and orchestration responsibilities.

---

# 2. Architectural Goals

The architecture shall be:

- Modular
- Deterministic
- Explainable
- Rule-driven
- Immutable
- Extensible
- Testable

---

# 3. Layered Architecture

```text
Calendar Engine
        │
        ▼
BaZi Engine
        │
        ▼
Analysis Engine
        │
        ├── Strength
        ├── Temperature
        ├── Pattern
        ├── Useful God
        ├── Ten Gods
        ├── Combination
        ├── ShenSha
        ├── Luck
        └── Summary
        │
        ▼
Interpretation Engine
        │
        ▼
Report Engine
```

---

# 4. Execution Model

The Analysis Engine follows a strictly ordered pipeline.

Every stage executes exactly once.

No stage may bypass another stage unless explicitly defined by architecture.

---

# 5. Stage Contracts

Each stage provides:

- Input Contract
- Output Contract
- Public API
- Internal Models
- Validation
- Error Handling

Stages communicate only through published contracts.

---

# 6. Shared Components

Shared components include:

- AnalysisContext
- AnalysisResult
- Shared Models
- Rule Registry
- Cache Infrastructure
- Common Exceptions
- Shared Interfaces

No stage owns these components exclusively.

---

# 7. Dependency Rules

Allowed:

- Upstream → Downstream
- Shared → Stage

Forbidden:

- Downstream → Upstream
- Stage → Stage internals
- Circular dependencies

---

# 8. Orchestration

The Analysis Engine orchestrator:

- Validates execution order.
- Creates shared context.
- Invokes stages.
- Collects stage results.
- Builds AnalysisResult.

Stages never invoke each other directly.

---

# 9. Architectural Principles

- Single Responsibility
- Separation of Concerns
- Immutable Data Flow
- Explicit Contracts
- Deterministic Execution
- Explainability
- Rule-Driven Analysis

---

# 10. Extension Strategy

Future analytical stages may be added without changing existing public contracts.

New stages shall conform to the same architectural standards defined in this document.

---

# 11. Governance

All stages within the Analysis Engine shall comply with:

- Architecture Baseline
- Shared Models
- Public API
- Validation Rules
- Version Compatibility

Architectural deviations require formal review and version updates.