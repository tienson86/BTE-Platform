# 11 — Before / After Comparison (Wave 1.1)

Version: 1.0  
Status: **EPIC 4 · SPRINT B**  
Date: 2026-08-08  
Fixture: Strong chart · day master Giáp · cách cục Chính Quan · Dụng thần Thủy · strength vuong  

Method: `build_narrative_result_dict(..., include_commercial_knowledge=False|True)`

---

## 1. Executive Summary

### Before Wave 1.1

| Slot | Text |
|------|------|
| Identity | `Quan sát từ dữ liệu phân tích: Nhật chủ: Giáp. Cách cục: Chính Quan` |
| Strengths | Same observation-style line (analysis echo) |
| Weaknesses | `Chưa đủ dữ liệu để đưa ra kết luận.` |
| Priority / next | `Ưu tiên phát huy theo nguồn phân tích: Dụng thần / khuyến nghị: Thủy.` |

Tone: calculator / data observation. Short token recommendation (`Thủy`).

### After Wave 1.1

| Slot | Text |
|------|------|
| Identity | `Bạn là người mang Nhật chủ Giáp trong cấu trúc Chính Quan. Điểm tựa chính của bạn nằm ở chỗ cấu trúc đang được nâng đỡ: thân vuong…` |
| Strengths | Commercial strength framing from KU-ST-001 (nền chịu trách nhiệm / nhịp dài) |
| Weaknesses | Unchanged insufficient flag (KU-WK-001 correctly not selected) |
| Priority / next | `Hành động: Ưu tiên các việc nuôi Dụng thần Thủy trong 2–4 tuần tới; tạm xếp sau những việc làm lệch hướng này.` |

Selected units: `KU-ID-001`, `KU-ST-001`, `KU-UG-001`, `KU-RC-001` · `bundle_status=complete`

---

## 2. Recommendation

### Before

| Field | Value |
|-------|-------|
| action | `Ưu tiên phát huy theo nguồn phân tích: Dụng thần / khuyến nghị: Thủy.` |
| reason | _(empty)_ |
| knowledge_refs | `knowledge:useful_god` |

### After

| Field | Value |
|-------|-------|
| action | KU-RC-001 action prose (2–4 tuần; nuôi Dụng thần Thủy) |
| reason | KU-UG-001 framing (`thuận theo Dụng thần Thủy`) |
| interpretation_refs | `interp:ck-KU-RC-001`, `interp:ck-KU-UG-001` |
| knowledge_refs | includes `knowledge:KU-RC-001` |

---

## 3. What improved

- Consultant language for identity and strength (not raw field dumps).  
- Actionable recommendation with time window and next-step posture.  
- Useful-god explanation available as recommendation reason.  
- Provenance: KU ids on knowledge_refs / commercial bundle.  
- Bundle attached on API payload for Portal traceability.

---

## 4. What remained unchanged

- Analytical facts (day master, pattern, useful god code, scores/grades).  
- Interpretation Engine conclusions (baseline sections preserved; commercial sections appended).  
- Narrative Pack 05 section set (same titles / component ids).  
- Weaknesses slot when no weakness signal (still insufficient — correct).  
- Foundation, Design System, UI layout, Report Engine.  
- Wave 1.1 CSV wording (content not edited).

---

## 5. Remaining gaps

| Gap | Notes |
|-----|-------|
| Publish status | Units still `awaiting_review`; Product must decide formal Publish |
| Weakness/Warning path | Needs weak/enemy fixture in live runs to surface KU-WK-001 |
| Section body fill | Some Pack 05 section bodies still empty; summary/recommendations carry prose |
| Band label polish | Analysis may pass `vuong` token into bound text |
| Portal surfacing | Bundle is available on API; UI not redesigned this sprint |
| Wave 1.2+ | Domains beyond core identity/strength/weakness/UG/action not integrated |

---

## 6. Success criteria check

| Criterion | Status |
|-----------|--------|
| Commercial Knowledge Adapter implemented | ✓ |
| CommercialKnowledgeBundle implemented | ✓ |
| Wave 1.1 integrated | ✓ |
| Executive Summary improved | ✓ |
| Recommendation improved | ✓ |
| Traceability preserved | ✓ |
| Module tests PASS | ✓ (16/16) |
| Build / Python module path PASS | ✓ |
| Stop before Wave 1.2 | ✓ |

---

## 7. Stop line

Comparison complete for Sprint B Product Review.  
**Do not start Wave 1.2.**

---

END
