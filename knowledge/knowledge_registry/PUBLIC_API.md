# Knowledge Registry Public API

**Component:** Knowledge Registry  
**Version:** V1.0.0  
**Status:** Frozen (Public API Specification)

---

# 1. Purpose

This document describes the logical Public API of the Knowledge Registry.

These are architectural contracts only.

No implementation, transport binding, or interface syntax is prescribed.

---

# 2. API Principles

- Logical operations only
- Path-independent identities
- Version-aware
- Authorization-aware
- Deterministic outcomes
- No knowledge execution

---

# 3. Module Operations

## Register Module

Registers a new Knowledge Module version.

Inputs: module registration payload  
Outputs: Module Registry Entry  
Errors: duplicate identity, validation failure, authorization failure

## Update Module

Updates allowed catalog fields or progresses lifecycle status.

Inputs: module_id, version, update payload  
Outputs: updated Module Registry Entry  
Errors: immutability violation, invalid transition, authorization failure

## Remove Module

Performs governed removal / archival according to lifecycle policy.

Inputs: module_id, version, removal mode  
Outputs: removal / archival record  
Errors: active consumer conflict, retention violation, authorization failure

## Find Module

Retrieves a module by identity and optional version.

Inputs: module_id, version?  
Outputs: Module Registry Entry  
Errors: not found, authorization failure

## List Versions (Module)

Lists version history for a module.

Inputs: module_id, status filters?  
Outputs: ordered version list

---

# 4. Asset Operations

## Register Asset

Registers a new Knowledge Asset version under a module.

Inputs: asset registration payload  
Outputs: Asset Registry Entry

## Update Asset

Updates allowed catalog fields or lifecycle status.

Inputs: asset_id, module_id, version, update payload  
Outputs: updated Asset Registry Entry

## Remove Asset

Performs governed removal / archival.

Inputs: asset_id, module_id, version, removal mode  
Outputs: removal / archival record

## Find Asset

Retrieves an asset by identity and optional version.

Inputs: asset_id, module_id?, version?  
Outputs: Asset Registry Entry

## List Versions (Asset)

Lists version history for an asset.

Inputs: asset_id, module_id  
Outputs: ordered version list

---

# 5. Dependency and Compatibility Operations

## Resolve Dependency

Resolves a dependency closure for a module version or requested set.

Inputs: root module_id / version, resolution policy  
Outputs: resolved dependency set + KnowledgeReferences  
Errors: unresolved required dependency, cycle, incompatible set

## Validate Compatibility

Validates compatibility for a proposed module/asset set.

Inputs: subject set, consumer context?  
Outputs: compatibility report  
Errors: incompatible pair, unknown production status

---

# 6. Discovery Operations

## Search Knowledge

Searches modules and assets by discovery query.

Inputs: RegistryDiscoveryQuery  
Outputs: KnowledgeSearchResult set

## Find by KnowledgeReference

Resolves a KnowledgeReference to catalog identity.

Inputs: KnowledgeReference  
Outputs: Module or Asset Registry Entry summary

---

# 7. Catalog Operations

## Get Registry Metadata

Returns registry metadata and catalog revision.

## Get Compatibility Matrix

Returns matrix entries for a subject or subject set.

## Get Dependency Graph

Returns graph slice for a subject or subject set.

---

# 8. Non-Goals

Public API does not include:

- Evaluate Rule
- Execute Formula
- Run Engine
- Load physical files by repository path

---

# 9. Acceptance Criteria

Public API is accepted when all mandated logical operations, inputs/outputs, and non-goals are defined without implementation detail.
