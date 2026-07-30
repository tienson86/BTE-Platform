# Knowledge Loader Domain Model

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Knowledge Loader domain.

These models describe loader runtime catalog and memory-management concepts, not engine evaluation objects.

---

# 2. Core Entities

```text
KnowledgeLoader
LoadRequest
LoadedModule
LoadedAsset
KnowledgeSnapshot
LoadMode
CacheEntry
CachePolicy
VersionSelection
DependencyClosure
CompatibilityCheck
IntegrityCheck
LoaderError
KnowledgeHandle
KnowledgeReference
```

---

# 3. KnowledgeLoader

Represents the loader service that resolves, validates, caches, and exposes knowledge to Runtime Engines.

---

# 4. LoadRequest

Represents a request to load modules/assets with consumer context, version constraints, and load mode.

---

# 5. LoadedModule

Represents a module snapshot successfully loaded into runtime memory, including selected version and dependency closure references.

---

# 6. LoadedAsset

Represents an asset snapshot successfully loaded into runtime memory under a LoadedModule.

---

# 7. KnowledgeSnapshot

Represents the frozen set of loaded modules/assets bound to one analysis request or loader session scope.

---

# 8. LoadMode

Represents loading strategy:

- Eager Loading
- Lazy Loading
- Incremental Loading

---

# 9. CacheEntry / CachePolicy

Represent cached loaded snapshots and retention / invalidation policy.

---

# 10. VersionSelection

Represents the outcome of Resolve Version for a module or asset under declared constraints.

---

# 11. DependencyClosure

Represents the resolved required dependency set for a root module version.

---

# 12. CompatibilityCheck / IntegrityCheck

Represent validation outcomes required before binding knowledge to consumers.

---

# 13. LoaderError

Represents classified load, validation, resolution, or cache failures.

---

# 14. KnowledgeHandle

Represents an opaque runtime handle returned to engines for GetKnowledge / GetAsset access without exposing storage internals.

---

# 15. KnowledgeReference

Stable reference model shared with Registry and engines:

- module_id
- asset_id
- version
- category / type where applicable

---

# 16. Ownership

All domain entities above are owned by the Knowledge Loader unless explicitly owned by Registry, KMS, KAS, or Runtime Engines.
