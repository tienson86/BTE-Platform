# Knowledge SDK Error Model

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Error Model Specification)

---

# 1. Purpose

This document defines the classified error model returned by the Knowledge SDK to Runtime Engines.

---

# 2. Error Principles

- Fail closed for integrity and compatibility failures
- Errors are explicit and classified
- No silent incompatible substitution
- SDK translates lower-layer failures into a stable engine-facing model
- Engines must not invent embedded knowledge to bypass SDK errors

---

# 3. Error Classes

| Class | Typical Cause |
|-------|---------------|
| RequestError | Illegal arguments / incomplete request |
| AuthorizationError | Consumer not permitted |
| NotFound | Module/asset/version absent |
| VersionResolutionError | Unsatisfiable or ambiguous version selection |
| DependencyError | Unresolved required dependency or cycle |
| CompatibilityError | Incompatible subject/consumer set |
| IntegrityError | Integrity/load validation failure |
| ValidationError | Validate() failed for proposed set |
| CacheError | Cache clear/refresh/revalidation failure |
| SessionStateError | Illegal operation against frozen/invalid session |
| UnavailableError | Registry/Loader dependency temporarily unavailable |

---

# 4. SDKError Surface

SDKError shall include:

- error class
- operation name
- subject KnowledgeReference(s)
- summary message
- retryability flag
- correlated catalog_revision where relevant
- cause layer (Registry / Loader / SDK) as logical source class

---

# 5. Propagation Rules

- Registry NotFound → SDK NotFound
- Loader Integrity failure → SDK IntegrityError
- Loader Compatibility failure → SDK CompatibilityError
- Authorization denial at either layer → SDK AuthorizationError

Engines depend on SDK classes, not lower-layer private error types.

---

# 6. Recovery Guidance

Retryable errors may be retried after Refresh where policy allows.

Non-retryable integrity/compatibility errors require governed knowledge correction or explicit compatible rebind.

---

# 7. Acceptance Criteria

Error Model is accepted when classes, surface fields, propagation, and recovery guidance are complete.
