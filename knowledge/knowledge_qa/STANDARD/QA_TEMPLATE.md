# QA Template — V1.0

| Field | Value |
|-------|-------|
| Document | QA_TEMPLATE |
| Standard | Knowledge QA V1.0 |
| Use | All pack phase reviews |

---

# Phase Review Template

Copy to:

```text
knowledge/knowledge_qa/PACK_XX_<DOMAIN>/PHASE_NN_<TOPIC>_REVIEW.md
```

---

```markdown
# Phase NN — <TOPIC> QA Review

| Field | Value |
|-------|-------|
| Document | PHASE_NN_<TOPIC>_REVIEW |
| Pack | PACK_XX_<DOMAIN> |
| Standard | Knowledge QA V1.0 |
| Scope | <TOPIC> units only |
| Date | YYYY-MM-DD |
| QA Assistant | <name or Cursor> |
| Status | QA input — not final approval |

---

# 1. Scope

| Field | Value |
|-------|-------|
| Unit count | N |
| Id range | IK-XX-<TOPIC>-0001 … NNNN |
| Review order | knowledge_id ascending |
| Catalog path | knowledge/knowledge_catalog/PACK_XX_<DOMAIN>/catalog/<topic>/ |
| Source path | knowledge/interpretation_knowledge/PACK_XX_<DOMAIN>/ |

**QA-only task:** No catalog edits. No status changes. No claim rewrites.

---

# 2. Verdict definitions

| Verdict | Meaning |
|---------|---------|
| **PASS** | No blocking defect; eligible for Domain Reviewer → Reviewed |
| **REVIEW** | Defect documented; remains Draft until resolved |
| **FAIL** | Blocking defect; authoring fix required |

QA PASS ≠ Validated. QA PASS ≠ Frozen. Cursor is not final authority.

Criteria: [QA_CRITERIA.md](../STANDARD/QA_CRITERIA.md)
Scoring: [QA_SCORING.md](../STANDARD/QA_SCORING.md)

---

# 3. Criteria columns (per unit table)

| Column | Criterion |
|--------|-----------|
| PC | Professional Correctness |
| EC | Evidence Compatibility |
| DP | Domain Purity |
| DR | Duplicate Risk |
| CV | Customer Value |
| AC | Actionability |
| RD | Readability |
| EX | Explainability |
| CQ | Commercial Quality |
| CP | Cross-Pack Dependency |
| CN | Consistency |
| TR | Traceability |
| Avg | Unit average |
| Verdict | PASS / REVIEW / FAIL |

Scores: 0, 3, 5, 7, 9, 10 only.

---

# 4. Pack-level notes

<!-- Duplicate clusters, golden references, schema gaps, topic-wide patterns -->

---

# 5. Unit reviews

## IK-XX-<TOPIC>-NNNN — <short title>

| PC | EC | DP | DR | CV | AC | RD | EX | CQ | CP | CN | TR | Avg | Verdict |
|----|----|----|----|----|----|----|----|----|----|----|-----|-----|---------|
| | | | | | | | | | | | | | |

**Source:** `<filename>.md`

**Overall: PASS / REVIEW / FAIL**

<!-- PASS: one paragraph why -->
<!-- REVIEW: -->
What is missing:
- …

Not FAIL: …

<!-- FAIL: -->
Blocking defect:
- …

Criterion: …

---

# 6. FAIL units

| knowledge_id | Blocking criterion | Summary |
|--------------|-------------------|---------|
| | | |

---

# 7. Summary statistics

| Metric | Value |
|--------|-------|
| Units reviewed | |
| PASS | |
| REVIEW | |
| FAIL | |
| Average score (all units) | |

### Criterion averages (topic)

| PC | EC | DP | DR | CV | AC | RD | EX | CQ | CP | CN | TR |
|----|----|----|----|----|----|----|----|----|----|----|-----|

---

# 8. PASS units

`IK-XX-<TOPIC>-…`

---

# 9. REVIEW units

`IK-XX-<TOPIC>-…`

### Cross-cutting REVIEW themes

1. …

---

# 10. Recommendations (non-blocking)

| # | Recommendation | Owner |
|---|----------------|-------|
| 1 | | Governance / Author / Reasoning |

---

# 11. Domain Reviewer sign-off

| Field | Value |
|-------|-------|
| Reviewer | |
| Decision | Accept QA / Partial accept / Re-QA required |
| Date | |
| Notes | |

---

END
```

---

END
