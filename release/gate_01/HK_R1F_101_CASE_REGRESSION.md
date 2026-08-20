# HK-R1F — 101-case regression

**Date:** 2026-08-20  
**Input:** `tests/golden_dataset/inputs` (n=101). **Golden expected files were not edited.**  
**Pipeline:** Calendar → BaZi → Strength → Temperature overlay → Pattern → Useful God → `build_useful_god_view`.  
**Before (HK-R1):** customer Hỷ = engine `favorable_display` (exact Dụng repeated).  
**After:** customer Hỷ = exact-Dụng omission in `engines/useful_god_engine/presentation.py`.

---

## Required vs after

| Check | BEFORE | AFTER | Required |
|-------|-------:|------:|----------|
| Exact Dụng repeated in **customer** Hỷ | 101 | **0** | 0 |
| Internal exact Dụng still in engine Hỷ | 101 | **101** | keep |
| Same-element, different stem/Ten God remainder | 27 | **27** | preserve |
| Empty customer Hỷ | 0 | **0** | report |
| Canonical internal `favorable_gods` changed | — | **0** | 0 |
| Overall Dụng changed | — | **0** | 0 |
| Kỵ changed | — | **0** | 0 |
| Customer role list still contains exact Dụng | 101 | **0** | 0 |

Empty-state string `Chưa có Hỷ thần bổ trợ riêng`: **0 / 101**. Implemented for future `[Dụng only]` rows.

---

## Overall winner distribution (unchanged vs PAT-R1F)

| Rule | n |
|------|--:|
| `str_003` | 45 |
| `str_005` | 29 |
| `str_002` | 15 |
| `str_004` | 7 |
| `spc_001` | 3 |
| `str_001` | 1 |
| `spc_003` | 1 |
| `spc_002` / `spc_004` / climate Overall | 0 |

---

## Control cases

Births: `Asia/Bangkok`. Internal favorable set is engine truth. Customer Hỷ is presentation only. Kỵ is winner-row, unchanged.

| Person | Dụng | Internal favorable | Customer Hỷ | Kỵ |
|--------|------|--------------------|-------------|-----|
| Nguyễn Tiến Sơn · 1987-01-21 04:30 male | `str_003` Hỏa · Đinh · Chính Quan | Chính Quan, Thực Thần → Hỏa · Đinh · Chính Quan / Thủy · Nhâm · Thực Thần | Thủy · Nhâm · Thực Thần | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài |
| Vũ Thị Thanh Tuyền · 1984-07-13 21:01 female | `str_003` Mộc · Ất · Chính Quan | Chính Quan, Thực Thần → Mộc · Ất · Chính Quan / Kim · Canh · Thực Thần | Kim · Canh · Thực Thần | Thổ · Mậu · Tỷ Kiên / Thổ · Kỷ · Kiếp Tài |
| Cao Xuân Trường · 1989-07-21 15:45 male | `str_001` Kim · Tân · Chính Ấn | Chính Ấn, Thiên Ấn, Tỷ Kiên → Kim · Tân · Chính Ấn / Kim · Canh · Thiên Ấn / Thủy · Nhâm · Tỷ Kiên | Kim · Canh · Thiên Ấn / Thủy · Nhâm · Tỷ Kiên | Hỏa · Đinh · Chính Tài / Hỏa · Bính · Thiên Tài |
| Lưu Hoàng Sơn · 1996-11-29 17:20 male | `str_005` Mộc · Ất · Chính Tài | Chính Tài, Thực Thần → Mộc · Ất · Chính Tài / Thủy · Nhâm · Thực Thần | Thủy · Nhâm · Thực Thần | Kim · Tân · Kiếp Tài |
| Phạm Thị Huyền · 1987-09-07 02:00 female | `str_004` Kim · Tân · Thực Thần | Thực Thần, Thương Quan → Kim · Tân · Thực Thần / Kim · Canh · Thương Quan | Kim · Canh · Thương Quan | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài |
| Lương Văn Mạnh · 1987-06-29 06:00 male | `str_004` Kim · Tân · Thực Thần | same as Huyền | Kim · Canh · Thương Quan | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài |
| Ngô Đắc Dũng · 1985-09-18 08:00 male | `str_004` Thủy · Nhâm · Thực Thần | Thực Thần, Thương Quan → Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan | Thủy · Quý · Thương Quan | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài |
| Đặng Thị Dung · 1982-05-22 09:30 female | `str_001` Thủy · Nhâm · Chính Ấn | Chính Ấn, Thiên Ấn, Tỷ Kiên → Thủy · Nhâm · Chính Ấn / Thủy · Quý · Thiên Ấn / Mộc · Ất · Tỷ Kiên | Thủy · Quý · Thiên Ấn / Mộc · Ất · Tỷ Kiên | Thổ · Mậu · Chính Tài / Thổ · Kỷ · Thiên Tài |
| Đoàn Quang Hưng · 1981-08-29 04:30 male | `str_005` Thủy · Nhâm · Chính Tài | Chính Tài, Thực Thần → Thủy · Nhâm · Chính Tài / Kim · Tân · Thực Thần | Kim · Tân · Thực Thần | Thổ · Mậu · Kiếp Tài |
| Lương Ngọc Huỳnh · 1966-09-24 04:15 male | `str_005` Kim · Tân · Chính Tài | Chính Tài, Thực Thần → Kim · Tân · Chính Tài / Thổ · Mậu · Thực Thần | Thổ · Mậu · Thực Thần | Hỏa · Đinh · Kiếp Tài |

PO checks:

- Tuyền Overall **not** changed; customer Hỷ is Kim · Canh · Thực Thần.
- Dũng Kỵ unchanged (Canh/Tỷ Kiên, Tân/Kiếp Tài).
- Trường: exact Tân/Chính Ấn removed from customer Hỷ; remainder kept; **no Earth added to Kỵ**.
- Huyền / Mạnh: exact Tân · Thực Thần removed; Canh · Thương Quan kept; **no Fire added to Kỵ**.
- Lưu: exact Ất · Chính Tài removed; remainder kept; **no Water added to Kỵ**.
- Same-element pairs kept (Dũng Thủy Nhâm vs Quý; Trường Kim Tân vs Canh; Huyền/Mạnh Kim Tân vs Canh).

---

## Surfaces

Sơn and Dũng: View = ReportInput = presented HTML = DOCX = PDF customer Hỷ. Dụng line still prints Overall. Exact Dụng is not repeated under Hỷ.

Canonical Desktop / Full Report copy `favorable_display` (no independent filter).
