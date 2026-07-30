# Summary Engine Architecture

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the official software architecture of the Summary Engine.

---

# 2. Architectural Goals

- Provide deterministic cross-stage analytical consolidation.
- Isolate summary aggregation from domain recomputation.
- Preserve upstream semantic integrity.
- Produce reusable `SummaryResult` for Interpretation Engine consumption.
- Guarantee reproducible aggregation results.
- Complete the Analysis Engine analytical pipeline.

---

# 3. Position in the BTE Platform

```text
01 Strength Engine
        │
        ▼
02 Temperature Engine
        │
        ▼
03 Pattern Engine
        │
        ▼
04 Useful God Engine
        │
        ▼
05 Ten Gods Engine
        │
        ▼
06 Combination Engine
        │
        ▼
07 ShenSha Engine
        │
        ▼
08 Luck Engine
        │
        ▼
09 Summary Engine
        │
        ▼
AnalysisResult
        │
        ▼
Interpretation Engine
        │
        ▼
Report Engine
```

The Summary Engine never invokes downstream engines and never modifies upstream stage results.

---

# 4. Architectural Principles

## 4.1 Single Responsibility

The module consolidates published analytical results only.

## 4.2 Non-Recomputation

No domain stage logic is re-executed inside Summary Engine.

## 4.3 Non-Mutation

Upstream StageResults remain immutable and unchanged.

## 4.4 Determinism

Identical upstream results ⇒ equivalent SummaryResult semantics.

## 4.5 Explainability Preservation

Evidence and KnowledgeReferences from upstream stages are preserved and indexed, not discarded.

---

# 5. Component Architecture

```text
SummaryEngine
        │
        ├── Context Validator
        ├── Upstream Result Reader
        ├── Completeness Validator
        ├── Cross-Stage Consistency Checker
        ├── Domain Summary Aggregator
        ├── Confidence Consolidator
        ├── Evidence Index Builder
        ├── Summary Result Builder
        └── Diagnostics Recorder
```

---

# 6. Dependency Rules

Allowed:

```text
Summary Engine → AnalysisContext (shared models)
Summary Engine → published upstream StageResults
Summary Engine → Analysis Runtime contracts
```

Forbidden:

```text
Summary Engine → upstream Engine internals
Summary Engine → Knowledge SDK for domain recomputation
Summary Engine → Interpretation / Report Engines
Summary Engine → mutation of upstream StageResults
```

---

# 7. Data Flow

```text
All published StageResults in AnalysisContext
        │
        ▼
Summary Engine aggregates
        │
        ▼
Immutable SummaryResult
        │
        ▼
AnalysisResult assembly (Runtime)
```

---

# 8. Extension Strategy

Within V1.x, additive summary views and diagnostic fields are allowed without changing public API.

Public API remains:

```text
evaluate(context: AnalysisContext) -> SummaryResult
```

---

# 9. Constraints

- One public entry point
- No domain knowledge execution
- No upstream semantic override
- Final mandatory analytical stage before AnalysisResult publication
