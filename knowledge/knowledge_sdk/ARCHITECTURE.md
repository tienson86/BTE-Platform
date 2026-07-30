# Knowledge SDK Architecture

**Component:** Knowledge SDK  
**Version:** V1.0.0  
**Status:** Frozen (Architecture Baseline)

---

# 1. Purpose

This document defines the logical architecture of the Knowledge SDK.

---

# 2. Architectural Goals

The SDK shall:

- be the sole public interface for Runtime Engines to the Knowledge Layer;
- compose Registry discovery and Loader binding behind one stable facade;
- preserve path-independent identities and frozen request snapshots;
- expose only declarative knowledge access, never execution;
- isolate engines from Registry/Loader internal APIs and storage details.

---

# 3. Layer Position

```text
Knowledge Registry
        │
        ▼
Knowledge Loader
        │
        ▼
Knowledge SDK
        │
        ├── Module Access Facade
        ├── Asset Access Facade
        ├── Discovery / Search Facade
        ├── Version / Dependency Facade
        ├── Validation Facade
        ├── Metadata Facade
        ├── Cache Control Facade
        ├── Error Translation
        │
        ▼
Runtime Engines
```

---

# 4. Separation of Concerns

## Knowledge SDK Owns

- public engine-facing API contracts
- orchestration of Registry + Loader calls for engine use cases
- request-scoped knowledge session handles
- error translation into SDK Error Model
- consumer authorization presentation to lower layers

## Knowledge SDK Does Not Own

- catalog authorship (Registry)
- materialization internals (Loader)
- business-rule evaluation
- engine scoring / matching / narrative generation
- knowledge content mutation

## Knowledge Registry Owns

- catalog, discovery index, compatibility matrix declarations

## Knowledge Loader Owns

- load, cache, integrity validation, snapshot freeze

## Runtime Engines Own

- consumption of SDK-returned knowledge views
- domain evaluation using KnowledgeReferences

---

# 5. Composition Model

```text
Engine Request
    │
    ▼
SDK Public API
    │
    ├── Registry Access (find / search / metadata / compatibility declarations)
    │
    └── Loader Access (resolve / load / get / validate / refresh / cache)
            │
            ▼
      Frozen Knowledge Session
            │
            ▼
      Engine consumption via GetModule / GetAsset
```

---

# 6. Identity Model

All SDK operations use logical identities:

- module_id
- asset_id
- version
- KnowledgeReference

Physical location is never part of the public SDK contract.

---

# 7. Bypass Prohibition

Runtime Engines must not:

- import Knowledge Module packages directly;
- call Registry or Loader internal interfaces;
- embed substitute business knowledge to avoid SDK failures.

---

# 8. Constraints

- One canonical Knowledge SDK for platform engines.
- SDK must not execute rules.
- SDK must not interpret knowledge meaning.
- Failures are explicit and classified.
