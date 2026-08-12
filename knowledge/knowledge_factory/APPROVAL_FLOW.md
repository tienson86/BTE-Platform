# Approval Flow — V1.0

| Field | Value |
|-------|-------|
| Document | APPROVAL_FLOW |
| Version | 1.0.0 |

---

# 1. Principle

**Human approval at every promotion gate.**

Cursor and QA Assistant **recommend**. Humans **approve**.

---

# 2. Approval chain

```text
Knowledge Author          (creates)
       ↓
Cursor                    (assists — no approval)
       ↓
QA Assistant              (scores — no approval)
       ↓
Domain Reviewer           (Review + Validation approval)
       ↓
Chief Reviewer            (Charter + Freeze + waivers)
       ↓
Production Owner          (Production load)
       ↓
Release Manager           (Release)
```

---

# 3. Approval matrix

| Decision | Approver | Cannot approve |
|----------|----------|----------------|
| Pack charter (QG0) | Chief Reviewer | Author alone |
| Library ready (QG1) | Domain Reviewer | Author alone |
| Catalog ready (QG2) | Domain Reviewer | Author alone |
| Accept QA (QG3→4) | Domain Reviewer | QA Assistant alone |
| Draft → Reviewed | Domain Reviewer | Cursor |
| Reviewed → Validated | Domain Reviewer + Reasoning gov | QA Assistant |
| Pack Freeze (QG6) | Chief Reviewer | Domain Reviewer alone |
| QA FAIL waiver | Chief Reviewer | Domain Reviewer |
| Production load | Production Owner | Release Manager alone |
| Release (QG7) | Release Manager + Production Owner | Author |

---

# 4. Sign-off artifacts

| Gate | Sign-off location |
|------|-------------------|
| QG0 | Pack charter / governance record |
| QG1 | Library README or governance record |
| QG2 | Catalog README or checklist |
| QG4 | Phase review § Domain Reviewer sign-off |
| QG5 | VALIDATION_RECORD.md |
| QG6 | Freeze record + catalog CHANGELOG |
| QG7 | Release manifest |

Template block in [CHECKLISTS.md](CHECKLISTS.md).

---

# 5. Borderline and waiver

| Situation | Approver | Record |
|-----------|----------|--------|
| QA Borderline | Domain Reviewer | Phase review decision |
| QA FAIL waiver | Chief Reviewer | Written impact assessment |
| REVIEW carry to Validated | Chief Reviewer or Domain Reviewer | Checklist waiver line |
| Emergency production rollback | Production Owner + Release Manager | Incident record |

---

# 6. Conflict of interest

| Rule | Detail |
|------|--------|
| Author ≠ sole Reviewer | Same person may not approve own QA |
| QA Assistant ≠ Reviewer | AI output always reviewed by human |
| Production Owner ≠ Author | Recommended separation |

Small teams may combine roles with documented exception on sign-off.

---

# 7. Cursor boundary (explicit)

Cursor **never** appears as final approver on:

- Reviewed status
- Validated status
- Frozen status
- Production load
- Release

Cursor may appear as **QA Assistant** with human Domain Reviewer acceptance.

---

END
