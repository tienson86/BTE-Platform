# Knowledge SDK Asset Access

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Asset Access Specification)

---

# 1. Purpose

This document defines engine-facing access to Knowledge Assets through the SDK.

---

# 2. GetAsset()

GetAsset returns a declarative AssetView.

Preconditions:

- owning module context known
- asset version resolved within frozen session set
- consumer authorized
- integrity gates passed

AssetView exposes:

- asset_id / module_id / version
- asset_type
- status
- declarative content accessors appropriate to asset type
- metadata summary
- KnowledgeReferences

AssetView does not evaluate rules or formulas.

---

# 3. ListAssets()

ListAssets returns filtered asset summaries by module, type, status, or tags.

Listing may be catalog-only; content retrieval requires GetAsset under session bind.

---

# 4. Lazy Materialization

If Loader lazy loading is enabled, GetAsset may trigger asset materialization within the already frozen version set.

Crossing into a different unresolved version during lazy get is forbidden.

---

# 5. Asset Type Neutrality

SDK Asset Access is type-agnostic at the facade level.

Asset-type contracts remain defined by KAS; engines consume typed declarative views without SDK interpreting domain meaning.

---

# 6. Error Conditions

Asset Access may raise:

- NotFound
- AuthorizationError
- VersionResolutionError
- IntegrityError
- SessionStateError
- DependencyError when owning module closure is incomplete

---

# 7. Acceptance Criteria

Asset Access is accepted when Get/List semantics, lazy-load version safety, and non-execution guarantees are complete.
