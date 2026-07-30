# Knowledge Asset Template

> **Document ID:** KC-TEMPLATE-001
>
> **Module:** `knowledge/knowledge_canon`
>
> **Version:** V1.0.0
>
> **Status:** Official
>
> **Document Type:** Root Template
>
> **Language:** English
>
> **Governance:** Governance V1.0

---

# 1. Purpose

This document defines the canonical template for all Knowledge Assets within the BTE Knowledge Canon.

Every Knowledge Asset shall conform to this template unless an approved extension is defined.

---

# 2. Usage

This template applies to all domains:

- Five Elements
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Yin Yang
- Ten Gods
- Strength
- Patterns
- Useful Gods
- Combinations
- Clashes
- Punishments
- Harms
- Transformations
- Seasonal Qi
- Temperature
- Shen Sha
- Luck Cycles
- Special Cases

---

# 3. Knowledge Asset Structure

```
Knowledge Asset
├── Identity
├── Metadata
├── Definition
├── Classification
├── Characteristics
├── Relationships
├── Evidence
├── References
├── Mapping
├── Governance
└── Revision History
```

---

# 4. Identity

| Field | Required | Description |
|--------|----------|-------------|
| Knowledge ID | Yes | Unique immutable identifier |
| Canonical Name | Yes | Official name |
| Domain | Yes | Knowledge domain |
| Category | Yes | Logical category |

---

# 5. Metadata

| Field | Required |
|--------|----------|
| Version | Yes |
| Status | Yes |
| Language | Yes |
| Author | Yes |
| Reviewer | Yes |
| Created Date | Yes |
| Updated Date | Yes |

Optional

- Tags
- Keywords
- Notes

---

# 6. Names

## Canonical Name

Official name.

## Chinese

Traditional Chinese

Simplified Chinese

## Vietnamese

Official Vietnamese name.

## English

Official English name.

## Aliases

Alternative names.

Historical names.

School-specific names.

---

# 7. Definition

## Short Definition

One paragraph.

## Detailed Description

Comprehensive explanation.

## Academic Notes

Optional.

---

# 8. Classification

Examples

- Element
- Heavenly Stem
- Ten God
- Pattern
- Rule Concept

Additional classifications may be defined by domain.

---

# 9. Characteristics

Describe:

- Nature
- Attributes
- Behavior
- Typical Features
- Exceptions

---

# 10. Relationships

Supported relationships:

- Parent
- Child
- Related
- Equivalent
- Derived From
- Depends On
- Extends
- Contradicts

Each relationship shall include the referenced Knowledge ID.

---

# 11. Dependencies

Knowledge Assets may depend on:

- Terminology
- Other Knowledge Assets
- References

Dependencies shall be explicitly declared.

---

# 12. Evidence

Evidence may include:

- Classical quotations
- Academic commentary
- Historical notes
- Reviewer observations

---

# 13. References

Reference IDs

Reference Sections

Reference Chapters

Reference Passages

Priority

Evidence Weight

---

# 14. Terminology Links

Reference standardized terminology.

Example

TERM-000123

---

# 15. Rule Links

Reference supporting rules.

Example

RUL-000245

---

# 16. Sentence Links

Reference interpretation sentences.

Example

SEN-000876

---

# 17. Mapping

Knowledge Assets may map to

- Rules
- Sentences
- Reports
- Dataset Cases

---

# 18. Confidence

Levels

- High
- Medium
- Low

Confidence Factors

- Reference Count
- Consensus
- Review Status

---

# 19. Governance

Review Status

Approval Status

Owner

Last Review

Next Review

---

# 20. Traceability

```
Reference
      ↓
Terminology
      ↓
Knowledge Asset
      ↓
Rule
      ↓
Sentence
      ↓
Interpretation
      ↓
Report
```

---

# 21. Validation Checklist

Before publication verify:

- ID assigned
- Canonical Name defined
- Metadata complete
- References linked
- Relationships validated
- Traceability complete
- Version assigned
- Reviewer approved

---

# 22. Example Skeleton

```
Knowledge ID

Canonical Name

Domain

Category

Metadata

Definition

Characteristics

Relationships

Evidence

References

Terminology

Rules

Sentences

Confidence

Governance

Revision History
```

---

# 23. Extension Rules

Additional fields may be introduced only if:

- Backward compatible
- Approved by Governance
- Documented in CHANGELOG

Core fields shall never be removed.

---

# 24. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| V1.0.0 | Official | Initial template |