# Analysis Engine Pipeline

**Module:** `engines/analysis_engine`  
**Version:** 1.0.0  
**Status:** Frozen (Pipeline Specification)

---

# 1. Purpose

This document defines the canonical execution pipeline of the Analysis Engine.

The pipeline specifies the execution order, stage dependencies, data flow, and orchestration rules for all analytical stages.

---

# 2. Pipeline Principles

The pipeline shall be:

- Sequential
- Deterministic
- Immutable
- Rule-driven
- Explainable

Each stage executes exactly once per analysis request.

---

# 3. Canonical Execution Flow

```text
Calendar Engine
        │
        ▼
BaZi Engine
        │
        ▼
AnalysisContext
        │
        ▼
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

---

# 4. Stage Responsibilities

| Stage | Primary Responsibility |
|--------|------------------------|
| Strength | Evaluate Day Master strength |
| Temperature | Evaluate climatic balance |
| Pattern | Identify chart pattern (Ge Ju) |
| Useful God | Determine Useful/Favorable/Unfavorable Gods |
| Ten Gods | Evaluate Ten Gods structure |
| Combination | Analyze combinations, clashes, transformations |
| ShenSha | Detect and evaluate ShenSha |
| Luck | Evaluate Da Yun / Liu Nian / Liu Yue / Liu Ri impacts |
| Summary | Consolidate analytical results |

---

# 5. Data Flow

Each stage:

- receives an immutable AnalysisContext plus published upstream results;
- performs its own domain analysis;
- publishes one immutable stage result.

No stage may modify upstream outputs.

---

# 6. Dependency Rules

A stage may depend only on:

- AnalysisContext
- Shared Models
- Published upstream stage results

Direct access to another stage's internal implementation is prohibited.

---

# 7. Failure Policy

If a mandatory stage fails:

- pipeline execution stops;
- no AnalysisResult is published.

Optional stages (future versions) shall declare explicit fallback behavior.

---

# 8. Completion Criteria

Pipeline execution completes only when:

- every mandatory stage succeeds;
- all stage results are immutable;
- AnalysisResult passes validation.