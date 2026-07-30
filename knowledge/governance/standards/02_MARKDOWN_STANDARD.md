# BTE Markdown Standard
## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-KC-002 |
| Document Name | Markdown Standard |
| Version | V1.0.0 |
| Status | Official |
| Author | BTE Platform |
| Category | Governance |
| Applies To | All files under `knowledge/` |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This document defines the official Markdown writing standard for the BTE Knowledge Canon.

Its objectives are:

- Standardize every knowledge document.
- Ensure consistency across all modules.
- Enable automatic parsing.
- Support AI processing.
- Support Rule Database generation.
- Support future documentation generation.

Every Markdown file inside the Knowledge Canon SHALL comply with this specification.

---

# 2. Scope

This standard applies to:

- knowledge/bazi/
- knowledge/numerology/
- knowledge/meihua/

It is also recommended for:

- terminology/
- phrase_library/
- sentence_library/

This specification does NOT apply to:

- Source code
- Unit tests
- Runtime configuration

---

# 3. General Principles

Every Markdown document SHALL satisfy the following principles.

## 3.1 Single Responsibility

Each document shall cover only one clearly defined topic.

Example:

✔ 01_yin_yang.md

✘ yin_yang_and_wuxing.md

---

## 3.2 Single Source of Truth

A concept must only be fully defined once.

Other documents shall reference it instead of duplicating content.

---

## 3.3 Consistency

Documents of the same type shall have identical structure.

---

## 3.4 Traceability

Every section shall be traceable to:

- Knowledge ID
- Rule Database
- Sentence Library
- Case Studies

---

# 4. Metadata Standard

Every document SHALL begin with metadata.

Example

```yaml
---
document_id: BTE-KC-002
knowledge_id:
title:
version:
status:
author:
created_date:
updated_date:
reviewers:
dependencies:
related_rules:
related_sentences:
tags:
---
```

Rules

Metadata must appear before the first heading.

Metadata uses YAML.

Empty values are allowed during drafting.

---

# 5. Heading Standard

Only four heading levels are allowed.

```markdown
# Chapter

## Section

### Subsection

#### Notes
```

Never use:

```markdown
##### Heading

###### Heading
```

---

# 6. Paragraph Standard

Each paragraph should discuss one idea only.

Recommended:

3–8 lines.

Avoid paragraphs exceeding 15 lines.

---

# 7. List Standard

Supported list types:

Unordered

```markdown
- Item
- Item
```

Ordered

```markdown
1. Item
2. Item
```

Checklist

```markdown
- [ ] Draft
- [x] Reviewed
```

---

# 8. Table Standard

Use GitHub Markdown tables only.

Example

| Item | Description |
|------|-------------|
| Can | Heavenly Stem |
| Chi | Earthly Branch |

Avoid merged cells.

---

# 9. Definition Block

Definitions shall use the following format.

```markdown
> **Definition**

Definition text...
```

---

# 10. Note Block

```markdown
> **Note**

Additional explanation...
```

---

# 11. Warning Block

```markdown
> **Warning**

Important caution...
```

---

# 12. Rule Block

```markdown
> **Rule**

Rule statement...
```

---

# 13. Exception Block

```markdown
> **Exception**

Exception description...
```

---

# 14. Example Standard

Every important concept should include at least one example.

Structure

```markdown
## Example

Background

Analysis

Conclusion
```

---

# 15. Case Study Standard

Structure

```markdown
## Case Study

Scenario

Observation

Analysis

Conclusion

Lessons Learned
```

---

# 16. Diagram Standard

Preferred formats:

- Mermaid
- Markdown Table
- ASCII Diagram

Avoid image-only diagrams unless necessary.

---

# 17. Reference Standard

References shall appear at the end of the document.

Example

```markdown
## References

1.
2.
3.
```

---

# 18. Glossary Standard

Every major document shall include:

```markdown
## Glossary
```

Each glossary entry contains:

Term

Definition

Reference

---

# 19. Revision History

Every document shall end with:

| Version | Date | Changes |
|----------|------|----------|

---

# 20. Document Checklist

Before freezing a document verify:

- [ ] Metadata complete
- [ ] Structure compliant
- [ ] Headings compliant
- [ ] Knowledge IDs assigned
- [ ] References added
- [ ] Examples included
- [ ] Case Studies included
- [ ] Rule Mapping completed
- [ ] Reviewed
- [ ] Approved

---

# 21. Compliance

Any Markdown document that violates this specification SHALL NOT be considered part of the official BTE Knowledge Canon.

Documents may remain in Draft status until all requirements have been satisfied.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |