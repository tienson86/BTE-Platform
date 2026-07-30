# BTE Case Study Standard

## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-KC-007 |
| Document Name | Case Study Standard |
| Version | V1.0.0 |
| Status | Official |
| Author | BTE Platform |
| Category | Governance Standard |
| Applies To | All Case Studies |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This specification defines the official standard for creating, reviewing, maintaining and referencing Case Studies within the BTE Knowledge Canon.

Case Studies are one of the most important knowledge assets because they connect theoretical knowledge with practical analysis.

The objectives are:

- Standardize every case study.
- Improve knowledge quality.
- Build a reusable Golden Dataset.
- Support AI Retrieval.
- Support Rule Validation.
- Support future model evaluation.

Every Case Study SHALL comply with this specification.

---

# 2. Scope

This specification applies to:

- Bazi
- Numerology
- Meihua

and any future knowledge domain added to the BTE Platform.

---

# 3. Principles

Every Case Study SHALL satisfy the following principles.

## 3.1 Authenticity

A case shall be based on a real or realistically constructed scenario.

---

## 3.2 Traceability

Every conclusion shall be traceable to:

- Knowledge Assets
- Rules
- References

---

## 3.3 Educational Value

A Case Study must explain why a conclusion is reached.

It is not sufficient to only present the final result.

---

## 3.4 Reproducibility

Another analyst following the same rules should reach substantially the same conclusion.

---

## 3.5 Reusability

Case Studies shall be reusable for:

- Learning
- Testing
- Rule Validation
- AI Evaluation

---

# 4. Case Study Classification

| Type | Description |
|------|-------------|
| Basic | Simple educational example |
| Standard | Typical real-world case |
| Advanced | Complex analysis |
| Edge Case | Rare or exceptional scenario |
| Golden Case | Official validation case |

---

# 5. Case Study ID

Every Case Study SHALL own a permanent ID.

Format

```
CAS-<DOMAIN>-<NUMBER>
```

Examples

```
CAS-BZ-00001

CAS-BZ-00002

CAS-NUM-00001

CAS-MH-00001
```

IDs are unique and immutable.

---

# 6. Standard Metadata

```yaml
asset_id:
title:
version:
status:
difficulty:
author:
reviewers:
created_date:
updated_date:
tags:
related_assets:
related_rules:
references:
```

---

# 7. Standard Structure

Every Case Study SHALL contain the following sections.

1. Metadata
2. Background
3. Input Data
4. Analysis Process
5. Rule Mapping
6. Findings
7. Final Conclusion
8. Alternative Interpretations
9. Lessons Learned
10. References
11. Revision History

---

# 8. Background

Describe the context of the case.

Include only information relevant to the analysis.

---

# 9. Input Data

Present all source data required for reproduction.

Example:

- Birth information
- Four Pillars
- Hidden Stems
- Luck Cycles
- Additional assumptions

No derived conclusions should appear in this section.

---

# 10. Analysis Process

Explain the reasoning step by step.

Each step should reference applicable Knowledge Assets and Rules.

---

# 11. Rule Mapping

Every analytical conclusion SHALL identify the Rules used.

Example

```yaml
related_rules:
  - RID-STR-00015
  - RID-PAT-00008
```

---

# 12. Knowledge Mapping

Reference the Knowledge Assets that support the analysis.

Example

```yaml
related_assets:
  - KID-BZ-STR-CH04
  - KID-BZ-PAT-CH02
```

---

# 13. Findings

Summarize the key observations obtained during analysis.

Do not include recommendations in this section.

---

# 14. Final Conclusion

Present the final interpretation based on the documented reasoning.

The conclusion must be supported by previous sections.

---

# 15. Alternative Interpretations

When multiple valid schools of thought exist:

- Describe each interpretation.
- Identify the supporting references.
- Explain why differences occur.

---

# 16. Lessons Learned

Summarize the most important knowledge gained from the case.

These lessons should be reusable in future analyses.

---

# 17. Golden Case Requirements

A Golden Case SHALL satisfy all of the following:

- Complete input data.
- Fully documented reasoning.
- Rule Mapping completed.
- Knowledge Mapping completed.
- References verified.
- Peer reviewed.
- Approved by the Knowledge Committee.

Only Golden Cases may be used as official validation datasets.

---

# 18. Validation Checklist

Before approval verify:

- [ ] Metadata completed
- [ ] Input Data complete
- [ ] Analysis reproducible
- [ ] Rule Mapping completed
- [ ] Knowledge Mapping completed
- [ ] References verified
- [ ] Conclusion supported
- [ ] Lessons Learned documented
- [ ] Review completed

---

# 19. Compliance

Any Case Study that does not comply with this specification SHALL NOT become part of the official BTE Knowledge Canon.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |