# Fundamental Knowledge Field Guide

> **Guide ID:** BAZI-FUNDAMENTAL-FIELDGUIDE-001
>
> **Module:** `knowledge/bazi/01_fundamental_knowledge`
>
> **Version:** V1.0.0
>
> **Status:** Draft
>
> **Document Type:** Knowledge Authoring Guide
>
> **Language:** English

---

# 1. Purpose

This guide defines the standards for creating, editing, validating, and maintaining Knowledge Records within the Fundamental Knowledge module.

Its objective is to ensure that all records are academically consistent, technically valid, and reusable across the BTE Platform.

---

# 2. Authoring Principles

Every Knowledge Record shall follow these principles:

- Academic Accuracy
- Canonical Terminology
- Single Source of Truth
- Traceability
- Consistency
- Machine Readability
- Human Readability
- Extensibility
- Reusability

Authors shall never sacrifice academic correctness for convenience.

---

# 3. Writing Style

Knowledge Records shall be written using:

- objective language
- factual statements
- concise definitions
- consistent terminology
- neutral tone

Avoid:

- personal opinions
- interpretation
- prediction
- fortune telling
- scoring
- implementation logic

---

# 4. Knowledge Record Workflow

Every record follows the lifecycle:

Draft

↓

Technical Validation

↓

Academic Review

↓

Official

↓

Maintenance

↓

Deprecated (if applicable)

---

# 5. Required Record Sections

Each Knowledge Record shall contain the following sections:

## Identity

Purpose:

Provide immutable identification.

Required fields:

- knowledge_id
- canonical_name
- chinese
- pinyin
- english_name

Rules:

- IDs are immutable.
- Canonical names shall be unique.
- Do not rename existing IDs.

---

## Classification

Purpose:

Describe the academic position of the record.

Required fields:

- domain
- category
- type
- status

Rules:

Use predefined classifications only.

---

## Definition

Purpose:

Provide the canonical academic definition.

Rules:

- one concept per record
- concise
- academically precise
- no interpretation
- no examples unless necessary

---

## Characteristics

Purpose:

Describe intrinsic properties.

May include:

- nature
- attributes
- symbolism
- functions
- classifications

Do not include:

- interpretation
- prediction
- scoring

---

## Relationships

Purpose:

Connect records together.

Allowed relationship types:

- parent_of
- child_of
- related_to
- depends_on
- controls
- generates

Rules:

Relationships shall reference Knowledge IDs only.

Never reference filenames.

---

## References

Purpose:

Provide academic traceability.

Rules:

Use Reference IDs only.

Example:

REF-000001

REF-000005

Never cite external URLs directly.

If verification is pending:

TODO_REVIEW

---

## Metadata

Purpose:

Track record history.

Typical fields:

- version
- created_at
- updated_at
- reviewer
- review_date
- status

---

# 6. Naming Rules

Canonical names shall:

- use singular nouns
- use Title Case
- avoid abbreviations
- remain stable across versions

Example:

Good

Five Elements

Hidden Stems

Bad

Elements

WuXingData

FiveElementInfo

---

# 7. Terminology Rules

Always use canonical terminology from:

knowledge/terminology/

Do not invent new terminology.

If a new term is required:

Mark:

TODO_REVIEW

until approved.

---

# 8. Relationship Rules

Relationships shall satisfy:

- bidirectional consistency (where applicable)
- valid Knowledge IDs
- no circular dependency unless academically justified
- no duplicate relationships

---

# 9. Reference Rules

Each academic statement shall have at least one reference.

Preferred sources:

Primary Classical Texts

↓

Recognized Classical Commentaries

↓

Official Academic Notes

Never cite blogs, forums, or unofficial summaries.

---

# 10. Validation Checklist

Before submission verify:

✓ Schema validation

✓ Required fields

✓ Naming convention

✓ Terminology consistency

✓ Relationship integrity

✓ Reference integrity

✓ Duplicate detection

✓ Metadata completeness

---

# 11. Common Mistakes

Avoid:

Duplicating existing concepts.

Mixing definition with interpretation.

Using unofficial terminology.

Leaving missing references.

Creating circular relationships.

Using free-text instead of IDs.

Adding runtime logic.

Embedding Rule Engine behaviour.

---

# 12. Examples

Good Definition

"Wood represents the element associated with growth, expansion, flexibility, and upward movement within the Five Elements system."

Bad Definition

"Wood means the person will become rich."

Reason:

This is interpretation, not knowledge.

---

# 13. Review Criteria

Academic Review checks:

- correctness
- completeness
- references
- terminology
- consistency

Technical Review checks:

- schema
- validation
- IDs
- metadata
- relationships

Governance Review checks:

- lifecycle
- version
- approval
- changelog

---

# 14. Change Management

Changes to Official Knowledge Records require:

1. Academic proposal
2. Review
3. Technical validation
4. Version update
5. Changelog update
6. Approval

Direct modification of Official records is prohibited.

---

# 15. Future Compatibility

Future revisions shall preserve:

- Knowledge IDs
- canonical terminology
- reference integrity
- relationship integrity
- backward compatibility

Deprecated records shall remain traceable and shall not be deleted from the Knowledge Canon.