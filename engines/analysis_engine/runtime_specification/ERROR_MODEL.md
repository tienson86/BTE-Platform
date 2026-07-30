# Analysis Runtime Error Model

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document defines error classification and recovery behavior for Analysis Runtime.

---

# 2. Error Principles

- Fail closed on validation, integrity, and compatibility failures
- Errors are classified and attributable to stage/runtime/knowledge layers
- No silent stage skip on required failures
- No embedded substitute knowledge inside runtime to bypass SDK errors
- Deterministic error class for equivalent failure conditions

---

# 3. Error Classes

| Class | Typical Cause |
|-------|---------------|
| AdmissionError | Invalid input AnalysisContext |
| KnowledgeError | SDK resolve/load/validate failure |
| CompatibilityError | Incompatible knowledge/engine set |
| IntegrityError | Knowledge integrity failure |
| PrerequisiteError | Missing prior StageResult |
| StageExecutionError | Module evaluate failure |
| ValidationError | Pre/post/final validation failure |
| CacheError | Runtime cache corruption/revalidation failure |
| StateError | Illegal lifecycle/order violation |
| AbortedError | Governed abort |

---

# 4. Error Surface

Runtime errors shall include:

- error class
- stage id (if applicable)
- KnowledgeReference(s) when knowledge-related
- summary
- retryability flag
- correlation to ExecutionMetadata

---

# 5. Error Recovery

## Allowed

- governed retry of a failed stage only under explicit retry policy with no committed corrupt context mutation
- request abort with classified error
- retry whole Execution Unit after knowledge Refresh when retryable KnowledgeError

## Forbidden

- skip required stage and continue as success
- invent StageResult defaults to force completion
- continue after integrity/compatibility failure
- call Interpretation Engine with partial success labeled complete

---

# 6. Propagation

Module errors are translated into Runtime Error Model for orchestrator and API surfaces.

Downstream engines do not receive ambiguous partial “success” payloads.

---

# 7. Acceptance Criteria

Error Model is accepted when classes, surface, recovery allow/forbid rules, and propagation are complete.
