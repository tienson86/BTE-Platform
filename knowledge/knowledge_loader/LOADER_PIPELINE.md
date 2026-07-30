# Knowledge Loader Pipeline

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Loader Pipeline Specification)

---

# 1. Purpose

This document defines the canonical loading pipeline from request to engine-consumable knowledge handles.

---

# 2. Pipeline Overview

```text
Receive LoadRequest
        │
        ▼
Authorize Consumer
        │
        ▼
Resolve Version
        │
        ▼
Resolve Dependencies
        │
        ▼
Check Compatibility
        │
        ▼
Check Cache
        │
        ├── Cache Hit → Revalidate → Bind Snapshot
        │
        └── Cache Miss
                │
                ▼
        Load Module / Assets
                │
                ▼
        Validate Integrity
                │
                ▼
        Populate Cache (policy-dependent)
                │
                ▼
        Freeze KnowledgeSnapshot
                │
                ▼
        Return KnowledgeHandle(s)
```

---

# 3. Stage Definitions

## 3.1 Receive LoadRequest

Capture requested module/asset identities, consumer context, version constraints, and LoadMode.

## 3.2 Authorize Consumer

Verify the consumer is permitted to load the requested knowledge status class.

## 3.3 Resolve Version

Select exact versions according to Version Selection policy and Registry declarations.

## 3.4 Resolve Dependencies

Compute DependencyClosure for required dependencies.

## 3.5 Check Compatibility

Validate Compatibility Matrix constraints for the resolved set and consumer.

## 3.6 Check Cache

Lookup CacheEntry candidates for the resolved identities/versions.

## 3.7 Load Module / Assets

Materialize knowledge into runtime memory using the selected LoadMode.

## 3.8 Validate Integrity

Perform Integrity Checking before exposure to engines.

## 3.9 Freeze KnowledgeSnapshot

Bind the resolved set for the request scope so versions cannot drift mid-request.

## 3.10 Return Handles

Provide KnowledgeHandle / GetKnowledge access to Runtime Engines.

---

# 4. Unload / Reload / Refresh Paths

```text
Unload:  Handle scope end → release or retain per CachePolicy
Reload:  Invalidate target → re-enter pipeline for same logical identity
Refresh: Reconsult Registry catalog revision → reload if changed
```

---

# 5. Failure Points

Any stage may fail closed with a classified LoaderError.

Partial exposure of unvalidated knowledge is forbidden.

---

# 6. Non-Goals

The pipeline does not evaluate rules, score charts, or generate interpretation text.

---

# 7. Acceptance Criteria

Loader Pipeline is accepted when stages, freeze semantics, cache branch behavior, and fail-closed rules are complete.
