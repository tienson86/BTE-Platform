# Summary Engine Error Handling

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Error Handling Specification)

---

# 1. Purpose

This document defines error classification and handling for the Summary Engine.

---

# 2. Error Principles

- Fail closed
- Explicit classification
- No silent omission of mandatory upstream results
- No upstream recomputation as recovery
- No mutation of upstream results as recovery
- Align with Analysis Runtime Error Model

---

# 3. Error Classes

| Class | Typical Cause |
|-------|---------------|
| ValidationError | Invalid AnalysisContext |
| PrerequisiteError | Missing required upstream stage results |
| ConsistencyError | Blocking cross-stage inconsistency |
| SchemaError | Upstream result schema mismatch |
| ExecutionError | Internal aggregation failure |
| StateError | Illegal invocation/lifecycle usage |

---

# 4. Error Surface

Errors shall include:

- error class
- stage identity (`summary`)
- missing upstream field identity when applicable
- consistency violation summary when applicable
- summary
- retryability flag

---

# 5. Recovery Policy

## Allowed

- whole-stage retry under Analysis Runtime governed retry policy when upstream results may become available on retry (normally not applicable if pipeline order is correct)

## Forbidden

- invent summary data without upstream results
- patch upstream StageResults to force consistency
- publish SummaryResult with missing mandatory upstream domains
- recompute domain stages locally

---

# 6. Propagation

Errors propagate to Analysis Runtime orchestrator.

No successful SummaryResult is returned on mandatory failure.

Pipeline does not publish AnalysisResult when Summary Engine fails.

---

# 7. Acceptance Criteria

Error Handling is accepted when classes, surface, recovery allow/forbid rules, and propagation are complete.
