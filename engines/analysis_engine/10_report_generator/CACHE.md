# Report Generator Cache

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Cache Specification)

---

# 1. Purpose

This document defines caching strategy for the Report Generator.

Caching must never alter report semantics or upstream result integrity.

---

# 2. Cache Layers

| Layer | Content | Notes |
|-------|---------|-------|
| Request-Scope Cache | Serializer helpers, layout resolution | Request-local only |
| Cross-Request ReportGeneratorResult Cache | Disabled by default | Only if governed runtime profile enables full semantic keying of InterpretationResult, AnalysisResult, and format profile |

Report Generator does not maintain interpretation or domain knowledge cache.

---

# 3. Engine Rules

- Assembly reads current upstream results from ReportAssemblyContext each assemble call
- Do not cache ReportGeneratorResult across requests unless semantic key includes InterpretationResult identity, AnalysisResult identity (when used), and format profile version
- Cache hits cannot bypass mandatory validation
- Cached report artifacts must not mask upstream result changes within the same request
- All format artifacts in a cached result must derive from the same StructuredReport key

---

# 4. Invalidation

Invalidate request-local helpers when assemble ends.

Cross-request cache invalidates when InterpretationResult, AnalysisResult, or format profile in the key changes.

---

# 5. Non-Goals

Cache specification does not:

- define storage technology
- cache InterpretationResult or AnalysisResult (owned by context/runtime)
- cache interpretive sentence libraries
- permit semantic shortcuts that skip validation or serialization

---

# 6. Acceptance Criteria

Cache specification is accepted when layers, engine rules, and invalidation behavior are complete.
