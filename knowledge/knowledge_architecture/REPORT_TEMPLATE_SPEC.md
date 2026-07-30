# Report Template Specification

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Report Template Architecture)

---

# 1. Purpose

This document defines the architecture of Report Templates within the Knowledge Layer.

Report Templates store presentation and layout assets consumed by the Report Engine.

---

# 2. Scope

A Report Template package contains:

- template definitions
- section layouts
- binding maps
- style profiles
- localization keys
- manifests

It does not contain:

- analytical decision rules
- interpretation sentence content ownership
- engine orchestration logic
- mutable runtime state

---

# 3. Ownership

Primary owner:

- Report Knowledge

Report Templates may reference AnalysisResult and Interpretation outputs through declared bindings.

---

# 4. Template Architecture

```text
Report Template Package
   │
   ├── Template Definitions
   ├── Section Tree
   ├── Binding Map
   ├── Style Profile
   ├── Localization Pack
   └── Manifest
```

---

# 5. Template Definition Requirements

Every template shall define:

- template_id
- version
- report type
- section hierarchy
- required bindings
- optional bindings
- style profile
- localization key
- status

---

# 6. Binding Model

Templates bind to published contracts such as:

- AnalysisResult
- stage results
- Interpretation outputs
- shared metadata

Templates shall not bind to:

- unpublished engine internals
- physical knowledge paths
- transient calculation buffers

---

# 7. Section Model

Sections are hierarchical and may include:

- identity / header
- chart summary
- analytical sections
- interpretation sections
- luck sections
- appendix / diagnostics

Section presence may be conditional through knowledge-defined visibility rules.

---

# 8. Consumption Contract

Report Engine consumes Report Templates only through:

```text
Abstract Report Knowledge Module
```

No hard-coded repository path is permitted in engine contracts.

---

# 9. Validation Requirements

Before publication, Report Templates shall validate:

- unique template IDs
- resolvable bindings
- section integrity
- style profile completeness
- localization completeness for declared locales

---

# 10. Traceability

Generated reports shall retain KnowledgeReferences to the template assets used.

---

# 11. Extensibility

New report types, sections, and style profiles may be added within V1.x without changing abstract engine contracts.
