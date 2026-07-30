# Combination Engine Architecture

**Module:** `engines/analysis_engine/06_combination_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Combination Engine.

---

# 2. Architectural Goals

- Provide deterministic natal Combination analysis.
- Isolate Combination analysis from other analytical concerns.
- Separate business knowledge from execution logic.
- Consume published upstream stage results from AnalysisContext without recomputation.
- Access Combination Knowledge only through Knowledge SDK.
- Produce reusable `CombinationResult` for downstream engines.
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

The Combination Engine never skips stages, never invokes downstream engines, and never modifies upstream data.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module performs Combination / Clash / Harm / Punishment / Destruction / Transformation analysis only.

## 4.2 Knowledge / Execution Separation

```text
Combination Knowledge (via Knowledge SDK) defines WHAT.
Combination Engine defines HOW.
```

## 4.3 No Upstream Recomputation

Strength, Temperature, Pattern, Useful God, and Ten Gods are read as published evidence only.

## 4.4 SDK-Only Knowledge Access

Direct Knowledge Module, Registry, or Loader access is forbidden.

## 4.5 Determinism

Identical AnalysisContext + frozen knowledge snapshot ⇒ equivalent CombinationResult semantics.

## 4.6 Explainability

Every material determination carries KnowledgeReferences / evidence.

---

# 5. Component Architecture

```text
CombinationEngine
        │
        ├── Context Validator
        ├── Upstream Result Reader
        ├── Knowledge Accessor (SDK)
        ├── Stem Combination Analyzer
        ├── Branch Combination Analyzer
        ├── Clash Analyzer
        ├── Harm Analyzer
        ├── Punishment Analyzer
        ├── Destruction Analyzer
        ├── Hidden Combination Analyzer
        ├── Transformation Evaluator
        ├── Priority / Conflict Resolver
        ├── Confidence Evaluator
        ├── Result Builder
        └── Diagnostics Recorder
```

---

# 6. Dependency Rules

Allowed:

```text
Combination Engine → AnalysisContext (shared models)
Combination Engine → Knowledge SDK
Combination Engine → Analysis Runtime contracts
```

Forbidden:

```text
Combination Engine → upstream Engine internals
Combination Engine → Knowledge Module packages directly
Combination Engine → Registry / Loader internals
Combination Engine → Interpretation / Report Engines
Combination Engine → ShenSha / Luck Engines
```

---

# 7. Knowledge Flow

```text
Frozen KnowledgeSession (SDK)
        │
        ▼
Combination Engine evaluates AnalysisContext
        │
        ▼
Matched KnowledgeReferences
        │
        ▼
Immutable CombinationResult
```

---

# 8. Extension Strategy

Within V1.x, additive knowledge content is allowed without changing public API.

Public API remains:

```text
evaluate(context: AnalysisContext) -> CombinationResult
```

---

# 9. Constraints

- One public entry point
- No path-coupled knowledge contracts
- No runtime knowledge mutation
- No sibling-module invocation
