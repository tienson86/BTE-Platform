# Sentence Library Specification

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Sentence Library Architecture)

---

# 1. Purpose

This document defines the architecture of Sentence Libraries within the Knowledge Layer.

Sentence Libraries store interpretive language assets consumed by the Interpretation Engine.

---

# 2. Scope

A Sentence Library contains:

- sentence templates
- intent tags
- variable bindings
- tone / style metadata
- localization keys
- selection constraints
- manifests

It does not contain:

- analytical scoring logic
- Useful God / Pattern recomputation
- report page layout
- engine orchestration

---

# 3. Ownership

Primary owner:

- Interpretation Knowledge

Sentence assets may be organized by analytical domain tags such as Strength, Temperature, Pattern, or Useful God, but ownership remains with Interpretation Knowledge.

---

# 4. Sentence Architecture

```text
Sentence Library
   │
   ├── Domains / Tags
   ├── Sentence Templates
   ├── Variable Schemas
   ├── Selection Rules
   ├── Style Profiles
   └── Manifest
```

---

# 5. Sentence Definition Requirements

Every sentence asset shall define:

- sentence_id
- version
- domain tags
- intent
- template body
- required variables
- optional variables
- tone / style
- localization key
- status

---

# 6. Binding Model

Sentence templates bind only to published analytical result fields and shared context metadata.

Forbidden bindings:

- raw unpublished engine internals
- mutable temporary calculation state
- physical knowledge paths

---

# 7. Selection Model

Sentence selection may use:

- domain tags
- analytical classifications
- confidence thresholds
- locale
- style profile

Selection policy is knowledge-defined.

Rendering execution belongs to Interpretation Engine.

---

# 8. Consumption Contract

Interpretation Engine consumes Sentence Libraries only through:

```text
Abstract Interpretation Knowledge Module
```

No hard-coded repository path is permitted in engine contracts.

---

# 9. Validation Requirements

Before publication, Sentence Libraries shall validate:

- unique sentence IDs
- valid variable schemas
- resolvable domain tags
- localization completeness for declared locales
- template syntax integrity

---

# 10. Traceability

Every generated interpretive statement shall retain KnowledgeReferences to the sentence assets used.

---

# 11. Extensibility

Additional languages, tones, and domain tags may be introduced within V1.x without breaking abstract contracts.
