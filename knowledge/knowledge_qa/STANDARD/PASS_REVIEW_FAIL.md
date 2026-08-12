# PASS / REVIEW / FAIL — V1.0

| Field | Value |
|-------|-------|
| Document | PASS_REVIEW_FAIL |
| Standard | Knowledge QA V1.0 |

---

# 1. Frozen verdicts

| Verdict | Code | Meaning |
|---------|------|---------|
| **PASS** | `PASS` | No blocking defect. Eligible for Domain Reviewer → **Reviewed**. |
| **REVIEW** | `REVIEW` | Defect documented. Remains **Draft** until resolved and re-QA’d. |
| **FAIL** | `FAIL` | Blocking defect. Must not promote. Requires authoring fix. |
| **Borderline** | `BORDERLINE` | Meets numeric band but human judgment required. Not auto-PASS. |

---

# 2. Decision rules

Apply in order:

```text
1. Any criterion scored 0 → FAIL
2. Any criterion scored 3 → FAIL (unless Domain Reviewer waives with record)
3. Any criterion scored 5 on Evidence, Traceability, or Cross-Pack → REVIEW minimum
4. Any criterion scored 5 on Commercial Quality or Professional Correctness → REVIEW minimum
5. All criteria ≥ 7 → PASS eligible
6. Average 7.0–7.4, all criteria ≥ 5, none ≤ 3 → BORDERLINE
7. Otherwise → REVIEW
```

**QA PASS ≠ Validated.** **QA PASS ≠ Frozen.**

---

# 3. What happens after each outcome

## PASS

| Step | Action |
|------|--------|
| 1 | Archive QA record (template in [QA_TEMPLATE.md](QA_TEMPLATE.md)) |
| 2 | Domain Reviewer confirms or rejects |
| 3 | On confirm → unit status **Reviewed** |
| 4 | Unit enters validation queue ([QA_CHECKLIST.md](QA_CHECKLIST.md)) |

Author may **not** self-promote to Reviewed.

## REVIEW

| Step | Action |
|------|--------|
| 1 | Document **what is missing** (not a rewrite in QA task) |
| 2 | Assign owner: Author, Governance, or Reasoning policy |
| 3 | Unit stays **Draft** |
| 4 | Re-QA same `knowledge_id` after fix |

REVIEW is **not** a failure of the QA process. It is the normal gate for scale.

## FAIL

| Step | Action |
|------|--------|
| 1 | Document **why** (blocking criterion + evidence) |
| 2 | Unit stays **Draft**; block validation |
| 3 | Authoring task required |
| 4 | Full re-QA after fix |

Do **not** validate, freeze, or ship FAIL units to Customer Mode.

## Borderline

| Step | Action |
|------|--------|
| 1 | Domain Reviewer reads QA rationale |
| 2 | Decision: PASS (promote Reviewed) or REVIEW (hold) — recorded |
| 3 | Cursor/AI cannot resolve Borderline alone |

---

# 4. Topic phase gates

Pack QA runs **by topic** (MEANING, CAUSES, ADVANTAGES, …).

| Phase outcome | Pack gate |
|---------------|-----------|
| Any FAIL in phase | Phase incomplete; fix FAIL units before pack validation |
| All units PASS or REVIEW | Phase complete; REVIEW tracked |
| Zero FAIL, REVIEW ≤ governance threshold | Pack may proceed to next phase |

Threshold for acceptable REVIEW count is **governance decision per pack**, not defined in V1.0 standard.

---

# 5. Relationship to catalog status

| Catalog status | QA verdict allowed |
|----------------|-------------------|
| Draft | PASS, REVIEW, FAIL |
| Reviewed | Only after QA PASS + Domain Reviewer |
| Validated | Only after QA_CHECKLIST + no open FAIL |
| Frozen | Only after FREEZE_POLICY |
| Deprecated | N/A — no new QA except audit |

---

END
