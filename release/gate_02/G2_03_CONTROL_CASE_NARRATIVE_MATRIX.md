# G2-03 — Control-case narrative matrix

**Method:** live `OrchestratorService.analyze` vs `G1_PREFINAL_CONTROL_CASES.json`, then scan `narrative_result` + interpretation + report excerpt.  
**Date:** 2026-08-20  
**Analytical expected:** 0 changes. **Observed:** MATCH 10/10.  
**Generator:** `narrative_composer_v2` · contract `pack05_narrative_result_v1`  
**Machine dump:** `release/gate_02/G2_03_NARRATIVE_PROBE.json`

In-process analyze leaves `analysis_id` / `run_id` empty (equal). HTTP Analyze copies `request_id` onto both.

| Case | Strength truth | Pattern truth | Dụng truth | Hỷ truth | Điều hậu truth | Narrative consistency | Stale phrase found? | PASS/FAIL |
|------|----------------|---------------|------------|----------|----------------|-----------------------|---------------------|-----------|
| Nguyễn Tiến Sơn | 0.87 strong | Chính Ấn / override false | Hỏa · Đinh · Chính Quan · CHẾ | insufficient | Hỏa | Strength treated as được nâng đỡ, not mỏng lực; Dụng Hỏa; no climate/Overall swap | none | **PASS** |
| Lương Ngọc Huỳnh | 0.64 balanced | Chính Tài / false | Kim · Tân · Chính Tài · BALANCED-WEALTH | insufficient | Hỏa | Balanced band; Dụng Kim; Hỷ insufficient respected | none | **PASS** |
| Đặng Thị Dung | 0.24 weak | Sát Ấn… / false | Thủy · Nhâm · Chính Ấn · SINH/TRỢ | **supported** Mộc · Ất · Tỷ Kiên | Thủy | Weak → mỏng lực allowed; Dụng Thủy; Hỷ Mộc present | none (typo Than→Thân sanitized) | **PASS** |
| Đoàn Quang Hưng | 0.61 balanced | Thực Thần / false | Thủy · Nhâm · Chính Tài · BALANCED-WEALTH | insufficient | Hỏa | Balanced; Dụng Thủy; Hỷ insufficient | none | **PASS** |
| Vũ Thị Thanh Tuyền | 0.66 strong | Kiếp Tài / false | Mộc · Ất · Chính Quan · CHẾ | insufficient | Thủy | No Tòng Tài; no cực nhược; Dụng Mộc not Nhâm | none | **PASS** |
| Cao Xuân Trường | 0.34 weak | Quan Ấn… / false | Kim · Tân · Chính Ấn · SINH/TRỢ | Thủy · Nhâm · Tỷ Kiên | Thủy | Weak, not cực nhược; Dụng Kim; no extra Earth Kỵ invented | none | **PASS** |
| Lưu Hoàng Sơn | 0.51 balanced | Sát Ấn… / false | Mộc · Ất · Chính Tài | insufficient | Hỏa (climate) | Overall stays Mộc; climate Hỏa not switched in as Dụng | none | **PASS** |
| Phạm Thị Huyền | 0.74 strong | Thương Quan / false | Kim · Tân · Thực Thần · TIẾT | insufficient | Hỏa | TIẾT winner Kim; no old Mộc/Thủy Overall | none | **PASS** |
| Lương Văn Mạnh | 1.00 strong | LEVEL-1 Giá Vượng / **false** | Kim · Tân · Thực Thần · TIẾT | insufficient | Thủy | Detected wording only; not chuyên cách Dụng; Hỷ insufficient | none | **PASS** |
| Ngô Đắc Dũng | 1.00 strong | LEVEL-1 Giá Sắc / **false** | Thủy · Nhâm · Thực Thần · TIẾT | insufficient | Hỏa / Cần ôn ấm | No Thổ/Mậu/Thiên Ấn Overall; no Ấn override; Hỷ not Quý; Hỏa is Điều hậu not Overall | none | **PASS** |

## Primary case notes — Ngô Đắc Dũng

Forbidden remnants searched in live narrative blob: `Thổ · Mậu · Thiên Ấn`, `Chuyên cách ưu tiên Ấn`, definite Hỷ Quý/Thủy, `Hỏa chính là Overall`, old season Overall. **None found.**

Reasoning remains HK-R1H: Canh Kim strong → Tiết → Kim sinh Thủy → Nhâm = Thực Thần.

## Secondary case notes — Tuyền

Live pattern `Kiếp Tài`. No `Tòng Tài`, no `cực nhược`, Overall remains `Mộc · Ất · Chính Quan`.

## Section order (frozen production equivalent)

Tóm tắt điều hành → Quan sát → Lý giải → Tác động → Khuyến nghị → Lưu ý → Kết luận.

Pack 04/05 architecture was not redesigned.
