# UG-R2 — Useful God Reconciliation Repair Report

**Date:** 2026-08-20  
**Gate:** GATE 1 / UG-R2  
**Does not start G1-FINAL.**  
**Did not lower `sea_*` CSV priority. Did not hard-code Mộc for Vũ Thị Thanh Tuyền. Did not add missing theory.**

## Status

**`UG-R2: ARCHITECTURE REPAIRED — KNOWLEDGE COVERAGE REVIEW REQUIRED`**

Điều hậu / climate is separated from Overall Dụng thần. Season and temperature no longer win Overall on the 101-case live set. Strength is the primary structural Overall source. Material V1.0 knowledge gaps remain (Pattern tokens, strong-Earth Mộc/Thất Sát control, strong wealth path).

---

## 1. Architecture repair

Two layers after matching, before `PriorityResolver`:

| Layer | Groups | Output | May win Overall? |
|-------|--------|--------|------------------|
| **Điều hậu / climate** | `season`, `temperature` | `climate_*` | **No** |
| **Overall Dụng thần** | `strength`, `flow`, `special` | `useful_god` / `winning_rule_*` | Yes |

`sea_*` and `tmp_*` still match and keep evidence. They rank **within climate only** (season group 90 still beats temperature 70 for Điều hậu). They are not Overall candidates.

If Overall has no structural winner: **no climate fallback**.

- `overall_incomplete = true`
- `useful_display` / `error` = `Chưa đủ căn cứ xác định Dụng thần tổng thể`
- Hỷ/Kỵ stay empty (not copied from climate)

Backward compatible keys: `useful_god`, `useful_display`, `winning_rule_id` remain **Overall**. New climate keys are additive. API contract `analysis_result.UsefulGodView@1.2`.

---

## 2. Temperature vs season (Điều hậu)

Both encode hot/cold (or season-phase) climate adjustment. They are **deduplicated as Overall competitors** by routing both into the climate layer. Distinct evidence is preserved:

| Source | Knows | Example |
|--------|-------|---------|
| `sea_002` | `summer` + `hot` | Nhâm |
| `tmp_002` | `hot` only | Quý |

Climate winner is still `max(group_priority, score, rule_priority)` inside that layer.

---

## 3. Vũ Thị Thanh Tuyền — re-evaluation

Upstream unchanged: Giáp Tý / Tân Mùi / Mậu Thân / Quý Hợi · Mậu · Strength `0.66 strong` · Pattern `kiep_tai` / Kiếp Tài · Climate Nhiệt · Cần làm mát · G1-05 Mộc3 Hỏa1 Thổ4 Kim3 Thủy6.

| Layer | Rule | Display | Hỷ / Kỵ |
|-------|------|---------|---------|
| **Điều hậu** | `sea_002` (climate) | Thủy · Nhâm · Thiên Tài | *not used for Overall* |
| Climate also matched | `tmp_002` | Quý | evidence only |
| **Overall** | `str_004` | **Kim · Canh · Thực Thần** | Thực Thần / Thương Quan vs Tỷ Kiên / Kiếp Tài |
| Structural also matched | `flo_004` | Mậu | loses to strength 80 > flow 60 |

Overall is **not** Mộc. Overall is **not** Thủy. Structural rules decided **drain/output** (`Thực Thần` → Canh / Kim for Mậu).

Hỷ/Kỵ come from `str_004`, not from `sea_002` (`Nhâm/Quý/Canh` vs `Bính/Đinh`).

---

## 4. Mộc coverage (item 10)

**`V1.0 KNOWLEDGE GAP — PRODUCT OWNER DECISION REQUIRED`**

No reachable Mộc / Giáp / Ất Overall path for this strong Mậu configuration.

| Asset | Fact |
|-------|------|
| Production `str_003` | Control candidate is **Chính Quan** only (`officer_elements contains Chính Quan`) |
| Tuyền `officer_elements` | `['Thất Sát']` (Giáp). Rule does **not** match. Implementation is reachable; the condition is unmatched. |
| Production CSV | No Thất Sát-as-control, no Wood-to-control-Earth row |
| Knowledge pack `bz_07` / `cand_ug_officer_strong` | Chính Quan for strong, **not wired** to production (UG-R1). Wiring it would be a new pipeline, not a reachability bug. |
| Pattern `kiep_tai` | No Useful God rule reads `main_pattern` |

Did **not** add a Mộc rule.

---

## 5. Pattern reconciliation

Canonical Pattern participates **only** where a Useful God rule reads follow/special tokens (G1-X01 still mandatory).

| Pattern token class | UG coverage |
|---------------------|-------------|
| Main (`chinh_an`, `chinh_tai`, `kiep_tai`, `thuc_than`, `that_sat`, …) | **None** |
| Combination (`sat_an`, `quan_an`, …) | **None** |
| Follow `tong_tai` / `tong_quan` / `tong_sat` | `spc_001`–`spc_003` when winner is that follow rule |
| Follow `tong_vuong` / `tong_nhi` / `tong_an` | **Gap** |
| Special `khuc_truc`, `viem_thuong`, `nhuan_ha`, `gia_sac` | `spc_004` → Thiên Ấn |
| Special `jia_wang` | **Gap** (`spc_004` list omits it) |

