# BTE Reference Standard

## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-KC-006 |
| Document Name | Reference Standard |
| Version | V1.0.0 |
| Status | Official |
| Author | BTE Platform |
| Category | Governance Standard |
| Applies To | All Knowledge Assets |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This specification defines the official reference management standard for the BTE Knowledge Canon.

The objectives are:

- Ensure every knowledge statement is traceable.
- Distinguish original knowledge from cited knowledge.
- Standardize citation format.
- Prevent duplicated references.
- Support Knowledge Graph.
- Support AI Retrieval.
- Support future academic publication.

Every Knowledge Asset SHALL comply with this specification.

---

# 2. Scope

This standard applies to:

- Knowledge Chapters
- Sections
- Rules
- Case Studies
- Examples
- Glossary
- Sentence Library
- Phrase Library
- Report Templates

---

# 3. Design Principles

The reference system follows six principles.

## 3.1 Traceability

Every external knowledge source shall be traceable.

---

## 3.2 Verifiability

Readers shall be able to verify every cited source.

---

## 3.3 Consistency

The same reference shall have exactly one official record.

---

## 3.4 Reusability

One reference may be reused by multiple Knowledge Assets.

---

## 3.5 Non-Duplication

Duplicate reference records are prohibited.

---

## 3.6 Stability

Reference IDs shall never change once published.

---

# 4. Reference Categories

BTE defines the following categories.

| Category | Code |
|-----------|------|
| Classical Book | CLASSIC |
| Modern Book | BOOK |
| Academic Paper | PAPER |
| Journal | JOURNAL |
| Internal Document | INTERNAL |
| Government Document | GOV |
| Website | WEB |
| Video | VIDEO |
| Lecture | LECTURE |
| Case Archive | CASE |
| Interview | INTERVIEW |

---

# 5. Reference ID

Every reference SHALL own a permanent Reference ID.

Format

```
REF-<CATEGORY>-<NUMBER>
```

Examples

```
REF-CLASSIC-0001

REF-BOOK-0025

REF-PAPER-0012

REF-WEB-0041
```

Reference IDs are immutable.

---

# 6. Reference Metadata

Every reference SHALL contain metadata.

```yaml
reference_id:
category:
title:
original_title:
author:
translator:
publisher:
publication_year:
edition:
language:
country:
isbn:
url:
accessed_date:
license:
remarks:
```

---

# 7. Mandatory Fields

The following fields are required.

- reference_id
- category
- title
- author
- publication_year

Other fields are optional.

---

# 8. Citation Rules

Knowledge Assets shall reference Reference IDs rather than repeating bibliographic information.

Example

```yaml
references:

- REF-CLASSIC-0003
- REF-BOOK-0018
```

---

# 9. Reference Registry

All references SHALL be stored in a centralized registry.

Recommended structure

```
knowledge/

governance/

reference_registry/

classic/

books/

papers/

web/

internal/
```

Only one official record shall exist for each source.

---

# 10. Internal References

Internal references point to BTE Knowledge Assets.

Example

```
KID-BZ-FND-CH03

KID-BZ-STR-CH07
```

Internal references SHALL use Knowledge IDs.

---

# 11. External References

External references include:

Books

Research Papers

Classical Texts

Government Documents

Official Websites

These SHALL use Reference IDs.

---

# 12. Reference Priority

When multiple references exist, priority SHALL be:

Classical Text

↓

Official Standard

↓

Academic Paper

↓

Published Book

↓

Internal Knowledge

↓

Website

↓

Video

↓

Personal Notes

---

# 13. Source Reliability Levels

| Level | Description |
|------|-------------|
| A | Classical or Official Source |
| B | Academic Publication |
| C | Published Book |
| D | Professional Website |
| E | Community Content |
| F | Unverified Source |

Knowledge should primarily rely on Level A–C sources.

---

# 14. Conflicting References

When references conflict:

- Record all viewpoints.
- Identify the source of each viewpoint.
- Do not merge conflicting conclusions.
- Explain differences objectively.

---

# 15. Deprecated References

A deprecated reference:

- Keeps its Reference ID.
- Remains searchable.
- Shall not be deleted.
- May be replaced by a newer edition.

---

# 16. Versioning

References are version independent.

The Reference ID remains unchanged.

Metadata may be updated.

---

# 17. AI Compatibility

Reference metadata shall support:

- Semantic Search
- Citation Generation
- Knowledge Graph
- AI Retrieval
- Rule Extraction

---

# 18. Example

```yaml
reference_id: REF-CLASSIC-0001

category: CLASSIC

title: 渊海子平

original_title: 渊海子平

author: Xu Ziping

language: zh-CN

publication_year: Unknown

remarks: Classical Bazi Text
```

---

# 19. Validation Rules

Every reference shall satisfy:

- Unique Reference ID
- Valid Category
- Valid Metadata
- No Duplicate Record
- Traceable Source

---

# 20. Compliance Checklist

Before approval verify:

- [ ] Reference ID assigned
- [ ] Category valid
- [ ] Metadata complete
- [ ] Duplicate check completed
- [ ] Source verified
- [ ] Registry updated

---

# 21. Compliance

Any reference that does not comply with this specification SHALL NOT become part of the official BTE Knowledge Canon.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |