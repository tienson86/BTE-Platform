# Review Process — V1.0

| Field | Value |
|-------|-------|
| Document | REVIEW_PROCESS |
| Standard | Knowledge QA V1.0 |

---

# 1. Frozen flow

```text
Author
  ↓
QA Assistant
  ↓
Domain Reviewer
  ↓
Approval (Governance)
  ↓
Freeze
```

**Cursor is never final authority.**

---

# 2. Roles

## Author

| Responsibility |
|----------------|
| Create catalog units from Interpretation Knowledge |
| Complete [QA_CHECKLIST.md](QA_CHECKLIST.md) self-check before submission |
| Fix FAIL/REVIEW items in authoring tasks (not in QA-only tasks) |
| Never self-promote to Reviewed or Validated |

## QA Assistant (may include Cursor / AI)

| Responsibility |
|----------------|
| Score all twelve criteria per [QA_CRITERIA.md](QA_CRITERIA.md) |
| Assign PASS / REVIEW / FAIL per [PASS_REVIEW_FAIL.md](PASS_REVIEW_FAIL.md) |
| Document rationale using [QA_TEMPLATE.md](QA_TEMPLATE.md) |
| **Recommend only** — cannot approve lifecycle promotion |

## Domain Reviewer

| Responsibility |
|----------------|
| Accept or reject QA Assistant output |
| Resolve Borderline verdicts |
| Waive criterion-3 FAIL only with written record |
| Promote Draft → Reviewed |
| Promote Reviewed → Validated after checklist |

## Approval (Governance)

| Responsibility |
|----------------|
| Pack-level validation sign-off |
| Duplicate cluster ownership |
| Cross-pack dependency declarations |
| Freeze events per [FREEZE_POLICY.md](FREEZE_POLICY.md) |

---

# 3. Submission package

Author submits:

1. Unit id list or topic phase scope
2. Catalog paths
3. Source document mapping
4. Known duplicate clusters
5. Self-check against QA_CHECKLIST

QA Assistant returns:

1. Per-unit scores
2. Verdicts
3. Written rationale (no silent PASS)
4. Topic summary statistics

---

# 4. Escalation

| Condition | Escalate to |
|-----------|-------------|
| Cross-pack dependency | Governance + owning packs |
| Duplicate cluster dispute | Governance |
| Golden reference conflict | Reasoning + Domain Reviewer |
| Schema vs limitation conflict | Catalog governance + Reasoning |
| Commercial/safety concern | Governance — hold Validated |

---

# 5. Re-review

Re-QA required when:

- Claim text changes
- `required_facts` / limitations change
- Source document changes
- Duplicate cluster assignment changes
- Golden plan changes affecting unit

Re-QA **not** required for typo fix in metadata with no claim change — Domain Reviewer discretion.

---

END