Tuyền `kiep_tai` has **no** pattern-specific Overall rule.

---

## 6. Flow (G1-06)

G1-06 unique-max `contains` is unchanged. Flow remains an Overall *structural* group (priority 60).

**Limitation (not promoted):** unique-max **occurrence** is not element excess / vượng suy. With Strength always populated, flow **cannot win Overall** (60 < 80). Tuyền `flo_004` still matches because engine dist Thủy is unique max; it is a losing Overall candidate only.

---

## 7. Hỷ / Kỵ and presentation

| Customer field | Source |
|----------------|--------|
| Dụng thần | Overall `useful_display` |
| Hỷ thần / Kỵ thần | Overall winner row |
| Điều hậu | G1-04 climate + balancing need |
| Optional | `Điều hậu ưu tiên {element}` from climate winner |

Đặng Thị Dung: Overall `str_001` and climate `sea_002` both **display** `Thủy · Nhâm · Chính Ấn` (Ất × Nhâm = Chính Ấn). Rule IDs differ. This is coincidence, not collapse.

Five Elements disclaimer (counts unchanged):

> Phân bố Ngũ hành phản ánh số lần xuất hiện trong cấu trúc, không phải mức vượng suy và không trực tiếp quyết định Dụng thần.

Applied: API `five_elements.disclaimer` · Result/Desktop S04 · Full Report · HTML/PDF/DOCX notes.

---

## 8. Control cases

| Case | Strength | Pattern | Điều hậu | Old Overall Dụng | New Overall Dụng | Winning structural rule |
|------|----------|---------|----------|------------------|------------------|-------------------------|
| Nguyễn Tiến Sơn | 0.87 strong | Chính Ấn | Hàn · Cần ôn ấm · ưu tiên Hỏa (`sea_001`) | Hỏa · Bính · Thất Sát (`sea_001`) | Thủy · Nhâm · Thực Thần | `str_004` |
| Lương Ngọc Huỳnh | 0.64 balanced | Chính Tài | Lương · Cần ôn ấm · ưu tiên Hỏa (`sea_004`) | Hỏa · Đinh · Kiếp Tài (`sea_004`) | Kim · Tân · Chính Tài | `str_005` |
| Đặng Thị Dung | 0.24 weak | Sát Ấn tương sinh | Nhiệt · Cần làm mát · ưu tiên Thủy (`sea_002`) | Thủy · Nhâm · Chính Ấn (`sea_002`) | Thủy · Nhâm · Chính Ấn | `str_001` |
| Đoàn Quang Hưng | 0.61 balanced | Thực Thần | Lương · Cần ôn ấm · ưu tiên Hỏa (`sea_004`) | Hỏa · Đinh · Thiên Ấn (`sea_004`) | Thủy · Nhâm · Chính Tài | `str_005` |
| Vũ Thị Thanh Tuyền | 0.66 strong | Kiếp Tài | Nhiệt · Cần làm mát · ưu tiên Thủy (`sea_002`) | Thủy · Nhâm · Thiên Tài (`sea_002`) | Kim · Canh · Thực Thần | `str_004` |

Old season Overall winners were **not** preserved for compatibility.

---

## 9. Invariants

1. Điều hậu ≠ Overall Dụng by default (separate fields; Dung display may coincide).  
2. Climate cannot automatically win Overall.  
3. Strength scores/class unchanged.  
4. Pattern remains canonical (G1-X01).  
5. Follow compatibility unchanged.  
6. G1-05 counts unchanged; disclaimer added.  
7. Hỷ/Kỵ from Overall row.  
8. No hidden season fallback.  
9. Same Overall/climate payload on API → Portal → Report/PDF/DOCX.

---

## 10. Files changed (implementation)

- `engines/useful_god_engine/layers.py` (new)
- `engines/useful_god_engine/engine.py`, `models.py`, `roles.py`
- `applications/api/models/analysis_result.py`, `services/useful_god_truth.py`, `services/five_elements_truth.py`
- `applications/production/interpretation/useful_god_composer.py` (incomplete Overall is not a balancing god name)
- `engines/report_engine/contracts/report_input_v1.py`, `adapters/report_input_v1_adapter.py`, `rendering/report_sections_v1.py`
- Portal: `canonicalUsefulGod.ts`, `canonicalFiveElements.ts`, `canonicalDesktopAdapter.ts`, `fullReportViewModel.ts`, `liveAnalysisResultAdapter.ts`
- Tests encoding old Overall=season SSOT (not Golden Dataset files)

CSV priorities and season/temperature **rows were not deleted**.
