# BTE Glossary Standard

## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-KC-008 |
| Document Name | Glossary Standard |
| Version | V1.0.0 |
| Status | Official |
| Author | BTE Platform |
| Category | Governance Standard |
| Applies To | All Knowledge Assets |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This specification defines the official terminology standard for the BTE Knowledge Canon.

Its objectives are:

- Establish a Single Source of Truth for terminology.
- Eliminate inconsistent naming.
- Improve readability.
- Support Rule Database.
- Support Sentence Library.
- Support AI Retrieval.
- Support multilingual expansion.

Every official term SHALL be registered in the Glossary Registry.

---

# 2. Scope

This specification applies to:

- Bazi
- Numerology
- Meihua
- Rule Database
- Sentence Library
- Phrase Library
- Report Engine
- API Documentation
- User Documentation

---

# 3. Principles

Every glossary entry SHALL satisfy the following principles.

## 3.1 Uniqueness

Each concept shall have one official definition.

---

## 3.2 Consistency

The same term shall always use the same wording.

---

## 3.3 Traceability

Every definition shall reference:

- Knowledge Assets
- References

---

## 3.4 Reusability

One glossary entry may be referenced by multiple assets.

---

## 3.5 Expandability

New languages and aliases may be added without changing the Glossary ID.

---

# 4. Glossary ID

Every glossary entry SHALL own a permanent identifier.

Format

```
GLS-<MODULE>-<NUMBER>
```

Examples

```
GLS-FND-0001

GLS-TGD-0028

GLS-UGD-0015
```

Glossary IDs are immutable.

---

# 5. Standard Metadata

Every glossary entry SHALL contain metadata.

```yaml
asset_id:
term:
language:
module:
version:
status:
author:
created_date:
updated_date:
tags:
references:
related_assets:
related_rules:
```

---

# 6. Standard Entry Structure

Each glossary entry SHALL contain the following sections.

1. Metadata
2. Official Term
3. Chinese Characters
4. Pinyin
5. English Name
6. Vietnamese Name
7. Abbreviations
8. Synonyms
9. Deprecated Names
10. Definition
11. Detailed Explanation
12. Usage Notes
13. Common Misunderstandings
14. Related Terms
15. Related Knowledge Assets
16. Related Rules
17. References
18. Revision History

---

# 7. Official Term

The official term approved by the Knowledge Committee.

Example

```
Dụng Thần
```

Only one official term is permitted.

---

# 8. Chinese Characters

Original Chinese writing.

Example

```
用神
```

Optional if unavailable.

---

# 9. Pinyin

Romanized Chinese.

Example

```
Yòng Shén
```

---

# 10. English Name

Official English translation.

Example

```
Useful God
```

Only one official translation shall be used.

---

# 11. Vietnamese Name

Official Vietnamese wording.

Example

```
Dụng Thần
```

---

# 12. Abbreviations

Accepted abbreviations.

Example

```
DT
```

Optional.

---

# 13. Synonyms

Alternative names that may appear in historical literature.

Example

```
Hỷ Dụng
```

These shall not replace the official term.

---

# 14. Deprecated Names

Outdated or discouraged terminology.

These remain searchable but shall not appear in new documents.

---

# 15. Definition

Provide a concise and authoritative definition.

The definition should fit within one paragraph.

---

# 16. Detailed Explanation

Expand upon the official definition.

Describe:

- Theory
- Context
- Application
- Limitations

---

# 17. Usage Notes

Explain correct usage.

Include:

- Recommended wording
- Context
- Restrictions

---

# 18. Common Misunderstandings

List frequent misconceptions.

Example

```
Many beginners confuse Dụng Thần with Hỷ Thần.
```

Clarify the difference.

---

# 19. Related Terms

Cross-reference other glossary entries.

Example

```
GLS-UGD-0002

GLS-TGD-0010
```

---

# 20. Related Knowledge Assets

Reference relevant Knowledge IDs.

Example

```
KID-BZ-UGD-CH03
```

---

# 21. Related Rules

Reference Rule IDs.

Example

```
RID-UGD-00031
```

---

# 22. References

Reference IDs only.

Example

```
REF-CLASSIC-0004

REF-BOOK-0012
```

---

# 23. Glossary Registry

All glossary entries SHALL be stored in a centralized registry.

Recommended structure

```
knowledge/

glossary/

fundamental/

strength/

temperature/

pattern/

useful_god/

ten_gods/

combination/

shensha/

luck/

general/
```

Every entry shall occupy one file.

---

# 24. Example Entry

```yaml
asset_id: GLS-UGD-0001

term: Dụng Thần

language: vi-VN

version: 1.0.0

status: official
```

Official Term

```
Dụng Thần
```

Chinese

```
用神
```

Pinyin

```
Yòng Shén
```

English

```
Useful God
```

Definition

```
The primary element selected to balance the chart and improve overall harmony.
```

Related Assets

```
KID-BZ-UGD-CH01
```

Related Rules

```
RID-UGD-00001
```

References

```
REF-CLASSIC-0001
```

---

# 25. Validation Rules

Every glossary entry SHALL satisfy:

- Unique Glossary ID
- Official Definition
- Related References
- Related Knowledge Assets
- Version Information
- Status Information

---

# 26. Compliance Checklist

Before approval verify:

- [ ] Glossary ID assigned
- [ ] Metadata complete
- [ ] Official definition approved
- [ ] Chinese characters verified
- [ ] English translation verified
- [ ] Related Assets linked
- [ ] Related Rules linked
- [ ] References verified

---

# 27. Compliance

Any terminology not registered in the official Glossary Registry SHALL NOT be considered an official BTE term.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |