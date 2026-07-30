# Knowledge SDK Domain Model

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Knowledge SDK domain.

These models describe SDK access contracts, not engine evaluation objects.

---

# 2. Core Entities

```text
KnowledgeSDK
KnowledgeSession
ModuleView
AssetView
DiscoveryQuery
SearchResult
VersionResolution
DependencyResolution
CompatibilityResolution
ValidationReport
MetadataView
CacheCommand
SDKError
KnowledgeReference
```

---

# 3. KnowledgeSDK

Represents the public facade service used by Runtime Engines.

---

# 4. KnowledgeSession

Represents a request-scoped or governed session binding to a frozen knowledge snapshot set resolved through the Loader.

---

# 5. ModuleView

Represents an engine-consumable declarative view of a Knowledge Module.

---

# 6. AssetView

Represents an engine-consumable declarative view of a Knowledge Asset.

---

# 7. DiscoveryQuery / SearchResult

Represent discovery/search requests and ranked results from Registry-backed indexes via SDK.

---

# 8. VersionResolution

Represents the outcome of ResolveVersion for a module or asset.

---

# 9. DependencyResolution

Represents the outcome of ResolveDependency for a root module version.

---

# 10. CompatibilityResolution

Represents compatibility evaluation outcomes for a proposed subject set and consumer.

---

# 11. ValidationReport

Represents Validate outcomes prior to or after binding.

---

# 12. MetadataView

Represents registry/module/asset metadata summaries returned to engines.

---

# 13. CacheCommand

Represents governed ClearCache / Refresh intents issued through the SDK.

---

# 14. SDKError

Represents classified SDK failures translated from Registry/Loader/security conditions.

---

# 15. KnowledgeReference

Stable reference model shared across Registry, Loader, SDK, and engines:

- module_id
- asset_id
- version
- category / type where applicable

---

# 16. Ownership

All domain entities above are owned by the Knowledge SDK unless explicitly owned by Registry, Loader, KMS, KAS, or Runtime Engines.
