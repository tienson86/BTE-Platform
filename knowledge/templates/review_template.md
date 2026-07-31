# Review Template

**Template ID:** TPL-KR-REVIEW-001  
**Version:** 1.0.0  
**Status:** Specification  
**Applies to:** Academic / Technical / Governance review of a Knowledge Record  
**Aligns with:** `knowledge/governance/review_workflow.json` · `knowledge/quality/*_scorecard.json`

---

## Instructions

1. One review package per `{{RECORD_ID}}` version under review.
2. Fill placeholders; cite checklist item IDs (`RC-*`, `GR-*`) in findings.
3. Author SHOULD NOT be the sole Approver for official promotion.

---

# R1 — Review header

| Field | Value |
|------|-------|
| Record ID | `{{RECORD_ID}}` |
| Canonical Name | `{{CANONICAL_NAME}}` |
| Version reviewed | `{{VERSION}}` |
| Pack / Module | `{{PACK_ID}}` / `{{MODULE_ID}}` |
| Review type | `{{REVIEW_TYPE}}` <!-- academic \| technical \| governance \| combined --> |
| Review date | `{{REVIEW_DATE}}` |
| Reviewer | `{{REVIEWER}}` |

---

# R2 — Academic review

| Field | Value |
|------|-------|
| Status | `{{ACADEMIC_REVIEW_STATUS}}` <!-- pending \| in_review \| approved \| rejected \| waived --> |
| Definition accuracy | `{{ACADEMIC_DEFINITION_STATUS}}` |
| Traceability | `{{ACADEMIC_TRACEABILITY_STATUS}}` |
| Bibliography integrity | `{{ACADEMIC_BIBLIOGRAPHY_STATUS}}` |
| Score (0–100) | `{{ACADEMIC_SCORE}}` |
| Findings | {{ACADEMIC_FINDINGS}} |
| `TODO_REVIEW` items remaining | {{ACADEMIC_TODO_REVIEW}} |

---

# R3 — Technical review

| Field | Value |
|------|-------|
| Status | `{{TECHNICAL_REVIEW_STATUS}}` |
| Schema / compiler compatibility | `{{TECHNICAL_COMPILER_STATUS}}` |
| Relationship integrity | `{{TECHNICAL_RELATIONSHIP_STATUS}}` |
| Graph integrity | `{{TECHNICAL_GRAPH_STATUS}}` |
| Score (0–100) | `{{TECHNICAL_SCORE}}` |
| Findings | {{TECHNICAL_FINDINGS}} |

---

# R4 — Governance review

| Field | Value |
|------|-------|
| Status | `{{GOVERNANCE_REVIEW_STATUS}}` |
| Approval matrix satisfied | `{{GOVERNANCE_MATRIX_OK}}` |
| Freeze readiness | `{{GOVERNANCE_FREEZE_READY}}` |
| Score (0–100) | `{{GOVERNANCE_SCORE}}` |
| Findings | {{GOVERNANCE_FINDINGS}} |

---

# R5 — Approval & freeze recommendation

| Field | Value |
|------|-------|
| Approval recommendation | `{{APPROVAL_STATUS}}` <!-- not_approved \| conditionally_approved \| approved --> |
| Freeze recommendation | `{{FREEZE_STATUS}}` <!-- unfrozen \| candidate \| frozen --> |
| Overall recommendation | `{{OVERALL_RECOMMENDATION}}` <!-- publish \| publish_after_minor_revision \| major_revision_required \| reject \| freeze_current_version --> |

---

# R6 — Checklist evidence

| Checklist item | Pass/Fail | Notes |
|----------------|-----------|-------|
| `{{RC_OR_GR_ID_1}}` | `{{ITEM_STATUS_1}}` | {{ITEM_NOTES_1}} |
| `{{RC_OR_GR_ID_2}}` | `{{ITEM_STATUS_2}}` | {{ITEM_NOTES_2}} |

---

# R7 — Decision log

| Date | Actor | Role | Decision | Notes |
|------|-------|------|----------|-------|
| `{{DECISION_DATE}}` | `{{DECISION_ACTOR}}` | `{{DECISION_ROLE}}` | `{{DECISION}}` | {{DECISION_NOTES}} |

---

## Governance mapping

| Template block | Governance / schema |
|----------------|---------------------|
| R2–R4 | `review.schema.json` academic/technical/governance |
| R5 | `approval` + `freeze` |
| Workflow stages | `RV-02-ACADEMIC` … `RV-04-GOVERNANCE` |
