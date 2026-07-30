# Knowledge SDK Performance Model

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Performance Model Specification)

---

# 1. Purpose

This document defines performance principles for the Knowledge SDK.

Correctness outranks performance.

---

# 2. Performance Goals

- minimize redundant Registry/Loader round-trips via session reuse
- support discovery without mandatory full materialization
- preserve deterministic freeze semantics even under caching
- keep facade overhead small relative to load/validation cost

---

# 3. Operation Cost Classes (Logical)

| Operation Class | Relative Cost Expectation |
|-----------------|---------------------------|
| Find / List / GetMetadata / Search | Catalog/index oriented |
| ResolveVersion / ResolveDependency / Validate | Resolution/validation oriented |
| GetModule / GetAsset (cold) | Materialization oriented |
| GetModule / GetAsset (warm session/cache) | Lower after revalidation |
| Refresh / ClearCache | Privileged operational cost |

---

# 4. Session Reuse

Engines should reuse a KnowledgeSession within one analysis request.

Re-resolving and reloading the same identities repeatedly within one request is discouraged unless explicitly required after invalidation.

---

# 5. Mandatory Safety Overhead

Authorization, compatibility, and integrity checks are mandatory where applicable.

Performance optimizations must not skip these gates.

---

# 6. Observability Metrics (Logical)

- API latency by operation
- session hit vs rebind counts
- validation failure counts by class
- cache-influenced get latency (diagnostic only)

Metric transport is out of scope.

---

# 7. Non-Goals

Performance Model does not mandate concurrency primitives, batching protocols, or specific cache algorithms.

---

# 8. Acceptance Criteria

Performance Model is accepted when goals, cost classes, session reuse guidance, and mandatory safety overhead are complete.
