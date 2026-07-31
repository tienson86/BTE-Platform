# KNOWLEDGE RECORD TEMPLATE

**BTE Knowledge Canon Standard**

---

| Item | Value |
|------|-------|
| Template Version | 1.0.0 |
| Status | Official |
| Applies To | All Knowledge Records |
| Based On | PART_03_KNOWLEDGE_RECORD_STANDARD.md |

---

# Authoring Instructions

This template defines the canonical structure for every Knowledge Record within the BTE Knowledge Canon.

Authors SHALL complete every mandatory section.

Optional sections MAY be omitted only when explicitly permitted by the Knowledge Record Standard.

Do NOT modify the overall structure of this template.

---

# 1. Identity

## Knowledge ID

```
KR-XXXXXXXX
```

## Canonical Name

```
...
```

## Chinese Name (Simplified)

```
...
```

## Chinese Name (Traditional)

```
...
```

## Pinyin

```
...
```

## English Name

```
...
```

## Vietnamese Name

```
...
```

## Aliases

- ...

## Record Type

```
Concept / Entity / Relationship / Principle / Rule Input / Reference
```

## Version

```
1.0.0
```

## Status

```
Draft
```

---

# 2. Classification

## Domain

```
...
```

## Module

```
...
```

## Pack

```
...
```

## Category

```
...
```

## Subcategory

```
...
```

## Knowledge Type

```
...
```

## Knowledge Level

```
Foundation / Intermediate / Advanced
```

## Academic School

```
...
```

## Owner Module

```
...
```

## Consumer Modules

- ...

---

# 3. Academic Sources

## Primary Sources

- ...

## Secondary Sources

- ...

## Modern References

- ...

## Citation Notes

...

## Source Confidence

```
High / Medium / Low
```

---

# 4. Scope

## Included

- ...

## Excluded

- ...

## Boundary Conditions

...

## Assumptions

...

## Limitations

...

---

# 5. Canonical Definition

## Definition

...

## Historical Notes

...

## Terminology Notes

...

## Academic Variants

...

---

# 6. Characteristics

## Fundamental Properties

- ...

## Behaviors

- ...

## Attributes

- ...

## Conditions

- ...

## Exceptions

- ...

## Special Cases

- ...

---

# 7. Relationships

## Parent

- ...

## Children

- ...

## Depends On

- ...

## Derived From

- ...

## Related To

- ...

## Equivalent To

- ...

## Contradicts

- ...

## Supersedes

- ...

## Referenced By

- ...

---

# 8. Constraints

## Academic Constraints

- ...

## Logical Constraints

- ...

## Computational Constraints

- ...

## Validation Constraints

- ...

## Usage Constraints

- ...

---

# 9. Examples

## Positive Examples

...

## Negative Examples

...

## Boundary Cases

...

## Typical Cases

...

## Exceptional Cases

...

---

# 10. References

## Canonical References

- ...

## Academic Citations

- ...

## Cross References

- ...

## External References

- ...

---

# 11. Metadata

## Author

...

## Reviewer

...

## Approver

...

## Created Date

YYYY-MM-DD

## Last Updated

YYYY-MM-DD

## Version

1.0.0

## Status

Draft

## Language

English

## Compiler Version

...

## Schema Version

...

---

# 12. Computational Semantics

## Knowledge Nature

```
Foundational / Descriptive / Derived / Rule Input / Rule Output / Interpretation / Reference
```

## Computational Properties

| Property | Value |
|----------|-------|
| Can Match | Yes / No |
| Can Score | Yes / No |
| Can Infer | Yes / No |
| Can Explain | Yes / No |
| Can Render | Yes / No |
| Can Generate Rule | Yes / No |
| Can Participate in Knowledge Graph | Yes / No |
| Can Be Cached | Yes / No |

---

## Engine Compatibility

| Engine | Supported |
|---------|-----------|
| Compiler | Yes / No |
| Rule Engine | Yes / No |
| Priority Engine | Yes / No |
| Analysis Engine | Yes / No |
| Interpretation Engine | Yes / No |
| Report Engine | Yes / No |
| AI Rewrite Engine | Yes / No |

