# Checklists — V1.0

| Field | Value |
|-------|-------|
| Document | CHECKLISTS |
| Version | 1.0.0 |
| Section | 14 — Checklists |

---

# 14.1 Author — Library (QG1)

| # | Check | ☐ |
|---|-------|---|
| 1 | Pack charter (QG0) approved | |
| 2 | All planned chapters drafted | |
| 3 | KNOWLEDGE_INDEX complete | |
| 4 | No rule ids, scores, algorithms in prose | |
| 5 | All strength classes covered (or pack equivalent) | |
| 6 | Interpretation Standard bans respected | |
| 7 | Examples chapter marked Validation-only | |
| 8 | README and KNOWLEDGE_ARCHITECTURE current | |
| 9 | Knowledge Version bumped | |
| 10 | Self-read aloud for consultant voice | |

**Approver:** Domain Reviewer  
**Sign-off:** _________________ Date: _______

---

# 14.2 Author — Catalog (QG2)

| # | Check | ☐ |
|---|-------|---|
| 1 | Library QG1 passed for this topic/pack | |
| 2 | Every unit matches CATALOG_SCHEMA | |
| 3 | One primary claim per unit | |
| 4 | `source_document` exact filename on every unit | |
| 5 | `knowledge_id` unique; id policy followed | |
| 6 | `required_facts` and `limitations` set | |
| 7 | Class gate on class-specific units | |
| 8 | `duplicate_cluster` declared for known overlaps | |
| 9 | All units status **Draft** | |
| 10 | CATALOG_INDEX matches file count | |
| 11 | CATALOG_ARCHITECTURE and CHANGELOG updated | |
| 12 | Author self-check: `knowledge/knowledge_qa/STANDARD/QA_CHECKLIST.md` §1 | |

**Approver:** Domain Reviewer  
**Sign-off:** _________________ Date: _______

---

# 14.3 QA (QG3)

| # | Check | ☐ |
|---|-------|---|
| 1 | Topic scope and unit count confirmed | |
| 2 | All twelve criteria scored per unit | |
| 3 | Scores use 0/3/5/7/9/10 only | |
| 4 | Verdict per PASS_REVIEW_FAIL rules | |
| 5 | Rationale for every REVIEW and FAIL | |
| 6 | FAIL count = 0 (or waiver attached) | |
| 7 | Phase review follows QA_TEMPLATE | |
| 8 | Review archived under `knowledge_qa/PACK_XX/` | |
| 9 | No catalog edits during QA-only task | |
| 10 | Topic summary statistics included | |

**Acceptance:** Domain Reviewer (not QA Assistant alone)  
**Sign-off:** _________________ Date: _______

Reference: `knowledge/knowledge_qa/STANDARD/QA_CHECKLIST.md`

---

# 14.4 Review (QG4)

| # | Check | ☐ |
|---|-------|---|
| 1 | QA phase accepted | |
| 2 | PASS units promoted to **Reviewed** | |
| 3 | REVIEW items assigned owner | |
| 4 | Borderline decisions documented | |
| 5 | Author ≠ sole reviewer (or exception recorded) | |
| 6 | Cursor not listed as final approver | |
| 7 | Duplicate representatives confirmed | |
| 8 | Cross-pack flags triaged | |

**Approver:** Domain Reviewer  
**Sign-off:** _________________ Date: _______

---

# 14.5 Validation (QG5)

| # | Check | ☐ |
|---|-------|---|
| 1 | All Reviewed units in validation scope | |
| 2 | Reasoning FREEZE golden cases loaded | |
| 3 | Golden-pinned knowledge_ids listed | |
| 4 | Pinned units: no open FAIL | |
| 5 | Pinned units: REVIEW resolved or waived | |
| 6 | required_facts align with golden facts | |
| 7 | duplicate_cluster aligns with golden reject/accept | |
| 8 | customer_mode aligns with golden Customer path | |
| 9 | VALIDATION_RECORD.md archived | |
| 10 | Units promoted to **Validated** | |

**Approvers:** Domain Reviewer + Reasoning governance  
**Sign-off:** _________________ Date: _______

---

# 14.6 Freeze (QG6)

| # | Check | ☐ |
|---|-------|---|
| 1 | 100% production-scope units **Validated** | |
| 2 | No open FAIL anywhere in pack | |
| 3 | REVIEW items resolved or Chief Reviewer waived | |
| 4 | Duplicate clusters final | |
| 5 | Catalog version bumped | |
| 6 | Catalog CHANGELOG updated | |
| 7 | FREEZE_POLICY satisfied (QA Standard) | |
| 8 | All production units set **Frozen** | |
| 9 | Freeze record archived | |
| 10 | Reasoning version compatibility confirmed | |

**Approver:** Chief Reviewer  
**Sign-off:** _________________ Date: _______

Reference: `knowledge/knowledge_qa/STANDARD/FREEZE_POLICY.md`

---

# 14.7 Release (QG7)

| # | Check | ☐ |
|---|-------|---|
| 1 | QG6 complete — Frozen catalog exists | |
| 2 | Production Owner loaded Frozen version | |
| 3 | Golden smoke tests pass | |
| 4 | Missing-fact rejection verified | |
| 5 | Customer Mode path verified | |
| 6 | Release version tagged (VERSIONING) | |
| 7 | Release manifest lists all version dimensions | |
| 8 | Rollback pointer to prior Frozen version | |
| 9 | Release notes drafted | |
| 10 | Production Owner sign-off | |
| 11 | Release Manager sign-off | |

**Approvers:** Production Owner + Release Manager  
**Sign-off:** _________________ Date: _______

---

# 14.8 Universal sign-off block

```text
Pack: _______________________
Gate: QG___
Scope: ______________________
Catalog Version: _____________
Knowledge Version: ___________
Reasoning Version: ___________
Reviewer: ____________________
Decision: PASS / HOLD / WAIVE
Date: ________________________
Notes: _______________________
```

---

END
