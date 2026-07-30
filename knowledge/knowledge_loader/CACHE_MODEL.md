# Knowledge Loader Cache Model

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Cache Model Specification)

---

# 1. Purpose

This document defines cache strategy and invalidation for loaded Knowledge Modules and Assets.

Caching is a performance mechanism.

Caching must never alter knowledge semantics.

---

# 2. Cache Objectives

- reduce repeated load cost
- preserve deterministic request snapshots
- invalidate safely on catalog / version change
- remain transparent to Runtime Engines

---

# 3. Cache Entry

A CacheEntry shall include:

- module_id / asset_id
- version
- integrity_reference
- catalog_revision observed at load
- loaded timestamp
- last access timestamp
- retention class
- validation status

---

# 4. Cache Strategy Classes

| Strategy | Description |
|----------|-------------|
| No Cache | Always load fresh |
| Request Cache | Reuse within one request only |
| Session Cache | Reuse across requests in a session |
| Shared Cache | Process/shared reuse under governance |

Exact deployment choice is configuration; semantic guarantees remain mandatory.

---

# 5. Cache Invalidation Triggers

Invalidate when any of the following occur:

- Catalog Revision advances for the subject
- module/asset version is deprecated/retired relative to policy
- integrity reference mismatch
- explicit ClearCache / Refresh
- Reload Module targeting the subject
- compatibility status becomes Incompatible for the bound consumer set

---

# 6. Cache Hit Revalidation

A cache hit is not automatically trustworthy.

Revalidation shall confirm:

- identity/version still selected
- integrity_reference unchanged
- catalog freshness per policy
- consumer still authorized

Failed revalidation forces reload or error.

---

# 7. ClearCache / Refresh

## ClearCache

Removes cache entries by scope (all, module, asset, version).

## Refresh

Reconsults Registry state and reloads changed subjects according to policy.

---

# 8. Non-Goals

Cache Model does not:

- invent substitute knowledge on miss
- bypass validation
- mutate published knowledge content

---

# 9. Acceptance Criteria

Cache Model is accepted when entry schema, strategies, invalidation triggers, and revalidation rules are complete.
