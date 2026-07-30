# BTE Metadata Specification

## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-KC-005 |
| Document Name | Metadata Specification |
| Version | V1.0.0 |
| Status | Official |
| Author | BTE Platform |
| Category | Governance |
| Applies To | All Knowledge Assets |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This specification defines the official metadata schema for every Knowledge Asset within the BTE Knowledge Canon.

Metadata provides:

- Identification
- Classification
- Versioning
- Dependency Management
- Traceability
- AI Retrieval
- Knowledge Registry
- Rule Generation

Every Knowledge Asset SHALL contain metadata.

---

# 2. Scope

This specification applies to:

- Knowledge Chapters
- Sections
- Rule Database
- Sentence Library
- Phrase Library
- Case Studies
- Glossary
- References
- Tables
- Diagrams
- Templates

---

# 3. Design Principles

Metadata shall satisfy the following principles.

## Completeness

Metadata shall completely describe an asset.

---

## Consistency

The same field shall have the same meaning everywhere.

---

## Machine Readability

Metadata shall be parseable.

---

## Human Readability

Metadata shall remain understandable.

---

## Extensibility

New fields may be added without breaking compatibility.

---

# 4. Metadata Levels

BTE defines four metadata levels.

Level 1

Repository Metadata

↓

Level 2

Module Metadata

↓

Level 3

Document Metadata

↓

Level 4

Section Metadata

---

# 5. Standard Metadata Schema

Every Knowledge Asset shall contain the following metadata.

```yaml
---
asset_id:
asset_type:
domain:
module:
title:
subtitle:
version:
status:

author:
reviewers:
approvers:

created_date:
updated_date:
published_date:

language:
locale:

tags:
keywords:

difficulty:
knowledge_level:

dependencies:
related_assets:

related_rules:
related_sentences:
related_cases:

references:

license:

visibility:

checksum:

remarks:
---
```

---

# 6. Field Definitions

## asset_id

Unique identifier.

Example

```
KID-BZ-FND-CH03
```

Required

YES

---

## asset_type

Allowed values

```
chapter

section

rule

sentence

phrase

case

reference

glossary

diagram

table

template
```

---

## domain

Example

```
bazi

numerology

meihua
```

---

## module

Example

```
fundamental

strength

temperature

pattern
```

---

## title

Human-readable title.

---

## subtitle

Optional.

---

## version

Semantic Versioning.

```
1.0.0
```

---

## status

Allowed values

```
draft

review

approved

official

deprecated

archived
```

---

## author

Document owner.

---

## reviewers

Knowledge reviewers.

---

## approvers

Final approvers.

---

## created_date

ISO 8601.

---

## updated_date

ISO 8601.

---

## published_date

Optional.

---

## language

Example

```
vi

en
```

---

## locale

Example

```
vi-VN
```

---

## tags

Keyword list.

---

## keywords

Search keywords.

---

## difficulty

Allowed values

```
basic

intermediate

advanced

expert
```

---

## knowledge_level

Example

```
L1

L2

L3

L4

L5
```

---

## dependencies

Knowledge dependencies.

Example

```
KID-BZ-FND-CH01

KID-BZ-FND-CH02
```

---

## related_assets

Cross references.

---

## related_rules

Referenced Rule IDs.

---

## related_sentences

Referenced Sentence IDs.

---

## related_cases

Referenced Case IDs.

---

## references

Referenced books.

Documents.

Papers.

---

## license

Default

```
BTE Internal
```

---

## visibility

Allowed values

```
private

internal

public
```

---

## checksum

Optional.

Reserved for future integrity verification.

---

## remarks

Additional notes.

Optional.

---

# 7. Metadata by Asset Type

## Chapter

Required

```
asset_id

title

version

status

module

author

dependencies
```

---

## Rule

Required

```
asset_id

related_assets

priority

rule_type
```

---

## Sentence

Required

```
asset_id

related_rules

tone

language
```

---

## Case Study

Required

```
asset_id

related_assets

difficulty
```

---

# 8. Metadata Validation

Every metadata object shall satisfy:

✓ asset_id exists

✓ version exists

✓ status exists

✓ title exists

✓ author exists

✓ created_date exists

---

# 9. Metadata Lifecycle

Draft

↓

Review

↓

Approved

↓

Official

↓

Deprecated

↓

Archived

Metadata shall always be updated.

---

# 10. AI Compatibility

Metadata shall support:

Knowledge Registry

↓

Knowledge Loader

↓

Semantic Search

↓

Embedding

↓

Knowledge Graph

↓

AI Retrieval

↓

Rule Extraction

---

# 11. Future Compatibility

Reserved fields may be introduced.

Older metadata shall remain valid.

Backward compatibility is mandatory.

---

# 12. Example

```yaml
---
asset_id: KID-BZ-FND-CH03

asset_type: chapter

domain: bazi

module: fundamental

title: Heavenly Stems

version: 1.0.0

status: official

author: BTE Platform

created_date: 2026-07-30

updated_date: 2026-07-30

language: vi

locale: vi-VN

difficulty: intermediate

knowledge_level: L2

dependencies:
  - KID-BZ-FND-CH01
  - KID-BZ-FND-CH02

related_rules:
  - RID-STR-00021

tags:
  - heavenly_stems
  - ten_heavenly_stems
---
```

---

# 13. Compliance Checklist

Before approval verify:

- [ ] Asset ID assigned
- [ ] Metadata complete
- [ ] Version valid
- [ ] Status valid
- [ ] Dependencies reviewed
- [ ] Related Rules reviewed
- [ ] References completed

---

# 14. Compliance

Any Knowledge Asset without valid metadata SHALL NOT become part of the official BTE Knowledge Canon.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |