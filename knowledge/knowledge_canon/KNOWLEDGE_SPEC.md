# Knowledge Canon Specification

> **Document ID:** KC-SPEC-001
>
> **Module:** `knowledge/knowledge_canon`
>
> **Version:** V1.0.0
>
> **Status:** Official
>
> **Document Type:** Root Specification
>
> **Language:** English
>
> **Governance:** Governance V1.0

---

# 1. Purpose

This specification defines the architecture, structure, governance, lifecycle, and interoperability of the BTE Knowledge Canon.

The Knowledge Canon is the authoritative repository of normalized knowledge used throughout the BTE Platform.

This document is the primary specification governing every Knowledge Asset.

---

# 2. Objectives

The Knowledge Canon shall:

- Standardize all domain knowledge.
- Normalize concepts extracted from references.
- Eliminate duplicated knowledge.
- Support explainable interpretation.
- Support traceability.
- Support version control.
- Provide a stable foundation for all engines.

---

# 3. Scope

This specification applies to:

- Knowledge Assets
- Knowledge Domains
- Metadata
- Relationships
- Evidence
- References
- Rule Mapping
- Sentence Mapping
- Governance
- Traceability

This specification does not define:

- Rule implementation
- Sentence implementation
- Report templates
- Runtime engine behavior

---

# 4. Position within BTE Architecture

```
Reference Library
        │
        ▼
Terminology
        │
        ▼
Knowledge Canon
        │
 ┌──────┼──────────────┐
 ▼      ▼              ▼
Rules  Sentences    Score Models
        │
        ▼
Interpretation Engine
        │
        ▼
Report Engine
```

The Knowledge Canon is the central semantic layer of the platform.

---

# 5. Core Principles

## Single Source of Truth

Every concept shall exist only once.

---

## Atomic Knowledge

Each Knowledge Asset represents one and only one concept.

---

## Evidence Driven

Every Knowledge Asset shall reference at least one approved source.

---

## Explainability

Every interpretation shall be traceable.

---

## Version Controlled

Knowledge is immutable.

Updates create new versions.

---

## Machine Readable

Knowledge Assets must be usable by software without manual interpretation.

---

# 6. Knowledge Lifecycle

```
Reference

↓

Extraction

↓

Normalization

↓

Review

↓

Publication

↓

Consumption

↓

Revision

↓

Archive
```

---

# 7. Knowledge Asset

A Knowledge Asset is the smallest reusable unit of normalized knowledge.

Examples:

- Wood
- Jia Wood
- Direct Wealth
- Seven Killings
- Seasonal Qi
- Combination
- Clash

A Knowledge Asset is not a document.

It is a structured knowledge object.

---

# 8. Knowledge Domains

Current domains include:

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

# 9. Knowledge Object Model

Every Knowledge Asset shall contain the following logical sections.

```
Knowledge Asset

├── Identity
├── Metadata
├── Definition
├── Classification
├── Relationships
├── Evidence
├── References
├── Terminology Links
├── Rule Links
├── Sentence Links
├── Traceability
└── Governance
```

---

# 10. Identity Model

Mandatory:

- Knowledge ID
- Canonical Name
- Domain
- Category

Identifiers shall be globally unique.

---

# 11. Metadata Model

Mandatory metadata:

- Version
- Status
- Language
- Author
- Reviewer
- Created Date
- Updated Date

Optional:

- Notes
- Tags
- Keywords

---

# 12. Canonical Naming

Each concept shall have one canonical name.

Aliases shall not replace the canonical name.

Names shall remain stable across versions.

---

# 13. Identifier Specification

Format

```
KNO-000001
```

Identifiers are immutable.

Deleted identifiers shall never be reused.

---

# 14. Classification

Knowledge may be classified by:

- Domain
- Category
- Complexity
- Confidence
- Source Priority

---

# 15. Relationship Model

Supported relationships:

- Parent
- Child
- Related
- Equivalent
- Derived From
- Depends On
- Contradicts
- Extends

Relationships shall be directional where applicable.

---

# 16. Evidence Model

Every Knowledge Asset shall include evidence.

Evidence consists of:

- References
- Citations
- Source Passages
- Reviewer Notes

Evidence quality shall be recorded.

---

# 17. Reference Integration

Every Knowledge Asset shall reference one or more approved sources.

Current approved references include:

- Yuan Hai Zi Ping
- Di Tian Sui
- San Ming Tong Hui
- Qiong Tong Bao Jian
- Zi Ping Zhen Quan

---

# 18. Terminology Integration

Knowledge Assets shall reference standardized terminology.

Terminology remains independent.

Knowledge Assets consume terminology.

---

# 19. Rule Integration

Knowledge Assets do not contain executable rules.

Rules reference Knowledge Assets.

One Knowledge Asset may support multiple Rules.

---

# 20. Sentence Integration

Knowledge Assets do not contain interpretation sentences.

Sentences reference Knowledge Assets.

---

# 21. Confidence Model

Confidence Levels

- High
- Medium
- Low

Confidence shall consider:

- Number of References
- Academic Consensus
- Review Status

---

# 22. Traceability

Every Knowledge Asset shall support complete bidirectional traceability.

```
Reference

↓

Chapter

↓

Paragraph

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

# 23. Validation

Every Knowledge Asset shall pass validation before publication.

Validation includes:

- Metadata completeness
- Reference integrity
- Identifier uniqueness
- Relationship consistency
- Traceability completeness

---

# 24. Governance

Knowledge Assets are governed by:

- Governance V1.0
- Review Guide
- Quality Standard
- Mapping Standard
- Traceability Specification

---

# 25. Versioning

Semantic Versioning shall be used.

- MAJOR
- MINOR
- PATCH

Knowledge Assets are immutable by version.

---

# 26. Directory Structure

```
knowledge_canon/

README.md

KNOWLEDGE_SPEC.md

KNOWLEDGE_TEMPLATE.md

KNOWLEDGE_MAPPING_STANDARD.md

KNOWLEDGE_TRACEABILITY_SPEC.md

KNOWLEDGE_REVIEW_GUIDE.md

KNOWLEDGE_QUALITY_STANDARD.md

CHANGELOG.md

EDGE_CASES.md

01_five_elements/
02_heavenly_stems/
...
registry/
```

---

# 27. Future Extensions

The Knowledge Canon is designed to support future domains including:

- Feng Shui
- Qi Men Dun Jia
- Liu Yao
- Zi Wei Dou Shu
- I Ching
- Knowledge Graph
- AI-assisted Retrieval

without breaking compatibility.

---

# 28. Compliance

Every module consuming Knowledge Assets shall comply with this specification.

No module may redefine the Knowledge Object Model.

---

# 29. Revision History

| Version | Status | Description |
|----------|--------|-------------|
| V1.0.0 | Official | Initial specification |