---

## Explainability Contract

### Explanation Source

...

### Supporting Rules

- ...

### Supporting Knowledge Records

- ...

### Supporting Evidence

- ...

### Confidence

High / Medium / Low

### Reasoning Path

...

---

# 13. Validation

## Identity Validation

☐ Pass

## Structure Validation

☐ Pass

## Academic Validation

☐ Pass

## Relationship Validation

☐ Pass

## Reference Validation

☐ Pass

## Schema Validation

☐ Pass

## Compiler Validation

☐ Pass

## Integrity Validation

☐ Pass

---

# 14. Review History

| Version | Date | Author | Summary |
|----------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | ... | Initial Draft |

---

# 15. Approval

## Academic Review

☐ Approved

Reviewer:

Date:

---

## Technical Review

☐ Approved

Reviewer:

Date:

---

## Publication Decision

☐ Draft

☐ Approved

☐ Published

☐ Frozen

☐ Deprecated

☐ Archived

---
---

# 16. Revision Log

This section records the detailed evolution of the Knowledge Record.

Every semantic modification SHALL be documented.

Editorial corrections MAY be grouped into a single entry.

## Revision History

| Version | Date | Author | Change Type | Description | Approved By |
|----------|------|--------|-------------|-------------|-------------|
| 1.0.0 | YYYY-MM-DD | ... | Initial | Initial publication | ... |

---

## Change Types

Allowed values:

- Initial
- Academic Update
- Technical Update
- Editorial Correction
- Schema Migration
- Relationship Update
- Reference Update
- Deprecation
- Restoration

---

## Versioning Rules

Major Version

Used when:

- Canonical definition changes
- Academic meaning changes
- Relationship model changes
- Breaking compatibility

Example

1.0.0

↓

2.0.0

---

Minor Version

Used when:

- New references added
- New examples added
- Additional explanations
- Metadata enhancement

Example

1.0.0

↓

1.1.0

---

Patch Version

Used when:

- Typographical corrections
- Formatting improvements
- Citation formatting
- Non-semantic fixes

Example

1.1.0

↓

1.1.1

---

## Migration Notes

If a revision introduces breaking changes, migration guidance SHALL be provided.

Example

Previous Record

↓

Migration Rule

↓

Current Record

---

# 17. Compiler Hints

This section provides optional implementation guidance for the Knowledge Compiler.

Compiler Hints SHALL NOT modify academic meaning.

Compiler Hints SHALL NOT introduce executable logic.

Compiler Hints are intended solely for compiler optimization and automation.

---

## JSON Export

Export Record

Yes / No

Export Metadata

Yes / No

Export Examples

Yes / No

Export References

Yes / No

---

## Knowledge Graph

Create Node

Yes / No

Create Edges

Yes / No

Relationship Types

- parent_of
- child_of
- depends_on
- related_to

---

## Search Index

Index Canonical Name

Yes / No

Index Aliases

Yes / No

Index Definition

Yes / No

Index Examples

Yes / No

Index References

Yes / No

---

## Compiler Validation

Special Validation Required

Yes / No

Validation Rules

- ...

---

## Internal Processing

Normalization Required

Yes / No

Generate Keywords

Yes / No

Generate Embeddings

Yes / No

Generate Cross References

Yes / No

---

## AI Processing

Available For AI Retrieval

Yes / No

Available For RAG

Yes / No

Available For Explanation

Yes / No

Available For Prompt Context

Yes / No

---

## Performance Hints

Cache Recommended

Yes / No

Priority Loading

High / Medium / Low

Lazy Loading Allowed

Yes / No

---

## Notes

Additional compiler guidance.

# 18. Quality Metrics

Academic Completeness

95%

Reference Coverage

100%

Relationship Completeness

90%

Terminology Consistency

100%

Compiler Readiness

100%

Validation Score

100%

Review Score

98%

Overall Quality

A
...
# End of Knowledge Record