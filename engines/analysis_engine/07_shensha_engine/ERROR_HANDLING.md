# ShenSha Engine Error Handling

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Error Handling Specification)

---

# 1. Purpose

This document defines error classification and handling for the ShenSha Engine.

---

# 2. Error Principles

- Fail closed
- Explicit classification
- No silent defaults for mandatory evidence
- No upstream recomputation as recovery
- No SDK bypass as recovery
- Align with Analysis Runtime Error Model

---

# 3. Error Classes

| Class | Typical Cause |
|-------|---------------|
| ValidationError | Invalid AnalysisContext |
| PrerequisiteError | Missing required upstream stage results |
| KnowledgeError | SDK resolve/load/get failure for ShenSha Knowledge |
| CompatibilityError | Incompatible knowledge/runtime set |
| IntegrityError | Knowledge integrity failure |
| ExecutionError | Internal evaluation failure |
| ConflictResolutionError | Unable to deterministically resolve required conflicts |
| StateError | Illegal invocation/lifecycle usage |

---

# 4. Error Surface

Errors shall include:

- error class
- stage identity (`shensha`)
- subject KnowledgeReference(s) when applicable
- missing upstream field identity when applicable
- summary
- retryability flag

---

# 5. Recovery Policy

## Allowed

- whole-stage retry under Analysis Runtime governed retry policy
- request-level retry after knowledge Refresh when KnowledgeError is retryable

## Forbidden

- invent ShenSha outcomes without knowledge
- skip interaction/exception resolution and publish incomplete success
- recompute upstream analytical domains locally
- continue after integrity/compatibility failure

---

# 6. Propagation

Errors propagate to Analysis Runtime orchestrator.

No successful ShenShaResult is returned on mandatory failure.

---

# 7. Acceptance Criteria

Error Handling is accepted when classes, surface, recovery allow/forbid rules, and propagation are complete.
