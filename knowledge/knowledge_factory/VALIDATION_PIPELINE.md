# Validation Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | VALIDATION_PIPELINE |
| Version | 1.0.0 |
| Section | 8 — Validation |

---

# 8.1 Purpose

Prove **Reviewed** catalog units align with **Reasoning golden cases** before Freeze.

Validation is **alignment and gate verification** — not full Reasoning Engine implementation in Factory V1.0.

---

# 8.2 Prerequisites

| Prerequisite | Gate |
|--------------|------|
| Units **Reviewed** | QG4 |
| Reasoning FREEZE exists | `knowledge/reasoning_engine/PACK_XX_*/FREEZE/` |
| Golden cases defined | CASE_0001, … |
| QA PASS on golden-pinned units | Or resolved REVIEW |

---

# 8.3 Validation workflow

```text
Reviewed units (topic complete or pack complete)
  ↓
Load golden reference (Reasoning FREEZE)
  ↓
For each pinned knowledge_id:
  verify required_facts align with golden facts
  verify duplicate_cluster matches golden reject/accept
  verify customer_mode matches golden Customer narrative
  verify no REVIEW/FAIL open on pinned unit
  ↓
Document validation record
  ↓
Domain Reviewer + Reasoning governance sign-off
  ↓
Promote units → Validated
  ↓
QG5 pass
```

---

# 8.4 Golden Case validation rules

| Check | Pass condition |
|-------|----------------|
| Pinned unit exists | knowledge_id in catalog |
| Status | Reviewed minimum; Validated after gate |
| Evidence | Golden facts satisfy required_facts |
| Duplicate policy | Golden reject list honored |
| Narrative budget | Golden facet count compatible with catalog |
| Cross-pack | Golden Strength-only; no unpublished pack leak |
| Consistency | No golden REVIEW conflict |

---

# 8.5 PACK-01 golden reference

Location (read-only for Factory):

```text
knowledge/reasoning_engine/PACK_01_STRENGTH/FREEZE/
```

Example pinned units (CASE-0001):

| knowledge_id | Role |
|--------------|------|
| MEAN-0006 | Full-tank representative |
| CAUS-0002, 0007, 0010, 0016 | Cause chain |
| ADV-0009, 0013 | Advantage representatives |

Validation must confirm these units can reach **Validated** without open blocking REVIEW on golden-critical paths.

---

# 8.6 Validation vs QA

| Aspect | QA | Validation |
|--------|-----|------------|
| Question | Is unit professionally suitable? | Does unit work in golden narrative? |
| Input | Source + criteria | Golden + Reasoning policy |
| Owner | QA Assistant | Domain Reviewer + Reasoning gov |
| Output | PASS/REVIEW/FAIL | Validated status |

QA may PASS a unit that fails golden alignment — Validation catches it.

---

# 8.7 Validation record

Per pack, archive:

```text
knowledge/knowledge_qa/PACK_XX_<DOMAIN>/VALIDATION_RECORD.md
```

(or governance location — Factory V1.0 recommends under knowledge_qa pack folder)

Contents:

- Golden cases validated
- Pinned unit list
- Conflicts found and resolved
- Sign-off names and dates

---

# 8.8 Exit criteria (QG5)

| Condition | Required |
|-----------|----------|
| All golden-pinned units Validated | Yes |
| No golden conflict open | Yes |
| Evidence gates documented | Align with Reasoning FREEZE |
| Validation record archived | Yes |
| Domain Reviewer sign-off | Yes |

---

END
