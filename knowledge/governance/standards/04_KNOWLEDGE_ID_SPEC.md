# BTE Knowledge Asset Identity Specification
## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-KC-004 |
| Document Name | Knowledge Asset Identity Specification |
| Version | V1.0.0 |
| Status | Official |
| Author | BTE Platform |
| Category | Governance |
| Applies To | All Knowledge Assets |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This specification defines the official identity system for every Knowledge Asset within the BTE Knowledge Canon.

Its objectives are:

- Guarantee uniqueness.
- Support traceability.
- Support Rule Engine.
- Support AI Retrieval.
- Support Knowledge Graph.
- Support version management.

Every Knowledge Asset SHALL own one permanent identifier.

---

# 2. Principles

The identity system follows five principles.

## 2.1 Uniqueness

Each asset has one unique ID.

Duplicate IDs are prohibited.

---

## 2.2 Permanence

An ID never changes.

Even if the document changes version.

---

## 2.3 Traceability

Every ID shall be traceable.

Knowledge

↓

Rule

↓

Sentence

↓

Report

↓

Engine Output

---

## 2.4 Human Readability

IDs should remain understandable by humans.

---

## 2.5 Machine Readability

IDs must be parseable.

No spaces.

No Unicode.

Uppercase only.

---

# 3. Knowledge Asset Types

The following assets require official IDs.

| Asset | Prefix |
|--------|---------|
| Knowledge Chapter | KID |
| Section | SID |
| Paragraph | PID |
| Rule | RID |
| Sentence | SEN |
| Phrase | PHR |
| Case Study | CAS |
| Glossary | GLS |
| Reference | REF |
| Diagram | DIA |
| Table | TAB |
| Template | TMP |

---

# 4. Domain Codes

| Domain | Code |
|---------|------|
| Bazi | BZ |
| Numerology | NUM |
| Meihua | MH |

---

# 5. Module Codes

| Module | Code |
|---------|------|
| Fundamental | FND |
| Strength | STR |
| Temperature | TMP |
| Pattern | PAT |
| Useful God | UGD |
| Ten Gods | TGD |
| Combination | COM |
| ShenSha | SHS |
| Luck | LUK |
| Marriage | MAR |
| Career | CAR |
| Wealth | WEA |
| Health | HLT |
| Children | CHD |
| Case Studies | CST |

---

# 6. Chapter Number

Every chapter uses:

CH01

CH02

CH03

...

---

# 7. Section Number

Sections use:

S01

S02

S03

...

---

# 8. Paragraph Number

Paragraphs use:

P01

P02

P03

...

---

# 9. Knowledge ID Format

Official format

```
KID-BZ-FND-CH03
```

Meaning

```
Knowledge

↓

Bazi

↓

Fundamental

↓

Chapter 03
```

---

# 10. Section ID

Example

```
SID-BZ-FND-CH03-S02
```

Meaning

```
Section 02

Chapter 03
```

---

# 11. Paragraph ID

Example

```
PID-BZ-FND-CH03-S02-P04
```

Meaning

Paragraph 04

Section 02

Chapter 03

---

# 12. Rule ID

Example

```
RID-STR-00125
```

Rule IDs are maintained independently from Knowledge IDs.

Knowledge references Rules.

Rules reference Knowledge.

---

# 13. Sentence ID

Example

```
SEN-00412
```

Sentence IDs remain independent.

---

# 14. Phrase ID

Example

```
PHR-00182
```

---

# 15. Case Study ID

Example

```
CAS-BZ-00031
```

---

# 16. Glossary ID

Example

```
GLS-TGD-008
```

---

# 17. Reference ID

Example

```
REF-BOOK-001

REF-PAPER-021

REF-CLASSIC-008
```

---

# 18. Diagram ID

Example

```
DIA-FND-001
```

---

# 19. Table ID

Example

```
TAB-FND-001
```

---

# 20. Template ID

Example

```
TMP-STRENGTH-001
```

---

# 21. Traceability

Every Rule SHALL reference Knowledge.

Example

```json
{
    "rule_id":"RID-STR-00125",
    "knowledge_ref":[
        "PID-BZ-STR-CH07-S03-P02"
    ]
}
```

---

Every Sentence SHALL reference Knowledge.

```json
{
    "sentence_id":"SEN-00412",
    "knowledge_ref":[
        "SID-BZ-STR-CH07-S03"
    ]
}
```

---

Every Report SHALL reference Sentences.

```
Report

↓

Sentence

↓

Rule

↓

Knowledge
```

---

# 22. Reserved IDs

Once an ID has been published:

It SHALL NEVER be reused.

Even if the asset is deleted.

---

# 23. Deprecated Assets

Deprecated assets remain traceable.

Status

```
Deprecated
```

Version continues.

ID never changes.

---

# 24. Version Independence

Identity

≠

Version

Example

```
KID-BZ-FND-CH03

Version

1.0.0

↓

1.1.0

↓

2.0.0
```

The ID remains identical.

---

# 25. Naming Rules

Uppercase only.

No spaces.

No accents.

Hyphen separated.

Maximum readability.

---

# 26. Validation Rules

Every ID SHALL satisfy:

✓ Unique

✓ Permanent

✓ Parseable

✓ Traceable

✓ Immutable

---

# 27. Identity Lifecycle

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

Identity remains unchanged.

---

# 28. Compliance

Any Knowledge Asset without a valid official ID SHALL NOT become part of the BTE Knowledge Canon.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |