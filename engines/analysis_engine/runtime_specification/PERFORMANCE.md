# Analysis Runtime Performance

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document defines performance strategy for Analysis Runtime.

Correctness and determinism outrank performance.

---

# 2. Performance Goals

- bound stage orchestration overhead relative to module work
- reuse frozen KnowledgeSession within a request
- avoid redundant SDK resolution calls inside one Execution Unit
- support concurrent isolated requests without shared mutable analytical state
- expose logical metrics for stage latency and failure rates

---

# 3. Strategy

| Strategy | Rule |
|----------|------|
| Knowledge bind once | Resolve/load required knowledge at Phase B; reuse handles in stages |
| Sequential stages | Preserve canonical order; no speculative stage skip |
| Lazy knowledge gets | Allowed only within frozen version set |
| Cache | Use Cache Model without semantic drift |
| Isolation | Prefer per-request isolation over cross-request semantic memoization by default |

---

# 4. Forbidden Optimizations

- reordering stages for speed
- skipping validation gates
- sharing mutable context across requests
- bypassing SDK for direct knowledge package reads
- approximating StageResults

---

# 5. Logical Metrics

- total request latency
- per-stage latency
- knowledge bind latency
- validation failure counts by class
- cache hit/miss (diagnostic)

Metric transport is out of scope.

---

# 6. Acceptance Criteria

Performance strategy is accepted when goals, strategies, forbidden optimizations, and metrics are complete.
