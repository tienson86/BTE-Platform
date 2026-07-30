# Summary Engine Execution Flow

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Execution Flow Specification)

---

# 1. Purpose

This document defines the end-to-end execution flow of the Summary Engine.

---

# 2. Execution Principles

- Deterministic
- Stateless
- Non-mutating
- Immutable
- Explainability-preserving
- Fail-fast / fail-closed

---

# 3. High-Level Flow

```text
Receive AnalysisContext
        │
        ▼
Validate Context
        │
        ▼
Read All Upstream Stage Results
        │
        ▼
Validate Completeness
        │
        ▼
Validate Cross-Stage Consistency
        │
        ▼
Aggregate Strength Summary
        │
        ▼
Aggregate Temperature Summary
        │
        ▼
Aggregate Pattern Summary
        │
        ▼
Aggregate Useful God Summary
        │
        ▼
Aggregate Ten Gods Summary
        │
        ▼
Aggregate Combination Summary
        │
        ▼
Aggregate ShenSha Summary
        │
        ▼
Aggregate Luck Summary
        │
        ▼
Consolidate Confidence
        │
        ▼
Build Evidence Index
        │
        ▼
Build Immutable SummaryResult
        │
        ▼
Publish SummaryResult
```

---

# 4. Stage Definitions

## Stage 1 — Receive AnalysisContext

Accept shared immutable AnalysisContext from Analysis Runtime.

## Stage 2 — Validate Context

Validate integrity and pipeline readiness for final consolidation.

## Stage 3 — Read Upstream Results

Read all eight published stage results from AnalysisContext.

## Stage 4 — Validate Completeness

Verify every mandatory upstream result is present and valid.

## Stage 5 — Validate Cross-Stage Consistency

Verify declared cross-stage consistency rules pass.

## Stage 6 — Domain Aggregation

Build non-destructive summary views for each domain without altering upstream payloads.

## Stage 7 — Confidence Consolidation

Aggregate confidence indicators into a consolidated summary profile.

## Stage 8 — Evidence Index Build

Index KnowledgeReferences / RuleEvidence from all upstream stages.

## Stage 9 — Build and Publish Result

Construct immutable `SummaryResult` and return to orchestrator.

---

# 5. Aggregation Order

Domain aggregation follows canonical pipeline order:

```text
Strength → Temperature → Pattern → Useful God → Ten Gods → Combination → ShenSha → Luck
```

Order reflects analytical dependency for summary indexing; it does not re-execute stages.

---

# 6. Data Movement

```text
AnalysisContext + eight StageResults
        │
        ▼
Internal summary intermediates (request-scoped)
        │
        ▼
SummaryResult (immutable)
```

---

# 7. Failure Points

Any stage may fail closed with classified errors.

Incomplete or inconsistent upstream sets must not produce SummaryResult.

---

# 8. Acceptance Criteria

Execution flow is accepted when order, aggregation semantics, and publish rules are complete.
