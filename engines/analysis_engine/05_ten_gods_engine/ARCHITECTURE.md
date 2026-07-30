# Ten Gods Engine Architecture

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Ten Gods Engine.

---

# 2. Architectural Goals

- Provide deterministic natal Ten Gods analysis.
- Isolate Ten Gods analysis from all other analytical concerns.
- Separate business knowledge from execution logic.
- Consume published Strength, Temperature, Pattern, and Useful God results from AnalysisContext without recomputation.
- Access Ten Gods Knowledge only through Knowledge SDK.
- Produce reusable `TenGodsResult` for downstream engines.
- Support future knowledge expansion without architectural changes.
- Guarantee reproducible analytical results.

---

# 3. Position in the BTE Platform

```text
Strength Engine
        │
        ▼
Temperature Engine
        │
        ▼
Pattern Engine
        │
        ▼
Useful God Engine
        │
        ▼
Ten Gods Engine
        │
        ▼
Combination Engine
        │
        ▼
ShenSha Engine
        │
        ▼
Luck Engine
        │
        ▼
Summary Engine
        │
        ▼
Interpretation Engine
        │
        ▼
Report Engine
```

The Ten Gods Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module performs Ten Gods analysis only.

## 4.2 Knowledge / Execution Separation

```text
Ten Gods Knowledge (via Knowledge SDK) defines WHAT.
Ten Gods Engine defines HOW.
```

## 4.3 No Upstream Recomputation

Strength, Temperature, Pattern, and Useful God are read as published evidence only.

## 4.4 SDK-Only Knowledge Access

Direct Knowledge Module, Registry, or Loader access is forbidden.

## 4.5 Determinism

Identical AnalysisContext + frozen knowledge snapshot ⇒ equivalent TenGodsResult semantics.

## 4.6 Explainability

Every material determination carries KnowledgeReferences / evidence.

---

# 5. Component Architecture

```text
TenGodsEngine
        │
        ├── Context Validator
        ├── Upstream Result Reader
        ├── Knowledge Accessor (SDK)
        ├── Presence / Identity Analyzer
        ├── Relationship Analyzer
        ├── Interaction Analyzer
        │     ├── Strength Interaction
        │     ├── Temperature Interaction
        │     ├── Pattern Interaction
        │     └── Useful God Interaction
        ├── Favorability Evaluator
        ├── Life-Area Concept Evaluator
        ├── Priority / Conflict Resolver
        ├── Confidence Evaluator
        ├── Result Builder
        └── Diagnostics Recorder
```

---

# 6. Dependency Rules

Allowed:

```text
Ten Gods Engine → AnalysisContext (shared models)
Ten Gods Engine → Knowledge SDK
Ten Gods Engine → Analysis Runtime contracts
```

Forbidden:

```text
Ten Gods Engine → Strength / Temperature / Pattern / Useful God Engine internals
Ten Gods Engine → Knowledge Module packages directly
Ten Gods Engine → Registry / Loader internals
Ten Gods Engine → Interpretation / Report Engines
Ten Gods Engine → Combination / ShenSha / Luck Engines
```

---

# 7. Knowledge Flow

```text
Frozen KnowledgeSession (SDK)
        │
        ▼
Ten Gods Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable TenGodsResult
```

---

# 8. Extension Strategy

Within V1.x, additive knowledge content and optional concept refinements are allowed without changing public API.

Public API remains:

```text
evaluate(context: AnalysisContext) -> TenGodsResult
```

---

# 9. Constraints

- One public entry point
- No path-coupled knowledge contracts
- No runtime knowledge mutation
- No sibling-module invocation
