# Analysis Runtime Public API

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document describes the logical Public API of the Analysis Runtime / Analysis Engine orchestration surface.

These are architectural contracts only.

No implementation syntax is prescribed.

---

# 2. Primary Entry Point

```text
AnalysisEngine.evaluate(context: AnalysisContext) -> AnalysisResult
```

This remains the canonical consumer-facing operation.

Analysis Runtime realizes this operation.

---

# 3. Logical Runtime Operations

| Operation | Purpose |
|-----------|---------|
| evaluate(context) | Execute full runtime pipeline |
| validate(context) | Admission / bind validation without full success publication (optional governed operation) |
| getExecutionMetadata(result) | Read metadata from published result |
| abort(requestId) | Governed abort of an in-flight Execution Unit where supported |

Stage-level evaluate methods are internal module contracts, not public platform API.

---

# 4. Input / Output

## Input

- AnalysisContext (immutable input snapshot)

## Output (success)

- AnalysisResult including StageResults, evidence, ExecutionMetadata

## Output (failure)

- classified Runtime Error (no false-complete AnalysisResult)

---

# 5. Knowledge Access API Boundary

Public API does not expose:

- GetModule/GetAsset directly to external callers as analysis API
- Registry/Loader internals

Knowledge access remains an internal Runtime ↔ SDK concern during evaluate.

---

# 6. Downstream Contract

Interpretation Engine consumes AnalysisResult only.

Report Engine does not call Analysis Runtime stage internals.

---

# 7. Compatibility

Public evaluate contract remains backward compatible within V1.x.

Breaking changes require MAJOR Runtime Spec / Analysis Engine version impact.

---

# 8. Acceptance Criteria

Public API is accepted when entry point, logical operations, I/O, and boundary rules are complete.
