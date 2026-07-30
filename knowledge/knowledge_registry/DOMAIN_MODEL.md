# Knowledge Registry Domain Model

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the logical entities of the Knowledge Registry domain.

These models describe registry catalog content, not runtime engine objects.

---

# 2. Core Entities

```text
KnowledgeRegistry
ModuleRegistryEntry
AssetRegistryEntry
RegistryMetadata
RegistryVersion
RegistryDiscoveryQuery
DependencyGraph
CompatibilityMatrix
ModuleStatus
AssetStatus
KnowledgeLifecycle
KnowledgeIndex
KnowledgeSearchResult
KnowledgeReference
```

---

# 3. KnowledgeRegistry

Represents the canonical catalog service and its authoritative module/asset inventories.

---

# 4. ModuleRegistryEntry

Represents a registered Knowledge Module catalog record, including identity, domain, versions, status, owners, consumers, and dependency declarations.

---

# 5. AssetRegistryEntry

Represents a registered Knowledge Asset catalog record belonging to a module, including asset type, identity, version, status, and references.

---

# 6. RegistryMetadata

Represents searchable descriptive metadata attached to registry, module, and asset entries.

---

# 7. RegistryVersion

Represents the version identity of the Registry specification and of cataloged module/asset publications.

---

# 8. RegistryDiscoveryQuery

Represents a logical discovery request against modules, assets, versions, domains, statuses, or metadata facets.

---

# 9. DependencyGraph

Represents directed dependency relationships among Knowledge Modules and, where declared, among Knowledge Assets.

---

# 10. CompatibilityMatrix

Represents declared compatibility between modules, assets, standards (KMS/KAS), and consumer engines.

---

# 11. ModuleStatus / AssetStatus

Represent lifecycle status values for modules and assets (for example Draft, Validated, Published, Deprecated, Retired).

Exact allowed enumerations are governed under Governance and Versioning models.

---

# 12. KnowledgeLifecycle

Represents the end-to-end lifecycle of knowledge from draft registration through publication, deprecation, and retirement.

---

# 13. KnowledgeIndex

Represents indexed facets used for discovery and search.

---

# 14. KnowledgeSearchResult

Represents ordered discovery results with matched identities, versions, and metadata summaries.

---

# 15. KnowledgeReference

Stable reference model used across Registry and consumers:

- module_id
- asset_id
- version
- category / type where applicable

---

# 16. Ownership

All domain entities above are owned by the Knowledge Registry unless explicitly owned by KMS, KAS, or individual Knowledge Modules.
