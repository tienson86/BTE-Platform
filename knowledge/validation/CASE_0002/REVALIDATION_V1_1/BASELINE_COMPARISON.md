# BASELINE_COMPARISON — CASE-0002 Post CDR V1.1

| Field | Value |
|-------|-------|
| Subject | Hoàng Thị Thu Phương |
| Birth | 1997-07-01 · 14:24 · Quảng Ninh · Female |
| Pillars | Đinh Sửu / Bính Ngọ / Giáp Thìn / Tân Mùi |
| Baseline | `knowledge/validation/CASE_0002/BASELINE.md` + `_raw_pipeline.json` |
| After | CDR V1.1 generic pipeline (this folder) |
| PDF | `exports/BTE_CASE-0002_Production_E2E.pdf` |
| Code edits this cycle | **None** |

---

## Technical: BEFORE vs AFTER

| Layer | BEFORE (baseline) | AFTER (CDR V1.1) | Changed? |
|-------|-------------------|------------------|----------|
| Strength | balanced · 0.61 | balanced · 0.61 | **No** (engine unchanged) |
| Ten Gods primary | Thương Quan (shang_guan) | Thương Quan (shang_guan) | **No** |
| Pattern | tong_nhi / Tòng Nhi · cực nhược theo Thực/Thương · than_vuong_nhuoc Trung hòa | identical | **No** |
| Useful God | Nhâm · Nhâm/Quý/Canh vs Bính/Đinh · mùa hạ cần thủy | identical | **No** |
| Domain conclusions | Same pilot composer texts | Same pilot composer texts | **No** (composers not rewritten) |
| Cross-domain tensions | `integrated.conflicts = []` | CDR tensions: `str_pattern_scope`, `follow_qualifies_strength`, `follow_strength_nuance`, `tg_vs_pattern_scope` | **Yes** (reasoning) |
| Primary theme | Implicit CASE-0001-shaped endurance/output stitch | `OPERATING_OUTPUT` (SECONDARY `FOLLOW_STRUCTURE`) | **Yes** |
| ExecutiveClaimPlan | N/A | Present (Thương Quan / Nhâm / Tòng + output insight) | **Yes** |
| Identity | Not wired | **AVAILABLE** | **Yes** |
| Career | Not wired | **AVAILABLE** | **Yes** |
| Executive insight | “sức bền… không phải gánh thêm vô hạn” | “Khung cấu trúc Tòng… + Vận hành theo đầu ra / biểu đạt” | **Yes** |

**Calculation engines:** unchanged — Strength / Pattern / Ten Gods / Useful God facts match baseline byte-for-byte on published fields.

---

## Feature availability

| Feature | BEFORE | AFTER |
|---------|--------|-------|
| Identity Report | NOT READY / not wired | AVAILABLE |
| Career Report | NOT READY / not wired | AVAILABLE |
| Executive Consulting | AVAILABLE (mismatched) | AVAILABLE (chart-aligned insight) |
| CrossDomainReasoningResult | Absent | Present (diagnostics) |
| Customer Deliverable | Domains + thin executive | Domains + Identity + Career + Executive |
| PDF | Prior baseline export | Regenerated under `REVALIDATION_V1_1/exports/` |

---

## ExecutiveClaimPlan (AFTER)

| Slot | Value |
|------|-------|
| identity_core | Output + body:balanced + Tòng Nhi structure |
| operating_style | Thương Quan |
| main_support | balance:Nhâm |
| main_constraint | follow_qualifies_strength |
| balance_direction | Nhâm |
| primary_insight | Tòng structure + output operating |
| priorities | align Thương Quan · apply Nhâm · load/recovery rhythm |
| avoidances | no ordinary DM frame · no suppress expression · no overexertion |
| unresolved | qualified:follow_qualifies_strength |

---

## Verdict (technical)

Pipeline PASS. Engines stable. Reasoning + feature wiring deliver the intended CASE-0002 delta.
