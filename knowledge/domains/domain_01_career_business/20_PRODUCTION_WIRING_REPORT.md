# 20 — Production Wiring Report · Career Selection Assessment

Version: 1.0  
Status: **PRODUCTION CAPABILITY V1 — WIRED**  
Date: 2026-08-08  
Capability: `CAP-D1-CA-SEL` · Career Selection Assessment  
Scope: Production integration only — no new Knowledge Units, no Narrative redesign, no layout/DS changes  

---

## 1. Mission result

Career Selection Assessment is available on the production Result path:

```
Analysis
  → CommercialKnowledgeAdapter (PRODUCTION_ALLOW_LIST)
  → CommercialKnowledgeBundle.career_selection_assessment
  → Narrative enrich (Executive Summary / Recommendation / Decision Support)
  → narrative_result (+ career_selection_assessment)
  → Portal adapters (existing Result Page slots)
```

**Production Capability V1** is live for Domain 01 Career Selection only.  
Promotion / Leadership / Partnership / other Domain 01 capabilities remain **off** the allow-list.

---

## 2. What was wired

| Layer | Change |
|-------|--------|
| Knowledge source | Loads `21_knowledge_units.csv` + `22_domain01_career_business.csv` |
| Allow-list | `PRODUCTION_ALLOW_LIST` = Wave 1.1 ∪ `CAREER_SELECTION_ALLOW_LIST` (11 SEL ids) |
| Adapter | Production hook passes `PRODUCTION_ALLOW_LIST`; default Adapter remains Wave 1.1-compatible |
| Bundle Builder | Maps SEL `evidence_kind` → typed Career Selection fields |
| Narrative Merge | Soft-enriches Exec/Rec paths; attaches assessment; does not replace Interpretation |
| API truth | `narrative_result_truth` attaches `commercial_knowledge_bundle` + `career_selection_assessment` |
| Portal | `narrativeResultAdapter` + `canonicalDesktopAdapter` prefer career fields inside **existing** S01/S08 slots |

---

## 3. Allow-list (Career Selection only)

| ID | Field |
|----|-------|
| KU-CN-CA-000001 | career_direction |
| KU-CN-CA-000010 | working_environment |
| KU-CN-CA-000011 | preferred_role |
| KU-CN-CA-000012 | leadership_posture |
| KU-CN-CA-000013 | employment_posture |
| KU-CN-CA-000014 | career_strengths |
| KU-RK-CA-000010 | career_risks |
| KU-MT-CA-000010 | career_mitigation |
| KU-CN-CA-000015 | development_focus |
| KU-CN-CA-000016 | timing_guidance |
| KU-AC-CA-000001 | action_plan_90d |

**Excluded:** `KU-CN-LE-000001`, `KU-AC-BU-000001`, and all non-SEL Domain 01 rows.

---

## 4. Bundle contract (Narrative never consumes raw KUs)

`career_selection_assessment` exposes:

- career_direction  
- working_environment  
- preferred_role  
- leadership_posture  
- employment_posture  
- career_strengths  
- career_risks  
- career_mitigation  
- development_focus  
- timing_guidance  
- action_plan_90d  

Each field carries `text`, `knowledge_unit_id`, `evidence_kind`, `version`, `confidence`.

---

## 5. Files changed (wiring)

### Runtime

- `engines/commercial_knowledge/models.py`
- `engines/commercial_knowledge/retrieval_service.py`
- `engines/commercial_knowledge/bundle_builder.py`
- `engines/commercial_knowledge/commercial_adapter.py`
- `engines/commercial_knowledge/narrative_merge.py`
- `engines/commercial_knowledge/__init__.py`
- `applications/api/services/narrative_result_truth.py`

### Portal (adapter only — no layout / DS / routes)

- `applications/customer_portal/src/adapters/narrativeResultAdapter.ts`
- `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts`
- `applications/customer_portal/src/adapters/index.ts`

### Tests

- `tests/domain01/*` (new)

### Not modified

- Wave 1.1 CSV content  
- Foundation / Design System / Visual Language  
- Interpretation Engine / Score Engine  
- Result Page layout / routes / APIs shape (additive fields only on narrative_result)

---

## 6. Traceability

```
Knowledge Unit
  → Commercial Bundle (career_selection_assessment)
  → Narrative enrichment + narrative_result
  → Portal existing Result slots
```

Bundle `traceability.capability_chain` records the capability path; legacy `traceability.chain` remains Wave 1.1-compatible.

---

## 7. Stop line

Career Selection Assessment = **Production Capability V1**.  

**Do not start Promotion Readiness. Wait for Product Review.**

---

END
