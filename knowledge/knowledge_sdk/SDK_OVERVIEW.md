# Knowledge SDK Overview

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (SDK Overview Specification)

---

# 1. Purpose

This document provides the canonical overview of SDK capabilities and usage boundaries for Runtime Engines.

---

# 2. What the SDK Is

The Knowledge SDK is a stable facade that unifies:

- Registry discovery, search, and metadata access
- Loader version resolution, dependency resolution, loading, validation, and cache control
- Engine-facing module/asset access under frozen session semantics

---

# 3. What the SDK Is Not

The SDK is not:

- a rule engine
- an interpretation engine
- a knowledge authoring tool
- a storage API
- a bypass around Registry governance or Loader integrity controls

---

# 4. Capability Map

| Capability | Primary Backing |
|------------|-----------------|
| FindModule / ListModules / SearchKnowledge | Registry |
| GetMetadata | Registry (+ Loader session metadata where relevant) |
| ResolveVersion / ResolveDependency | Loader (+ Registry declarations) |
| Validate / Compatibility Resolution | Loader + Registry |
| GetModule / GetAsset | Loader-bound KnowledgeSession |
| Refresh / Cache Access | Loader |

---

# 5. Typical Engine Flow

```text
Create / obtain KnowledgeSession context
        │
        ▼
ResolveVersion / ResolveDependency (as needed)
        │
        ▼
Validate
        │
        ▼
GetModule / GetAsset
        │
        ▼
Engine evaluates using declarative views + KnowledgeReferences
```

Discovery/search may precede resolution when the engine needs to locate candidates.

---

# 6. Session Freeze Guarantee

For one analysis request, selected module/asset versions are frozen in the KnowledgeSession.

Mid-request silent version drift is forbidden.

---

# 7. Consumer Classes

| Consumer | Usage |
|----------|-------|
| Analysis Engine | Primary analytical knowledge access |
| Interpretation Engine | Interpretive knowledge access |
| Report Engine | Template/presentation knowledge access where declared |
| Other Runtime Engines | Same SDK contracts only |

---

# 8. Acceptance Criteria

SDK Overview is accepted when capabilities, non-goals, backing map, and freeze guarantee are complete.
