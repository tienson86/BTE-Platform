# BTE Reference Extraction Guide

---

# Document Information

| Field | Value |
|--------|-------|
| Document ID | BTE-REF-GUIDE-001 |
| Document Name | Reference Extraction Guide |
| Version | V1.0.0 |
| Status | Official |
| Category | Knowledge Engineering |
| Last Updated | YYYY-MM-DD |

---

# 1. Purpose

This document defines the official methodology for transforming authoritative references into structured knowledge assets within the BTE Knowledge Platform.

The extraction process ensures that knowledge derived from classical texts remains:

- Accurate
- Traceable
- Consistent
- Version Controlled
- Machine Readable
- AI Ready

---

# 2. Scope

This guide applies to every reference source:

- Classical Books
- Modern Books
- Academic Papers
- Internal Research
- Historical Manuscripts

---

# 3. Extraction Principles

## Single Source of Truth

Every extracted knowledge item SHALL originate from a documented reference.

---

## Traceability

Every extracted statement SHALL be traceable back to:

Reference

↓

Chapter

↓

Section

↓

Paragraph

↓

Original Text

---

## Atomic Knowledge

Each extracted knowledge item SHALL represent only one concept.

Example:

❌

Fire generates Earth and Earth controls Water.

✔

Rule A

Fire generates Earth.

✔

Rule B

Earth controls Water.

---

## No Interpretation During Extraction

Extraction captures the author's knowledge.

Interpretation belongs to the Interpretation Engine.

---

## Version Integrity

Extraction SHALL always reference a specific edition.

---

# 4. Extraction Workflow

```
Reference Selection

↓

Metadata Registration

↓

Structural Analysis

↓

Terminology Extraction

↓

Concept Extraction

↓

Knowledge Extraction

↓

Rule Candidate Extraction

↓

Evidence Registration

↓

Cross Mapping

↓

Validation

↓

Governance Review

↓

Registry

```

---

# 5. Phase 1 — Reference Registration

Objectives

Register the source.

Outputs

- Reference ID
- Metadata
- Edition
- Language
- Reliability
- Registry Entry

---

# 6. Phase 2 — Structural Analysis

Identify:

Book

↓

Volume

↓

Chapter

↓

Section

↓

Paragraph

↓

Sentence

Every unit receives a structural identifier.

Example

BOOK-01

VOL-01

CH-03

SEC-02

PAR-015

---

# 7. Phase 3 — Terminology Extraction

Extract every technical term.

Each term includes:

Chinese

Vietnamese

English

Definition

Aliases

Synonyms

Usage

References

Output:

Terminology Registry Candidate

---

# 8. Phase 4 — Concept Extraction

Extract conceptual knowledge.

Each concept includes:

Concept ID

Definition

Relationships

Dependencies

Importance

Output

Knowledge Canon Candidate

---

# 9. Phase 5 — Rule Candidate Extraction

Convert concepts into executable rules.

Every rule includes:

Condition

Action

Priority

Exceptions

Evidence

Confidence

Output

Rule Database Candidate

---

# 10. Phase 6 — Sentence Candidate Extraction

Identify reusable interpretation statements.

Each sentence includes:

Template

Variables

Conditions

Applicable Rules

Output

Sentence Library Candidate

---

# 11. Phase 7 — Evidence Registration

Every extracted item SHALL register evidence.

Evidence includes:

Reference

↓

Edition

↓

Volume

↓

Chapter

↓

Section

↓

Paragraph

↓

Original Text

↓

Translation

---

# 12. Phase 8 — Knowledge Mapping

Map every extracted item.

Reference

↓

Knowledge Canon

↓

Rule Database

↓

Sentence Library

↓

Interpretation

↓

Report

---

# 13. Knowledge Extraction Matrix

Every reference SHALL produce the following matrix.

## Domain Coverage

| Domain | Coverage | Confidence |
|----------|----------|------------|

---

## Concept Inventory

List all extracted concepts.

---

## Rule Inventory

Potential Rule IDs.

---

## Terminology Inventory

Extracted terms.

---

## Citation Inventory

Complete citation mapping.

---

## Cross Reference Inventory

Related references.

---

# 14. Quality Validation

Validation Checklist

✓ Metadata complete

✓ Structural identifiers complete

✓ Terminology verified

✓ Concepts unique

✓ Rules atomic

✓ Evidence attached

✓ Traceability complete

✓ Mapping completed

---

# 15. Governance Review

Review levels

Technical Review

↓

Knowledge Review

↓

Editorial Review

↓

Governance Review

↓

Approval

---

# 16. Deliverables

Each completed extraction SHALL generate:

Reference Document

Knowledge Extraction Matrix

Terminology Candidates

Knowledge Canon Candidates

Rule Candidates

Sentence Candidates

Evidence Registry

Traceability Links

Review Report

---

# 17. Common Extraction Errors

Typical mistakes:

Multiple concepts in one rule

Missing evidence

Missing terminology

Incorrect translation

Interpretation mixed into extraction

Broken traceability

Duplicate concepts

---

# 18. Best Practices

Always extract literally first.

Interpret later.

Never merge independent concepts.

Prefer smaller knowledge units.

Always keep original terminology.

Register every citation.

Validate every dependency.

---

# 19. Related Documents

REFERENCE_TEMPLATE.md

REFERENCE_SPEC.md

Terminology Standard

Traceability Standard

Rule Template

Knowledge Template

Governance Procedures

---

# 20. Revision History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | YYYY-MM-DD | Initial release |