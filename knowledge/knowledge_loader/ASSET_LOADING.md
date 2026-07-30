# Knowledge Asset Loading

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Asset Loading Specification)

---

# 1. Purpose

This document defines how Knowledge Assets are loaded, unloaded, cached, and validated at load time.

---

# 2. Load Asset

Load Asset materializes a Knowledge Asset version into runtime memory.

Preconditions:

- owning module is registered and selected version is known;
- asset_id exists in Registry under that module version;
- asset status is load-eligible;
- integrity and compatibility checks pass.

Effects:

- create LoadedAsset
- attach to LoadedModule / KnowledgeSnapshot
- optionally Cache Asset
- return asset KnowledgeHandle

---

# 3. Asset Load Modes

Assets may be loaded:

- eagerly with the module;
- lazily on first GetAsset;
- incrementally by asset group / type.

Selected mode must not change asset semantics.

---

# 4. Unload Asset

Unload Asset releases a LoadedAsset from active memory scope.

Module-level unload may cascade to owned loaded assets according to policy.

---

# 5. Cache Asset

Cache Asset stores a validated LoadedAsset according to CachePolicy.

Only integrity-validated assets may enter cache.

---

# 6. Validate Asset

Validate Asset at load time includes:

- structural loadability
- identity/version match
- integrity reference verification
- asset-type contract conformance evidence
- ownership consistency with module version

Content golden-dataset execution remains a Knowledge Module publication concern; Loader validates load-time integrity and contract evidence, not business interpretation.

---

# 7. GetAsset

GetAsset returns a loaded asset through KnowledgeHandle for engine consumption.

If lazy loading is enabled, GetAsset may trigger Load Asset within the frozen version set.

Crossing into a different unresolved version during lazy load is forbidden.

---

# 8. Acceptance Criteria

Asset Loading is accepted when load / unload / cache / validate / GetAsset semantics are complete and version-safe.
