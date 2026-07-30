# Knowledge SDK Cache Access

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Cache Access Specification)

---

# 1. Purpose

This document defines governed cache control operations exposed by the Knowledge SDK.

Caching is owned operationally by the Knowledge Loader.

The SDK exposes only controlled cache intents to authorized consumers.

---

# 2. Cache Access Principles

- Cache must not alter knowledge semantics
- Engines should not depend on cache hit/miss for correctness
- Cache mutation is privileged relative to ordinary GetModule/GetAsset
- Request-scope freeze outranks shared cache convenience

---

# 3. Logical Cache Operations

## ClearCache()

Clears Loader cache entries by scope:

- all
- module
- asset
- version
- session

## Refresh()

Reconsults Registry catalog revision and refreshes loaded/cached subjects according to Loader policy.

## Cache Status (optional read)

May return non-authoritative cache residency summaries for diagnostics.

Diagnostics must not be required for engine correctness.

---

# 4. Authorization

Cache mutation operations require elevated authorization relative to ordinary knowledge read access.

Unauthorized ClearCache / Refresh attempts fail closed.

---

# 5. Interaction with KnowledgeSession

ClearCache / Refresh must not silently mutate an already frozen analysis KnowledgeSession.

Active request sessions either:

- remain on frozen snapshots until completion; or
- are explicitly invalidated according to governed policy, forcing rebind

---

# 6. Non-Goals

Cache Access does not:

- provide direct cache storage APIs
- allow engines to inject arbitrary cache payloads
- bypass integrity revalidation

---

# 7. Acceptance Criteria

Cache Access is accepted when operations, authorization, and session-safety rules are complete.
