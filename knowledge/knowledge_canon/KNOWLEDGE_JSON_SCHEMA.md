# Knowledge JSON Schema Specification

> **Document ID:** KC-SCHEMA-001
>
> **Module:** `knowledge/knowledge_canon`
>
> **Version:** V1.0.0
>
> **Status:** Official
>
> **Document Type:** Data Contract Specification
>
> **Language:** English
>
> **Governance:** Governance V1.0

---

# 1. Purpose

This document defines the canonical JSON schema for all Knowledge Assets within the BTE Platform.

The schema serves as the official data contract between knowledge repositories, validation tools, APIs, runtime engines, and reporting modules.

---

# 2. Objectives

The schema shall:

- Standardize data representation.
- Support machine validation.
- Ensure interoperability.
- Preserve backward compatibility.
- Enable automated tooling.
- Support explainable AI.
- Support long-term governance.

---

# 3. Scope

This specification applies to every Knowledge Asset stored within the Knowledge Canon.

It governs:

- JSON structure
- Field definitions
- Data types
- Validation rules
- Compatibility
- Extensions

---

# 4. Design Principles

The schema shall be:

- Canonical
- Deterministic
- Extensible
- Backward Compatible
- Human Readable
- Machine Readable
- Version Controlled

---

# 5. Knowledge Asset Object Model

```
Knowledge Asset

├── identity
├── metadata
├── names
├── definition
├── classification
├── characteristics
├── relationships
├── evidence
├── references
├── terminology_links
├── rule_links
├── sentence_links
├── mappings
├── governance
└── revision_history
```

---

# 6. Root Object

```json
{
  "identity": {},
  "metadata": {},
  "names": {},
  "definition": {},
  "classification": {},
  "characteristics": {},
  "relationships": [],
  "evidence": {},
  "references": [],
  "terminology_links": [],
  "rule_links": [],
  "sentence_links": [],
  "mappings": [],
  "governance": {},
  "revision_history": []
}
```

---

# 7. Identity Object

Required Fields

| Field | Type | Required |
|---------|------|----------|
| knowledge_id | string | Yes |
| domain | string | Yes |
| category | string | Yes |

Example

```json
{
  "knowledge_id": "KNO-000001",
  "domain": "five_elements",
  "category": "element"
}
```

---

# 8. Metadata Object

Required

```json
{
  "version": "1.0.0",
  "status": "official",
  "language": "en",
  "author": "",
  "reviewer": "",
  "created_date": "",
  "updated_date": ""
}
```

Status Enumeration

```
draft

review

approved

official

deprecated

archived
```

---

# 9. Names Object

```json
{
  "canonical": "",
  "english": "",
  "vietnamese": "",
  "traditional_chinese": "",
  "simplified_chinese": "",
  "aliases": []
}
```

Canonical Name is mandatory.

---

# 10. Definition Object

```json
{
  "summary": "",
  "description": "",
  "notes": ""
}
```

Summary is required.

---

# 11. Classification Object

```json
{
  "domain": "",
  "category": "",
  "complexity": "",
  "confidence": ""
}
```

Confidence

```
high

medium

low
```

---

# 12. Characteristics Object

```json
{
  "nature": "",
  "attributes": [],
  "behaviors": [],
  "exceptions": []
}
```

---

# 13. Relationships

```json
[
  {
    "type": "",
    "target": ""
  }
]
```

Supported Types

```
parent

child

related

depends_on

extends

derived_from

equivalent

contradicts
```

---

# 14. Evidence Object

```json
{
  "confidence": "high",
  "review_notes": "",
  "academic_notes": ""
}
```

---

# 15. References

```json
[
  {
    "reference_id": "",
    "chapter": "",
    "section": "",
    "priority": 1
  }
]
```

Minimum one reference required for publication.

---

# 16. Terminology Links

```json
[
    "TERM-000001"
]
```

---

# 17. Rule Links

```json
[
    "RUL-000001"
]
```

---

# 18. Sentence Links

```json
[
    "SEN-000001"
]
```

---

# 19. Mapping Records

```json
[
  {
    "mapping_type": "",
    "target": ""
  }
]
```

---

# 20. Governance Object

```json
{
  "owner": "",
  "approval_status": "",
  "review_cycle": "",
  "next_review": ""
}
```

---

# 21. Revision History

```json
[
  {
    "version": "",
    "date": "",
    "summary": ""
  }
]
```

---

# 22. Required Fields

The following fields shall always be present:

- identity.knowledge_id
- names.canonical
- metadata.version
- metadata.status
- definition.summary
- classification.domain
- references

---

# 23. Data Type Rules

Supported primitive types:

- string
- integer
- number
- boolean
- object
- array
- null (only where explicitly permitted)

---

# 24. Validation Rules

Validators shall verify:

- Required fields
- Identifier format
- Enum values
- Duplicate identifiers
- Relationship integrity
- Mapping integrity
- Reference existence
- Version format
- Traceability completeness

---

# 25. Compatibility Rules

PATCH releases

- No schema changes.

MINOR releases

- Optional fields may be added.

MAJOR releases

- Breaking structural changes permitted.

---

# 26. Extension Rules

Custom extensions shall:

- Use vendor-specific namespaces if applicable.
- Not redefine canonical fields.
- Remain backward compatible.
- Be documented.

Example

```json
{
  "extensions": {
    "vendor_name": {
      "custom_field": "value"
    }
  }
}
```

---

# 27. Example Knowledge Asset

```json
{
  "identity": {
    "knowledge_id": "KNO-000001",
    "domain": "five_elements",
    "category": "element"
  },
  "metadata": {
    "version": "1.0.0",
    "status": "official",
    "language": "en"
  },
  "names": {
    "canonical": "Wood",
    "english": "Wood",
    "vietnamese": "Mộc",
    "traditional_chinese": "木",
    "simplified_chinese": "木",
    "aliases": []
  },
  "definition": {
    "summary": "One of the Five Elements.",
    "description": "Represents growth, expansion, and vitality.",
    "notes": ""
  },
  "classification": {
    "domain": "five_elements",
    "category": "element",
    "complexity": "basic",
    "confidence": "high"
  },
  "characteristics": {
    "nature": "Yang",
    "attributes": ["Growth", "Expansion"],
    "behaviors": [],
    "exceptions": []
  },
  "relationships": [],
  "evidence": {
    "confidence": "high",
    "review_notes": "",
    "academic_notes": ""
  },
  "references": [
    {
      "reference_id": "REF-000001",
      "chapter": "Chapter 1",
      "section": "Section A",
      "priority": 1
    }
  ],
  "terminology_links": [
    "TERM-000001"
  ],
  "rule_links": [
    "RUL-000001"
  ],
  "sentence_links": [
    "SEN-000001"
  ],
  "mappings": [],
  "governance": {
    "owner": "Knowledge Team",
    "approval_status": "approved",
    "review_cycle": "annual",
    "next_review": "2027-01-01"
  },
  "revision_history": [
    {
      "version": "1.0.0",
      "date": "2026-07-30",
      "summary": "Initial release."
    }
  ]
}
```

---

# 28. Compliance

All Knowledge Assets shall conform to this specification.

Any deviation requires Governance approval.

---

# 29. Future Extensions

Future versions may support:

- JSON Schema Draft 2020-12 compatibility
- JSON-LD export
- RDF serialization
- Graph database integration
- Digital signatures
- Multilingual localization packages

---

# 30. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| V1.0.0 | Official | Initial JSON schema specification |