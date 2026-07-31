# JSON MAPPING TEMPLATE

**BTE Knowledge Canon Standard**

---

| Item | Value |
|------|-------|
| Template Version | 1.0.0 |
| Status | Official |
| Applies To | All Knowledge Records |
| Based On | KNOWLEDGE_RECORD_TEMPLATE.md |

---

# Purpose

This document defines the canonical mapping between Markdown Knowledge Records and the JSON Knowledge Canon.

The mapping SHALL be deterministic, reversible, and machine-readable.

Every Markdown Knowledge Record SHALL be convertible into a valid JSON representation without semantic loss.

---

# Mapping Principles

The compiler SHALL:

- preserve semantic meaning
- preserve hierarchical structure
- preserve relationships
- preserve metadata
- validate required fields
- reject invalid mappings

The compiler SHALL NOT:

- invent new knowledge
- modify canonical definitions
- change relationship semantics
- remove mandatory fields

---

# Canonical Mapping

| Markdown Section | JSON Property | Type | Required |
|------------------|--------------|------|----------|
| Knowledge ID | knowledge_id | string | Yes |
| Canonical Name | canonical_name | string | Yes |
| Chinese Name | chinese_name | object | No |
| English Name | english_name | string | No |
| Vietnamese Name | vietnamese_name | string | No |
| Aliases | aliases | array | No |
| Record Type | record_type | string | Yes |
| Version | version | string | Yes |
| Status | status | string | Yes |

---

# Classification Mapping

| Markdown | JSON |
|----------|------|
| Domain | classification.domain |
| Module | classification.module |
| Pack | classification.pack |
| Category | classification.category |
| Subcategory | classification.subcategory |
| Knowledge Type | classification.knowledge_type |
| Knowledge Level | classification.knowledge_level |

---

# Academic Source Mapping

| Markdown | JSON |
|----------|------|
| Primary Sources | academic_sources.primary |
| Secondary Sources | academic_sources.secondary |
| Modern References | academic_sources.modern |
| Citation Notes | academic_sources.notes |
| Source Confidence | academic_sources.confidence |

---

# Definition Mapping

| Markdown | JSON |
|----------|------|
| Definition | definition |
| Historical Notes | historical_notes |
| Terminology Notes | terminology_notes |
| Academic Variants | academic_variants |

---

# Relationship Mapping

| Markdown | JSON |
|----------|------|
| Parent | relationships.parent |
| Children | relationships.children |
| Depends On | relationships.depends_on |
| Derived From | relationships.derived_from |
| Related To | relationships.related_to |
| Equivalent To | relationships.equivalent_to |
| Contradicts | relationships.contradicts |

---

# Metadata Mapping

| Markdown | JSON |
|----------|------|
| Author | metadata.author |
| Reviewer | metadata.reviewer |
| Version | metadata.version |
| Created Date | metadata.created_date |
| Updated Date | metadata.updated_date |
| Status | metadata.status |

---

# Computational Semantics Mapping

| Markdown | JSON |
|----------|------|
| Knowledge Nature | computational.nature |
| Computational Properties | computational.properties |
| Engine Compatibility | computational.engine_compatibility |
| Explainability | computational.explainability |

---

# Validation Rules

## Required Fields

- knowledge_id
- canonical_name
- definition
- classification
- metadata

---

## Data Types

| Type | JSON |
|------|------|
| Text | string |
| Number | number |
| Flag | boolean |
| List | array |
| Object | object |

---

## Empty Value Policy

Required fields SHALL NOT be empty.

Optional fields MAY be null.

Arrays SHALL be empty arrays instead of null.

Objects SHALL exist even if partially populated.

---

# Compiler Pipeline

Markdown

↓

Markdown Parser

↓

AST

↓

Knowledge Model

↓

Schema Validation

↓

Relationship Validation

↓

JSON Generation

↓

Knowledge Graph

---

# Error Handling

Possible Compiler Errors

- Missing Required Field
- Invalid Data Type
- Duplicate Knowledge ID
- Invalid Relationship
- Invalid Enumeration
- Schema Validation Failed

---

# Version Compatibility

| Template Version | JSON Schema |
|------------------|-------------|
| 1.0.x | schema_v1 |
| 1.1.x | schema_v1_1 |
| 2.x | schema_v2 |

---

# End of Document