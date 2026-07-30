# Luck Engine Architecture

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Luck Engine.

---

# 2. Architectural Goals

- Provide deterministic natal Luck analysis across Da Yun → Liu Shi hierarchy.
- Isolate Luck analysis from other analytical concerns.
- Separate business knowledge from execution logic.
- Consume published upstream stage results from AnalysisContext without recomputation.
- Access Luck Knowledge only through Knowledge SDK.
- Produce reusable `LuckResult` for downstream engines.
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

The Luck Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module performs Luck / fortune timeline analysis only.

## 4.2 Knowledge / Execution Separation

```text
Luck Knowledge (via Knowledge SDK) defines WHAT.
Luck Engine defines HOW.
```

## 4.3 No Upstream Recomputation

All upstream natal analytical results are read as published evidence only.

## 4.4 SDK-Only Knowledge Access

Direct Knowledge Module, Registry, or Loader access is forbidden.

## 4.5 Determinism

Identical AnalysisContext + frozen knowledge snapshot ⇒ equivalent LuckResult semantics.

## 4.6 Explainability

Every material determination carries KnowledgeReferences / evidence.

---

# 5. Component Architecture

```text
LuckEngine
        │
        ├── Context Validator
        ├── Upstream Result Reader
        ├── Knowledge Accessor (SDK)
        ├── Da Yun Evaluator
        ├── Liu Nian Evaluator
        ├── Liu Yue Evaluator
        ├── Liu Ri Evaluator
        ├── Liu Shi Evaluator
        ├── Luck Interaction Evaluator
        ├── Timing / Activation Evaluator
        ├── Favorability Evaluator
        ├── Priority / Conflict Resolver
        ├── Confidence Evaluator
        ├── Result Builder
        └── Diagnostics Recorder
```

---

# 6. Dependency Rules

Allowed:

```text
Luck Engine → AnalysisContext (shared models)
Luck Engine → Knowledge SDK
Luck Engine → Analysis Runtime contracts
```

Forbidden:

```text
Luck Engine → upstream Engine internals
Luck Engine → Knowledge Module packages directly
Luck Engine → Registry / Loader internals
Luck Engine → Interpretation / Report Engines
Luck Engine → Summary Engine
```

---

# 7. Knowledge Flow

```text
Frozen KnowledgeSession (SDK)
        │
        ▼
Luck Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable LuckResult
```

---

# 8. Extension Strategy

Within V1.x, additive knowledge content is allowed without changing public API.

Public API remains:

```text
evaluate(context: AnalysisContext) -> LuckResult
```

---

# 9. Constraints

- One public entry point
- No path-coupled knowledge contracts
- No runtime knowledge mutation
- No sibling-module invocation
