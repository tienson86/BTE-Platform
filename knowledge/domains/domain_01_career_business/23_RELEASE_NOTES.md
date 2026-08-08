# 23 — Release Notes · Career Selection Assessment · Production Capability V1

Version: 1.0  
Status: **RELEASED TO PRODUCTION PATH**  
Date: 2026-08-08  
Capability: CAP-D1-CA-SEL  

---

## 1. Headline

**Career Selection Assessment** is the first completed Commercial Capability on the live Result pipeline.

Customers who analyze a BaZi chart now receive Career Selection Assessment content inside the existing Result Page (Executive / strengths / warnings / actions slots), driven by approved Domain 01 SEL Knowledge Units.

---

## 2. Included

- Production allow-list: Wave 1.1 cores + 11 Career Selection Assessment units  
- Multi-CSV retrieval (`21` + `22`)  
- Typed `career_selection_assessment` on Commercial Bundle + `narrative_result`  
- Narrative soft-enrichment for Executive Summary / Recommendation / Decision Support  
- Portal adapter consumption without new routes or layout redesign  
- Golden Case + `tests/domain01` coverage  

---

## 3. Explicitly not included

- New Knowledge Units  
- Wave 1.1 content edits  
- Promotion Readiness capability  
- Leadership Assessment / Partnership / Entrepreneurship packs  
- New Result screens, APIs, Design System, or Visual Language changes  
- Interpretation Engine or Score Engine redesign  

---

## 4. Customer value

| Before | After |
|--------|-------|
| Core identity / strength / useful-god / generic action | Career families, environment, role, postures, risks, mitigation, development, timing, 90-day plan |
| Recommendation as short useful-god action | Structured 90-day career plan (KU-AC-CA-000001) |
| No Domain 01 capability projection | `CAP-D1-CA-SEL` complete on Result path |

---

## 5. Ops / engineering notes

- Default `CommercialKnowledgeAdapter()` remains Wave 1.1 for backward-compatible module tests.  
- Production wiring (`narrative_result_truth`) passes `PRODUCTION_ALLOW_LIST`.  
- Narrative must never consume raw Knowledge Unit CSV rows — only Bundle / assessment.  

---

## 6. Product Review gate

This release stops at **Production Capability V1**.

**Do not start Promotion Readiness until Product Review signs off.**

---

END
