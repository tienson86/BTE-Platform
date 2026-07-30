# ShenSha Engine Cache

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Cache Specification)

---

# 1. Purpose

This document defines caching strategy for the ShenSha Engine.

Caching must never alter ShenSha analytical semantics.

---

# 2. Cache Layers

| Layer | Content | Notes |
|-------|---------|-------|
| Knowledge Cache | ShenSha Knowledge via SDK/Loader | Owned by Knowledge Loader; accessed through SDK |
| Request-Scope Cache | Validated knowledge handles / pure helpers | Request-local only |
| Cross-Request StageResult Cache | Disabled by default | Only if governed runtime profile enables full semantic keying |

---

# 3. Engine Rules

- Prefer reuse of frozen KnowledgeSession handles provided by Analysis Runtime
- Do not reload knowledge with different versions mid-evaluate
- Do not cache mutable intermediate analytical state across requests by default
- Cache hits cannot bypass mandatory validation

---

# 4. Invalidation

Invalidate request-local helpers when:

- evaluate ends
- knowledge session is invalidated/refreshed by Runtime
- validation detects integrity mismatch

---

# 5. Non-Goals

Cache specification does not:

- define storage technology
- permit semantic shortcuts
- replace Knowledge SDK cache controls

---

# 6. Acceptance Criteria

Cache specification is accepted when layers, engine rules, and invalidation behavior are complete.
