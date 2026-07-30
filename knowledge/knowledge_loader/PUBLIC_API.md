# Knowledge Loader Public API

**Component:** Knowledge Loader  
**Version:** V1.0.0  
**Status:** Frozen (Public API Specification)

---

# 1. Purpose

This document describes the logical Public API of the Knowledge Loader.

These are architectural contracts only.

No implementation, transport binding, or interface syntax is prescribed.

---

# 2. API Principles

- Logical operations only
- Path-independent identities
- Version-aware
- Authorization-aware
- Deterministic for identical inputs and catalog revision
- No knowledge execution

---

# 3. Module Operations

## LoadModule()

Loads a Knowledge Module version into runtime memory.

Inputs: module_id, version constraints?, consumer context, LoadMode?  
Outputs: KnowledgeHandle / LoadedModule summary  
Errors: NotFound, VersionResolution, Dependency, Compatibility, Integrity, Authorization

## UnloadModule()

Unloads a LoadedModule from active scope.

Inputs: KnowledgeHandle or module_id + version + scope  
Outputs: unload confirmation

## ReloadModule()

Reloads a module subject according to reload policy.

Inputs: KnowledgeHandle or module_id, version policy  
Outputs: new KnowledgeHandle  
Errors: same as LoadModule plus StateError

---

# 4. Asset Operations

## LoadAsset()

Loads a Knowledge Asset into runtime memory.

Inputs: module_id, asset_id, version constraints?, consumer context  
Outputs: KnowledgeHandle / LoadedAsset summary

## UnloadAsset()

Unloads a LoadedAsset from active scope.

Inputs: KnowledgeHandle or asset identity + scope  
Outputs: unload confirmation

## GetAsset()

Retrieves a loaded asset, triggering lazy load within frozen version set when enabled.

Inputs: KnowledgeHandle / asset identity  
Outputs: asset knowledge view

---

# 5. Access Operations

## GetKnowledge()

Retrieves loaded module knowledge views for engine consumption.

Inputs: KnowledgeHandle / module identity  
Outputs: module knowledge view

## Validate()

Runs Loader validation for a proposed load set without necessarily binding engines.

Inputs: LoadRequest or resolved subject set  
Outputs: validation report

---

# 6. Resolution Operations

## ResolveVersion()

Selects an exact version for a module or asset under constraints.

Inputs: identity, version range / policy, consumer context  
Outputs: VersionSelection

## ResolveDependency()

Resolves DependencyClosure for a root module version.

Inputs: module_id, version, resolution policy  
Outputs: DependencyClosure

---

# 7. Cache Operations

## ClearCache()

Clears cache entries by scope.

Inputs: scope (all / module / asset / version)  
Outputs: clear confirmation

## Refresh()

Reconsults Registry catalog state and refreshes loaded/cached subjects per policy.

Inputs: scope / subjects  
Outputs: refresh report

---

# 8. Non-Goals

Public API does not include:

- EvaluateRule()
- InterpretKnowledge()
- RegisterModule() (Registry concern)
- ExecuteEngine()

---

# 9. Acceptance Criteria

Public API is accepted when all mandated logical operations, inputs/outputs, and non-goals are defined without implementation detail.
