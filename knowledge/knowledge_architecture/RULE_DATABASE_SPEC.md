# Rule Database Specification

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Database Architecture)

---

# 1. Purpose

This document defines the architecture of Rule Databases within the Knowledge Layer.

Rule Databases store analytical decision knowledge consumed by Analysis Engine stages.

---

# 2. Scope

A Rule Database contains:

- rule definitions
- categories
- priorities
- weights
- thresholds
- examples
- indexes
- manifests

It does not contain:

- engine algorithms
- interpretation sentences
- report layouts
- runtime state

---

# 3. Ownership Model

Each analytical Knowledge Module owns one Rule Database domain.

Examples:

| Knowledge Module | Rule Domain |
|------------------|-------------|
| Strength Knowledge | Strength Rules |
| Temperature Knowledge | Temperature Rules |
| Pattern Knowledge | Pattern Rules |
| Useful God Knowledge | Useful God Rules |

---

# 4. Rule Architecture

```text
Rule Database
   │
   ├── Categories
   ├── Rules
   ├── Priority Model
   ├── Weight Model
   ├── Threshold Model
   ├── Examples
   └── Manifest
```

---

# 5. Rule Definition Requirements

Every rule shall define:

- rule_id
- version
- category
- status
- priority
- conditions
- effects
- evidence requirements
- effective dating

Rules shall be immutable after publication within a version.

---

# 6. Category Model

Rule categories are domain-specific and defined by the owning Knowledge Module.

Category examples may include:

- seasonal
- structural
- candidate generation
- conflict resolution
- priority resolution
- confidence

Categories must be declared in the module manifest.

---

# 7. Priority and Conflict Model

When multiple rules match:

1. Apply declared priority.
2. Apply conflict-resolution rules if present.
3. Preserve deterministic ordering.
4. Record resolution evidence.

Engines execute priority mechanics.

Rule Databases supply priority data.

---

# 8. Consumption Contract

Engines consume Rule Databases only through:

```text
Abstract Knowledge Module → Rule Catalog / Rule Query APIs
```

Engines shall not:

- open physical directories by hard-coded path;
- parse unpublished drafts;
- mutate rule content;
- invent undocumented rules.

---

# 9. Validation Requirements

Before publication, Rule Databases shall validate:

- unique rule IDs
- valid categories
- valid references
- priority consistency
- schema conformance
- example integrity

Invalid Rule Databases shall not be published.

---

# 10. Traceability

Every matched rule in an engine result shall produce a KnowledgeReference containing:

- module_id
- rule_id
- rule version
- category

---

# 11. Extensibility

New rule categories and fields may be added within V1.x if existing consumers remain compatible.

Breaking rule schema changes require a major knowledge version.
