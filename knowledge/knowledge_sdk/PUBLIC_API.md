# Knowledge SDK Public API

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Public API Specification)

---

# 1. Purpose

This document describes the logical Public API of the Knowledge SDK.

These are architectural contracts only.

No implementation, transport binding, or interface syntax is prescribed.

---

# 2. API Principles

- Single engine-facing facade
- Logical operations only
- Path-independent identities
- Version-aware
- Authorization-aware
- Deterministic for identical inputs and catalog revision
- No knowledge execution

---

# 3. Module Operations

## GetModule()

Returns a ModuleView for a resolved module identity/version within a KnowledgeSession.

## FindModule()

Finds a module catalog entry by identity and optional version filters.

## ListModules()

Lists modules by domain, status, consumer scope, or other discovery filters.

---

# 4. Asset Operations

## GetAsset()

Returns an AssetView for a resolved asset identity/version within a KnowledgeSession.

## ListAssets()

Lists assets by module, asset type, status, or other discovery filters.

---

# 5. Discovery and Metadata Operations

## SearchKnowledge()

Searches modules and assets by DiscoveryQuery and returns SearchResult set.

## GetMetadata()

Returns MetadataView for registry, module, or asset subjects.

---

# 6. Resolution Operations

## ResolveVersion()

Selects an exact version under constraints and consumer context.

## ResolveDependency()

Resolves DependencyResolution for a root module version.

---

# 7. Validation Operations

## Validate()

Validates a proposed or session-bound knowledge set and returns ValidationReport.

Compatibility Resolution is included as part of Validate outcomes and/or dedicated compatibility result fields.

---

# 8. Cache and Refresh Operations

## Refresh()

Reconsults Registry state and refreshes Loader-bound subjects according to policy.

Cache clear/refresh intents are exposed as governed Cache Access operations (see CACHE_ACCESS.md).

---

# 9. Session Semantics

Public access operations that return ModuleView / AssetView require a KnowledgeSession or equivalent request-scoped bind context.

Discovery-only operations may run without full materialization, subject to authorization.

---

# 10. Non-Goals

Public API does not include:

- EvaluateRule()
- InterpretKnowledge()
- RegisterModule() / RegisterAsset() as engine-facing defaults
- ExecuteEngine()
- direct storage open/read by path

---

# 11. Acceptance Criteria

Public API is accepted when all mandated logical operations, session rules, and non-goals are defined without implementation detail.
