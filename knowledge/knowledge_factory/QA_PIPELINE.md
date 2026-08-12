# QA Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | QA_PIPELINE |
| Version | 1.0.0 |
| Section | 7 — QA |

---

# 7.1 Rule

**Do NOT redefine QA.**

All criteria, scoring, verdicts, lifecycle, and checklists come from:

```text
knowledge/knowledge_qa/STANDARD/
```

The Factory defines **when QA runs** and **what happens after**. The QA Standard defines **how to score**.

---

# 7.2 QA in the factory pipeline

```text
Catalog topic complete (QG2)
  ↓
Author self-check (QA_CHECKLIST § Author)
  ↓
Topic phase QA (QA_TEMPLATE)
  ↓
PASS / REVIEW / FAIL per unit
  ↓
Phase review archived
  ↓
QG3 pass (zero FAIL)
  ↓
Domain Reviewer Review stage
```

---

# 7.3 Topic phase order

Recommended (Strength-style packs):

```text
MEANING → CAUSES → ADVANTAGES → CHALLENGES → PERSONALITY
  → CAREER → WEALTH → MARRIAGE → HEALTH → LUCK
  → RECOMMENDATION → EDGE_CASES → EXAMPLES
```

MEANING before ADVANTAGES when advantages restate identity.

---

# 7.4 QA task boundaries

### QA-only task

| Allowed | Forbidden |
|---------|-----------|
| Score 12 criteria | Rewrite claims |
| Assign verdict | Change catalog status |
| Document gaps | Edit duplicate clusters |
| Archive phase review | Modify QA Standard |

### Authoring fix task (separate)

| Allowed |
|---------|
| Edit claim, limitations, metadata |
| Re-submit for re-QA |

---

# 7.5 Key QA Standard references

| Topic | Document |
|-------|----------|
| Criteria | QA_CRITERIA.md |
| Scoring | QA_SCORING.md |
| Verdicts | PASS_REVIEW_FAIL.md |
| Workflow | QA_WORKFLOW.md |
| Review roles | REVIEW_PROCESS.md |
| Checklist | QA_CHECKLIST.md |
| Template | QA_TEMPLATE.md |
| Examples | QA_EXAMPLES.md |

---

# 7.6 Outputs

Per topic phase:

```text
knowledge/knowledge_qa/PACK_XX_<DOMAIN>/PHASE_NN_<TOPIC>_REVIEW.md
```

Required content: per QA_TEMPLATE.

---

# 7.7 QG3 pass conditions

| Condition | Required |
|-----------|----------|
| All units in scope scored | Yes |
| FAIL count | 0 (or Chief Reviewer waiver) |
| Phase review archived | Yes |
| Rationale for every REVIEW | Yes |

REVIEW units may proceed to Review stage but not to Validated until resolved or waived.

---

# 7.8 Cursor as QA Assistant

Cursor follows QA_TEMPLATE and QA Standard.

Cursor is **not final authority**. Domain Reviewer accepts QA before Review gate.

---

# 7.9 PACK-01 QA progress

| Phase | Units | PASS | REVIEW | FAIL |
|-------|------:|-----:|-------:|-----:|
| 01 MEANING | 18 | 8 | 10 | 0 |
| 02 CAUSES | 25 | 10 | 15 | 0 |
| 03 ADVANTAGES | 35 | 16 | 19 | 0 |

Remaining topics: not yet QA’d.

---

END
