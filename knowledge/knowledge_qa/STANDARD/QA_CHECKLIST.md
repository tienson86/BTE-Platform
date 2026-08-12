# QA Checklist — V1.0

| Field | Value |
|-------|-------|
| Document | QA_CHECKLIST |
| Standard | Knowledge QA V1.0 |
| Use | Before Reviewed → Validated promotion |

---

# 1. Author self-check (before QA submission)

| # | Check | ☐ |
|---|-------|---|
| 1 | `knowledge_id` unique and stable | |
| 2 | `source_document` exact filename; claim traceable | |
| 3 | One primary claim (So what) | |
| 4 | Class gate matches claim | |
| 5 | Topic matches declared purpose (MEANING/CAUSE/ADV/…) | |
| 6 | `required_facts` lists every implied fact | |
| 7 | `limitations` gate unpublished facts | |
| 8 | No rule ids, scores, thresholds in claim | |
| 9 | `customer_mode` matches claim safety | |
| 10 | `duplicate_cluster` set if overlap known | |
| 11 | No hard cross-pack dependency undeclared | |
| 12 | Supporting points support the claim (not blind spot) | |

---

# 2. QA Assistant check (during review)

| # | Check | ☐ |
|---|-------|---|
| 1 | All twelve criteria scored 0/3/5/7/9/10 | |
| 2 | Verdict assigned per PASS_REVIEW_FAIL rules | |
| 3 | Rationale written for every REVIEW/FAIL | |
| 4 | Duplicate clusters cross-checked | |
| 5 | Golden references checked if unit pinned | |
| 6 | No catalog status change in QA-only task | |
| 7 | No claim rewrite in QA-only task | |

---

# 3. Domain Reviewer check (before Validated)

| # | Check | ☐ |
|---|-------|---|
| 1 | QA PASS accepted or Borderline resolved | |
| 2 | No open FAIL on unit | |
| 3 | REVIEW items resolved or governance-waived | |
| 4 | Evidence gates align with Reasoning FREEZE policy | |
| 5 | Duplicate representative identified per cluster | |
| 6 | Cross-pack dependencies declared or isolated | |
| 7 | Consistency with Narrative budget / golden plan | |
| 8 | Phase review archived under `knowledge_qa/PACK_XX/` | |
| 9 | Catalog CHANGELOG updated if pack-level | |
| 10 | Human sign-off recorded (not AI-only) | |

---

# 4. Governance check (before Freeze)

| # | Check | ☐ |
|---|-------|---|
| 1 | All production-scope units Validated | |
| 2 | Catalog version incremented | |
| 3 | FREEZE_POLICY prerequisites met | |
| 4 | Deprecated ids documented if any | |
| 5 | Reasoning consumption scope confirmed | |

---

# 5. Sign-off block

```text
Pack: _______________________
Topic / Unit ids: ___________
Catalog version: ____________
QA phase file: _______________
Domain Reviewer: _____________ Date: _______
Governance (if Freeze): ______ Date: _______
```

---

END
