# Analysis Module Lifecycle

**Component:** Analysis Runtime  
**Version:** V1.0.0  
**Status:** Frozen Runtime Baseline

---

# 1. Purpose

This document defines the lifecycle of Analysis Modules within the Analysis Runtime.

---

# 2. Module Lifecycle States

```text
Registered
    │
    ▼
Resolved (knowledge + contract ready)
    │
    ▼
Ready
    │
    ▼
Executing
    │
    ├── Succeeded → Published StageResult
    │
    └── Failed → Error surfaced to Runtime
    │
    ▼
Released (end of request scope)
```

---

# 3. Registration

Analysis Modules are registered with the Runtime by stable module identity and version-compatible stage contract.

Registration does not load knowledge content by itself.

---

# 4. Resolution

Before execution, Runtime ensures:

- module contract is Compatible with Runtime Spec
- required knowledge modules are resolvable through SDK
- prerequisite StageResults will be available by pipeline position

---

# 5. Ready

A module is Ready when admission checks for its stage are satisfied and KnowledgeSession is frozen.

---

# 6. Executing

Runtime invokes `evaluate(context)` exactly once per request for required stages.

Re-entrant execution of the same stage in one request is forbidden unless an explicit governed retry policy recreates a clean stage attempt without committing partial mutation.

---

# 7. Succeeded / Failed

Succeeded stages publish immutable StageResult into shared context.

Failed stages raise classified errors; Runtime applies Error Recovery policy.

---

# 8. Released

At request completion or abort, module execution scope is released.

Cached knowledge remains under SDK/Loader policy and does not keep stage execution state.

---

# 9. Module Dependencies

Modules depend on:

- Analysis Runtime contracts
- Knowledge SDK session access
- prior StageResults according to pipeline position
- assigned Knowledge Modules for their domain

Modules do not depend on Interpretation or Report Engines.

---

# 10. Acceptance Criteria

Module Lifecycle is accepted when states, invocation cardinality, and dependency boundaries are complete.
