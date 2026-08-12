# Explainability Standard — V1.0

| Field | Value |
|-------|-------|
| Document | EXPLAINABILITY_STANDARD |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Every unit must **earn its place** in the customer narrative.

Explainability answers: **So what?**

---

# 2. Frozen rules

| Rule | Requirement |
|------|-------------|
| Removal test | If removed, does customer lose important insight **in this narrative context**? |
| So what | Claim must change understanding, decision, or self-view |
| Budget context | OPTIONAL/DETAIL units may score LOW EXPLAINABILITY without FAIL |
| Duplicate | If removal changes nothing because duplicate exists → LOW EXPLAINABILITY |
| Governance | Teaching-only units may be FORBIDDEN in Customer Mode — explainability N/A there |

---

# 3. Evaluation

```text
1. Identify narrative context (headline vs detail, class, co-selected units)
2. Simulate print with unit
3. Simulate print without unit
4. If loss is material → explainability satisfied
5. If loss is none → REVIEW or omit under budget
```

---

# 4. Scoring

| Score | Meaning |
|-------|---------|
| 10 | Headline-essential |
| 7 | Valuable support |
| 5 | Optional / LOW EXPLAINABILITY |
| 3 | Redundant with sibling unit |
| 0 | Pure duplicate |

---

# 5. Typical failures

| Example | Issue |
|---------|-------|
| MEAN-0007 supporting point | States blind spot — does not support claim |
| Class cluster CAUS-0020–0024 | Taxonomy when atomics present |
| ADV optional adaptability | When headline facets already selected |
| MEAN shell + class MEAN | Shell redundant if class MEAN kept |

PACK-01 references: [QA_EXAMPLES.md](QA_EXAMPLES.md).

---

END
