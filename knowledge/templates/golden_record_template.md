# Golden Record Template

**Template ID:** TPL-KR-GOLDEN-001  
**Version:** 1.0.0  
**Status:** Specification  
**Applies to:** Golden / official Knowledge Record candidates  
**Depends on:** Type-specific template + `knowledge_record_template.md`  
**Gate:** `knowledge/quality/golden_record_checklist.json`

---

## Authoring instructions

1. Complete the matching type template (`foundational_concept_template.md`, `entity_template.md`, or `rule_template.md`).
2. Copy this golden overlay and fill every `{{PLACEHOLDER}}`.
3. All eight quality metrics MUST pass (≥ 80); overall score for golden promotion ≥ **90**.
4. Do **not** rewrite locked golden datasets, snapshots, or expected test outputs to force a pass.

---

# G1 — Candidate identity

| Field | Value |
|------|-------|
| Record ID | `{{RECORD_ID}}` |
| Canonical Name | `{{CANONICAL_NAME}}` |
| Candidate version | `{{VERSION}}` |
| Pack / Module | `{{PACK_ID}}` / `{{MODULE_ID}}` |
| Type template used | `{{TYPE_TEMPLATE_FILE}}` |

---

# G2 — Golden checklist (GR-*)

| Item | Requirement | Status | Evidence |
|------|-------------|--------|----------|
| GR-001 | Record ID immutable and registered | `{{GR_001_STATUS}}` | {{GR_001_EVIDENCE}} |
| GR-002 | Academic scorecard ≥ 80; no blocking bibliography gaps | `{{GR_002_STATUS}}` | {{GR_002_EVIDENCE}} |
| GR-003 | Technical scorecard ≥ 80 (compiler + relationships + graph) | `{{GR_003_STATUS}}` | {{GR_003_EVIDENCE}} |
| GR-004 | Governance pass; approval approved; freeze frozen/candidate accepted | `{{GR_004_STATUS}}` | {{GR_004_EVIDENCE}} |
| GR-005 | All mandatory RC-* review checklist items satisfied | `{{GR_005_STATUS}}` | {{GR_005_EVIDENCE}} |
| GR-006 | No open `TODO_REVIEW` on high-confidence claims | `{{GR_006_STATUS}}` | {{GR_006_EVIDENCE}} |
| GR-007 | Unique canonical Concept node; no dependency cycles | `{{GR_007_STATUS}}` | {{GR_007_EVIDENCE}} |
| GR-008 | Promotion does not rewrite locked snapshots / expected outputs | `{{GR_008_STATUS}}` | {{GR_008_EVIDENCE}} |

---

# G3 — Quality metric scores

| Metric | Score (0–100) | Notes |
|--------|---------------|-------|
| Completeness | `{{QM_COMPLETENESS}}` | {{QM_COMPLETENESS_NOTES}} |
| Consistency | `{{QM_CONSISTENCY}}` | {{QM_CONSISTENCY_NOTES}} |
| Traceability | `{{QM_TRACEABILITY}}` | {{QM_TRACEABILITY_NOTES}} |
| Compiler Compatibility | `{{QM_COMPILER}}` | {{QM_COMPILER_NOTES}} |
| Relationship Integrity | `{{QM_RELATIONSHIP}}` | {{QM_RELATIONSHIP_NOTES}} |
| Bibliography Integrity | `{{QM_BIBLIOGRAPHY}}` | {{QM_BIBLIOGRAPHY_NOTES}} |
| Graph Integrity | `{{QM_GRAPH}}` | {{QM_GRAPH_NOTES}} |
| Governance Compliance | `{{QM_GOVERNANCE}}` | {{QM_GOVERNANCE_NOTES}} |
| **Overall (weighted)** | `{{QM_OVERALL}}` | |

---

# G4 — Governance freeze & release

| Field | Value |
|------|-------|
| Academic review | `{{ACADEMIC_REVIEW_STATUS}}` |
| Technical review | `{{TECHNICAL_REVIEW_STATUS}}` |
| Governance review | `{{GOVERNANCE_REVIEW_STATUS}}` |
| Approval | `{{APPROVAL_STATUS}}` |
| Freeze | `{{FREEZE_STATUS}}` |
| Release status | `{{RELEASE_STATUS}}` |
| Canon version | `{{CANON_VERSION}}` |
| Change request (if unfreeze/supersede) | `{{CHANGE_REQUEST_ID}}` |

---

# G5 — Index & graph publication checklist

- [ ] `record_index.json` entry present for `{{RECORD_ID}}`
- [ ] `canonical_index.json` key unique: `{{CANONICAL_KEY}}`
- [ ] Aliases registered (no second canonical identity)
- [ ] Cross-references validated (no duplicate triples)
- [ ] Graph constraints respected (acyclicity, immutable ID)

---

# G6 — Compiler readiness

| Field | Value |
|------|-------|
| Compiler status | `{{COMPILER_STATUS}}` |
| Target artifacts | `{{COMPILER_ARTIFACTS}}` |
| Blocking compiler notes | {{COMPILER_BLOCKERS}} |

---

# G7 — Golden decision

| Field | Value |
|------|-------|
| Eligible for golden | `{{GOLDEN_ELIGIBLE}}` <!-- yes \| no --> |
| Blocking items | {{GOLDEN_BLOCKERS}} |
| Decision | `{{GOLDEN_DECISION}}` <!-- promote \| hold \| reject --> |
| Decision by | `{{GOLDEN_DECIDER}}` |
| Decision date | `{{GOLDEN_DECISION_DATE}}` |

---

## Notes

{{GOLDEN_NOTES}}
