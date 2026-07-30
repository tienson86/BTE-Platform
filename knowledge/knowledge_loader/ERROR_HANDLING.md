# Knowledge Loader Error Handling

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Error Handling Specification)

---

# 1. Purpose

This document defines error classification and recovery behavior for the Knowledge Loader.

---

# 2. Error Principles

- Fail closed for integrity and compatibility failures
- Errors are explicit and classified
- No silent substitution of incompatible knowledge
- No rule execution as a recovery mechanism
- Request snapshot consistency is preserved or the request fails

---

# 3. Error Classes

| Class | Examples |
|-------|----------|
| RequestError | Missing identity, illegal LoadMode |
| AuthorizationError | Consumer not permitted |
| NotFoundError | Module/asset/version absent in Registry |
| VersionResolutionError | Ambiguous or unsatisfiable version range |
| DependencyError | Unresolved required dependency or cycle |
| CompatibilityError | Incompatible module/consumer set |
| IntegrityError | Integrity reference mismatch / corrupt snapshot |
| CacheError | Cache corruption or failed revalidation |
| LoadError | Materialization failure |
| StateError | Illegal unload/reload against frozen snapshot policy |

---

# 4. Error Surface

LoaderError shall include:

- error class
- subject KnowledgeReference(s)
- stage in Loader Pipeline
- human-readable summary
- retryability flag
- correlated catalog_revision where relevant

---

# 5. Error Recovery

## Allowed Recovery

- retry after Refresh when retryability is true
- reload after ClearCache for cache-related failures
- select an explicitly governed compatible substitute version only when policy authorizes and Compatibility Validation passes

## Forbidden Recovery

- ignore integrity failure
- load Draft knowledge for production consumers by default
- invent missing assets
- continue with partial required dependency closure

---

# 6. Propagation to Engines

Runtime Engines receive classified failures through Loader API error contracts.

Engines must not catch Loader integrity failures and continue with ad hoc embedded knowledge.

---

# 7. Acceptance Criteria

Error Handling is accepted when classes, surface fields, allowed/forbidden recovery, and engine propagation rules are complete.
