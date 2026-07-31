# Release Template

**Template ID:** TPL-KR-RELEASE-001  
**Version:** 1.0.0  
**Status:** Specification  
**Applies to:** Publication / freeze / release of a Knowledge Record  
**Aligns with:** `knowledge/governance/publication_workflow.json` · `release_policy.json` · `freeze_policy.json`

---

## Instructions

1. Use only after review package recommends publish (or freeze candidate).
2. `release_status=released` REQUIRES `freeze=frozen` and `approval=approved`.
3. Update indexes at publication; do not change `{{RECORD_ID}}`.

---

# P1 — Release header

| Field | Value |
|------|-------|
| Record ID | `{{RECORD_ID}}` |
| Canonical Name | `{{CANONICAL_NAME}}` |
| Version | `{{VERSION}}` |
| Pack / Module | `{{PACK_ID}}` / `{{MODULE_ID}}` |
| Canon version | `{{CANON_VERSION}}` |
| Release Manager | `{{RELEASE_MANAGER}}` |
| Release date | `{{RELEASE_DATE}}` |

---

# P2 — Gate checklist (REL-G-*)

| Gate | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| REL-G-001 | Reviews complete | `{{REL_G_001}}` | {{REL_G_001_EVIDENCE}} |
| REL-G-002 | Approval = approved | `{{REL_G_002}}` | {{REL_G_002_EVIDENCE}} |
| REL-G-003 | Freeze = frozen | `{{REL_G_003}}` | {{REL_G_003_EVIDENCE}} |
| REL-G-004 | Quality threshold met | `{{REL_G_004}}` | {{REL_G_004_EVIDENCE}} |
| REL-G-005 | Schema / indexes OK | `{{REL_G_005}}` | {{REL_G_005_EVIDENCE}} |
| REL-G-006 | Changelog present | `{{REL_G_006}}` | {{REL_G_006_EVIDENCE}} |
| REL-G-007 | No high-confidence `TODO_REVIEW` | `{{REL_G_007}}` | {{REL_G_007_EVIDENCE}} |

---

# P3 — Publication workflow stages

| Stage | Status | Notes |
|-------|--------|-------|
| PB-01 Freeze candidate | `{{PB_01}}` | {{PB_01_NOTES}} |
| PB-02 Freeze | `{{PB_02}}` | {{PB_02_NOTES}} |
| PB-03 Index sync | `{{PB_03}}` | {{PB_03_NOTES}} |
| PB-04 Release | `{{PB_04}}` | {{PB_04_NOTES}} |
| PB-05 Post-release verification | `{{PB_05}}` | {{PB_05_NOTES}} |

---

# P4 — Freeze record

| Field | Value |
|------|-------|
| Freeze status | `{{FREEZE_STATUS}}` |
| Frozen at | `{{FROZEN_AT}}` |
| Frozen by | `{{FROZEN_BY}}` |
| Unfreeze change request (if any) | `{{CHANGE_REQUEST_ID}}` |

---

# P5 — Release note

### Summary

{{RELEASE_SUMMARY}}

### Changes in this version

- {{CHANGE_1}}
- {{CHANGE_2}}

### Consumer impact

{{CONSUMER_IMPACT}}

### Known limitations

{{KNOWN_LIMITATIONS}}

---

# P6 — Index & compiler post-checks

- [ ] `record_index` status = official / compiler_status updated: `{{COMPILER_STATUS}}`
- [ ] `canonical_index` unique for `{{CANONICAL_KEY}}`
- [ ] Cross-references published
- [ ] No record_id remap

---

# P7 — Sign-off

| Role | Actor | Decision | Date |
|------|-------|----------|------|
| Governance Owner | `{{GOVERNANCE_OWNER}}` | `{{GOV_DECISION}}` | `{{GOV_DATE}}` |
| Release Manager | `{{RELEASE_MANAGER}}` | `{{RM_DECISION}}` | `{{RM_DATE}}` |

**Final release status:** `{{RELEASE_STATUS}}` <!-- unreleased \| candidate \| released \| superseded \| withdrawn -->
