# Summary Engine Cache

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Cache Specification)

---

# 1. Purpose

This document defines caching strategy for the Summary Engine.

Caching must never alter summary semantics or upstream result integrity.

---

# 2. Cache Layers

| Layer | Content | Notes |
|-------|---------|-------|
| Request-Scope Cache | Pure aggregation helpers | Request-local only |
| Cross-Request SummaryResult Cache | Disabled by default | Only if governed runtime profile enables full semantic keying of all eight upstream results |

Summary Engine does not maintain a domain knowledge cache; it aggregates published StageResults only.

---

# 3. Engine Rules

- Aggregation reads current upstream results from AnalysisContext each evaluate call
- Do not cache SummaryResult across requests unless semantic key includes all eight upstream result identities/versions
- Cache hits cannot bypass mandatory validation
- Cached summary must not mask upstream result changes within the same request

---

# 4. Invalidation

Invalidate request-local helpers when evaluate ends.

Cross-request cache invalidates when any upstream stage result version/content in the key changes.

---

# 5. Non-Goals

Cache specification does not:

- define storage technology
- cache upstream StageResults (owned by context/runtime)
- permit semantic shortcuts that skip consistency validation

---

# 6. Acceptance Criteria

Cache specification is accepted when layers, engine rules, and invalidation behavior are complete.
