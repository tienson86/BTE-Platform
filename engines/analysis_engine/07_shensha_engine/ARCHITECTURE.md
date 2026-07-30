# ShenSha Engine Architecture

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the ShenSha Engine.

---

# 2. Architectural Goals

- Provide deterministic natal ShenSha analysis.
- Isolate ShenSha analysis from other analytical concerns.
- Separate business knowledge from execution logic.
- Consume published upstream stage results from AnalysisContext without recomputation.
- Access ShenSha Knowledge only through Knowledge SDK.
- Produce reusable `ShenShaResult` for downstream engines.
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

The ShenSha Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module performs ShenSha detection and evaluation only.

## 4.2 Knowledge / Execution Separation

```text
ShenSha Knowledge (via Knowledge SDK) defines WHAT.
ShenSha Engine defines HOW.
```

## 4.3 No Upstream Recomputation

All upstream analytical results are read as published evidence only.

## 4.4 SDK-Only Knowledge Access

Direct Knowledge Module, Registry, or Loader access is forbidden.

## 4.5 Determinism

Identical AnalysisContext + frozen knowledge snapshot ⇒ equivalent ShenShaResult semantics.

## 4.6 Explainability

Every material determination carries KnowledgeReferences / evidence.

---

# 5. Component Architecture

```text
ShenShaEngine
        │
        ├── Context Validator
        ├── Upstream Result Reader
        ├── Knowledge Accessor (SDK)
        ├── Calculation Reference Resolver
        ├── Lookup / Mapping Evaluator
        ├── Auspicious ShenSha Evaluator
        ├── Inauspicious ShenSha Evaluator
        ├── Interaction Evaluator
        ├── Compatibility Evaluator
        ├── Exception Evaluator
        ├── Priority / Conflict Resolver
        ├── Confidence Evaluator
        ├── Result Builder
        └── Diagnostics Recorder
```

---

# 6. Dependency Rules

Allowed:

```text
ShenSha Engine → AnalysisContext (shared models)
ShenSha Engine → Knowledge SDK
ShenSha Engine → Analysis Runtime contracts
```

Forbidden:

```text
ShenSha Engine → upstream Engine internals
ShenSha Engine → Knowledge Module packages directly
ShenSha Engine → Registry / Loader internals
ShenSha Engine → Interpretation / Report Engines
ShenSha Engine → Luck Engine
```

---

# 7. Knowledge Flow

```text
Frozen KnowledgeSession (SDK)
        │
        ▼
ShenSha Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable ShenShaResult
```

---

# 8. Extension Strategy

Within V1.x, additive knowledge content is allowed without changing public API.

Public API remains:

```text
evaluate(context: AnalysisContext) -> ShenShaResult
```

---

# 9. Constraints

- One public entry point
- No path-coupled knowledge contracts
- No runtime knowledge mutation
- No sibling-module invocation
