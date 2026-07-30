# Knowledge SDK Changelog

**Component:** Knowledge SDK

This document records architecture and specification changes for the Knowledge SDK.

The changelog follows Semantic Versioning (SemVer).

---

# Version 1.0.0

**Status:** Frozen Architecture Baseline

## Overview

Version 1.0.0 establishes the architectural baseline for the Knowledge SDK.

The SDK is the only public interface between Runtime Engines and the Knowledge Layer.

It composes Knowledge Registry discovery/metadata and Knowledge Loader resolution/loading behind one stable facade.

It does not execute business rules and does not interpret knowledge.

No implementation code is included in this milestone.

---

## Added

### Documentation

- README.md
- ARCHITECTURE.md
- DOMAIN_MODEL.md
- SDK_OVERVIEW.md
- PUBLIC_API.md
- MODULE_ACCESS.md
- ASSET_ACCESS.md
- CACHE_ACCESS.md
- VERSION_RESOLUTION.md
- DEPENDENCY_RESOLUTION.md
- ERROR_MODEL.md
- SECURITY_MODEL.md
- PERFORMANCE_MODEL.md
- GOVERNANCE.md
- VERSIONING.md
- CHANGELOG.md

### Scope

- Module Access
- Asset Access
- Registry Access
- Loader Access
- Cache Access
- Version Resolution
- Compatibility Resolution
- Validation
- Search
- Discovery
- Metadata Access
- Dependency Resolution

### Logical Public API

GetModule() · GetAsset() · FindModule() · SearchKnowledge() · ResolveVersion() · ResolveDependency() · Validate() · Refresh() · GetMetadata() · ListModules() · ListAssets()

---

## Compatibility

Compatible with:

- Knowledge Architecture V1.x
- Knowledge Module Standard (KMS) V1.x
- Knowledge Asset Standard (KAS) V1.x
- Knowledge Registry V1.x
- Knowledge Loader V1.x
- Analysis Engine / Interpretation Engine abstract consumption model

---

## Known Limitations

Runtime SDK implementation, language bindings, and deployment policy profiles are not included in this architecture baseline.

Future work includes implementation against these frozen contracts.

---

## Upgrade Policy

### Minor Versions (1.x)

Additive compatible extensions and clarifications only.

### Major Versions (2.x)

Required for breaking SDK contracts or incompatible engine-facing semantics.

---

## Freeze Declaration

Version **1.0.0** is designated as the official Frozen Architecture Baseline for the Knowledge SDK.
