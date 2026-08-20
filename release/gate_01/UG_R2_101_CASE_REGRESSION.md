# UG-R2 — 101-case regression (live recompute)

**Date:** 2026-08-20  
**Input set:** `tests/golden_dataset/inputs` (n=101). **Golden expected files were not edited.**  
**Pipeline:** `OrchestratorService.analyze` (production Strength → Temperature overlay → Pattern → Useful God).

---

## Overall winner groups

| Group | Count | Role |
|-------|------:|------|
| `strength` | 89 | Overall Dụng thần |
| `special` | 12 | Overall Dụng thần (follow/special override) |
| `season` | **0** | must not win Overall after UG-R2 |
| `temperature` | **0** | must not win Overall after UG-R2 |
| `flow` | 0 | structural candidate only; never beat Strength |
| incomplete / no-result | **0** | |

Architectural property holds: **season and pure climate temperature do not appear as Overall winner groups.**

### Overall rule IDs

| Rule | Count | Layer |
|------|------:|-------|
| `str_004` | 29 | overall / strong drain |
| `str_005` | 29 | overall / balanced wealth |
| `str_003` | 15 | overall / strong Chính Quan |
| `str_002` | 15 | overall / weak Thiên Ấn fallback |
| `str_001` | 1 | overall / weak Chính Ấn |
| `spc_004` | 8 | overall / special Ấn |
| `spc_001` | 3 | overall / Tòng Tài |
| `spc_003` | 1 | overall / Tòng Sát |

---

## Climate recommendations (separate)

| Group | Count |
|-------|------:|
| `season` | 82 |
| `temperature` | 19 |
| none | 0 |

Every chart still received a Điều hậu climate candidate. Climate IDs:

| Rule | Count |
|------|------:|
| `sea_001` | 28 |
| `sea_002` | 23 |
| `sea_004` | 17 |
| `sea_003` | 14 |
| `tmp_004` | 13 |
| `tmp_003` | 6 |

Season still dominates the **climate** layer (priority 90 vs 70). That is correct for Điều hậu, not Overall.

---

## No-result cases

**None.** Strength rules cover `weak | strong | balanced`, so after removing climate from Overall every chart still had a structural winner.

Policy remains: if a future chart has no structural candidate, publish `Chưa đủ căn cứ xác định Dụng thần tổng thể` — do not fall back to climate.

---

## Special Overall winners (12)

| Case | Rule | Display | Pattern | Strength |
|------|------|---------|---------|----------|
| case_0015 | `spc_004` | Mộc · Ất · Thiên Ấn | `viem_thuong` | strong |
| case_0021 | `spc_001` | Kim · Canh · Chính Tài | `tong_tai` | weak |
| case_0022 | `spc_004` | Thủy · Quý · Thiên Ấn | `khuc_truc` | strong |
| case_0032 | `spc_004` | Thủy · Nhâm · Thiên Ấn | `khuc_truc` | strong |
| case_0057 | `spc_004` | Thổ · Mậu · Thiên Ấn | `gia_sac` | strong |
| case_0059 | `spc_004` | Kim · Canh · Thiên Ấn | `nhuan_ha` | strong |
| case_0073 | `spc_001` | Hỏa · Đinh · Chính Tài | `tong_tai` | weak |
| case_0077 | `spc_004` | Thổ · Mậu · Thiên Ấn | `gia_sac` | strong |
| case_0084 | `spc_004` | Mộc · Giáp · Thiên Ấn | `viem_thuong` | strong |
| case_0087 | `spc_004` | Thổ · Kỷ · Thiên Ấn | `gia_sac` | strong |
| case_0093 | `spc_003` | Thổ · Kỷ · Thất Sát | `tong_sat` | weak |
| case_0095 | `spc_001` | Thổ · Kỷ · Chính Tài | `tong_tai` | weak |

---

## Control five (same live pipeline)

See `UG_R2_USEFUL_GOD_RECONCILIATION_REPAIR_REPORT.md` §8. All five left season Overall winners. Tuyền Overall = `str_004` Kim · Canh · Thực Thần; Điều hậu remains `sea_002` Thủy.
