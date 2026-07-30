# Knowledge Domain Model

**Module:** `knowledge/knowledge_architecture`  
**Version:** V1.0.0  
**Status:** Frozen (Domain Model Specification)

---

# 1. Purpose

This document defines the shared domain models of the Knowledge Layer.

These models provide stable contracts for Knowledge Modules, Knowledge Gateways, and Engine consumers.

---

# 2. Design Principles

Knowledge domain models shall be:

- Immutable after publication
- Strongly typed
- Versioned
- Serializable
- Storage-agnostic
- Explainable
- Backward compatible within V1.x

---

# 3. Core Domain Objects

```text
KnowledgeModuleDescriptor
KnowledgeAsset
RuleDefinition
SentenceDefinition
ReportTemplateDefinition
KnowledgeManifest
KnowledgeVersion
KnowledgeReference
KnowledgeEvidence
```

---

# 4. KnowledgeModuleDescriptor

Represents one Knowledge Module.

Contains:

- module_id
- domain
- display_name
- status
- version
- capability set
- asset family support
- dependency declarations

Status values include:

- Planned
- Draft
- Validated
- Published
- Deprecated

---

# 5. KnowledgeAsset

Base contract for all knowledge assets.

Contains:

- asset_id
- asset_family
- module_id
- version
- status
- checksum
- metadata

Asset families:

- Rule
- Sentence
- ReportTemplate
- Taxonomy
- Example
- Manifest

---

# 6. RuleDefinition

Represents one analytical rule.

Contains:

- rule_id
- category
- priority
- conditions
- effects
- weight references
- effective dating
- evidence schema

Rules are consumed by Analysis Engine stages.

---

# 7. SentenceDefinition

Represents one interpretive language asset.

Contains:

- sentence_id
- domain tags
- intent
- template body
- variable bindings
- tone / style metadata
- localization key

Sentences are consumed by Interpretation Engine.

---

# 8. ReportTemplateDefinition

Represents one presentation template.

Contains:

- template_id
- report type
- section layout
- binding map
- style profile
- localization key

Templates are consumed by Report Engine.

---

# 9. KnowledgeManifest

Published inventory of a Knowledge Module package.

Contains:

- module descriptor
- asset index
- dependency graph
- compatibility matrix
- validation status

---

# 10. KnowledgeVersion

Represents a versioned knowledge snapshot.

Contains:

- semantic version
- release channel
- compatibility range
- publication timestamp
- supersedes reference

---

# 11. KnowledgeReference

Stable reference used by engines and results.

Contains:

- module_id
- asset_id
- asset_version
- category

KnowledgeReference appears in matched-rule and explainability payloads.

---

# 12. KnowledgeEvidence

Traceability object linking engine decisions to knowledge assets.

Contains:

- KnowledgeReference
- match context
- contribution summary
- diagnostic notes

---

# 13. Ownership Rules

| Model | Owner |
|-------|-------|
| KnowledgeModuleDescriptor | Knowledge Layer |
| RuleDefinition | Owning Knowledge Module |
| SentenceDefinition | Interpretation Knowledge |
| ReportTemplateDefinition | Report Knowledge |
| KnowledgeManifest | Knowledge Module publisher |
| KnowledgeReference | Shared Knowledge contract |

Engine Modules may read these models.

Engine Modules must not mutate them.

---

# 14. Compatibility

Domain models remain backward compatible within Version 1.x.

Breaking model changes require a major version.
