# Change Pipeline — V1.0

| Field | Value |
|-------|-------|
| Document | CHANGE_PIPELINE |
| Version | 1.0.0 |
| Section | 11 — Change Management |

---

# 11.1 Rule

**Never edit production directly.**

Frozen and released knowledge changes only through a **new version** and full factory path for affected artifacts.

---

# 11.2 Change types

| Type | Trigger | Path |
|------|---------|------|
| **Correction** | Professional error found | Library → Catalog → QA → … |
| **Enhancement** | New insight approved | New units or chapters |
| **Deprecation** | Duplicate, unsafe, superseded | Deprecate id; add successor |
| **Golden update** | Reasoning policy change | Validation re-run |
| **Emergency rollback** | Production defect | Rollback version; then change pipeline |

---

# 11.3 Change workflow

```text
Change request logged
  ↓
Chief Reviewer triage (scope + impact)
  ↓
Never edit Frozen unit in place
  ↓
Edit Library (if prose change) OR Catalog Draft (if metadata only)
  ↓
Increment Knowledge and/or Catalog version
  ↓
Re-run factory stages from first affected gate:
  Catalog (QG2) → QA (QG3) → Review (QG4) → Validation (QG5) → Freeze (QG6)
  ↓
Production Owner loads new Frozen version
  ↓
Release Manager publishes new Release (if customer-visible)
  ↓
Deprecate superseded ids
```

---

# 11.4 What may not change in place

| Artifact | Rule |
|----------|------|
| Frozen catalog unit | New version only |
| Production-loaded catalog | Swap version pointer |
| Released knowledge_id claim | Deprecate old; new id for new claim |
| Golden reference | Reasoning FREEZE update + re-validation |

---

# 11.5 Deprecation rules

| Rule | Detail |
|------|--------|
| knowledge_id | Never reused after Deprecated |
| Successor | New id documents replacement |
| Reasoning | Stops selecting Deprecated |
| Audit | Deprecation reason archived |

---

# 11.6 Impact assessment

Every change request documents:

| Field | Required |
|-------|----------|
| Affected knowledge_ids | List |
| Current catalog version | |
| Customer impact | None / low / high |
| Golden impact | Yes / no |
| Minimum re-gate | QG2 … QG7 |

Chief Reviewer approves scope before Author begins.

---

# 11.7 PACK-01 example (hypothetical)

**Request:** Fix CAUS-0002 season polarity evidence gate.

```text
Edit catalog limitations + required_facts (Draft)
  ↓
Re-QA CAUS-0002
  ↓
Domain Reviewer → Reviewed → Validated
  ↓
Re-validate CASE-0001 golden
  ↓
New catalog version freeze
  ↓
Production load + release note
```

No edit to Frozen 1.0.0 in place.

---

END
