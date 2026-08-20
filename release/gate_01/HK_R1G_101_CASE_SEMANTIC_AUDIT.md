# HK-R1G — 101-case semantic audit

**Date:** 2026-08-20  
**Input:** `tests/golden_dataset/inputs` (n=101). **Golden expected files were not edited.**  
**Pipeline:** Calendar → BaZi → Strength → Temperature overlay → Pattern → Useful God → `build_useful_god_view`.

Compared with HK-R1F:

- Internal `favorable_gods` / engine `favorable_display` / Overall Dụng / Kỵ **unchanged**.
- Customer Hỷ adds an independent-role gate after exact-Dụng omit.
- Every Overall Dụng now publishes a customer reasoning chain (no rule IDs).

---

## Required vs after

| Check | AFTER | Required |
|-------|------:|----------|
| Exact Dụng in **customer** Hỷ | **0** | 0 |
| Overall Dụng changed | **0** | 0 |
| Internal `favorable_gods` changed | **0** | 0 |
| Kỵ changed | **0** | 0 |

### Remaining Hỷ after exact-Dụng omit, by role

Counts are leftover **entries** (a case may have more than one leftover).

| Class | Entry count | Customer treatment |
|-------|------------:|--------------------|
| SUPPORTED_ROLE | **43** | displayed |
| STATIC_FAVORABLE_ONLY | **74** | not displayed as a justified Hỷ thần |
| UNKNOWN | **0** | — |

| Case-level | n |
|------------|--:|
| Customer insufficient Hỷ (`Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng`) | **74** |
| Customer displayed Hỷ (at least one SUPPORTED leftover) | **27** |
| Same-element Dụng/Hỷ remainder that is SUPPORTED_ROLE | **27** |
| Empty remainder after exact omit (`Chưa có Hỷ thần bổ trợ riêng`) | **0** |

Same-element remainders are **not** hidden by a UI rule. They stay only when published Ten God sibling (or weak-path peer) knowledge supports an independent role.

---

## Archetype distribution (Overall winners unchanged vs PAT-R1F / HK-R1F)

| Archetype | n | Rules |
|-----------|--:|-------|
| CHẾ | 45 | `str_003` |
| BALANCED-WEALTH | 29 | `str_005` |
| SINH / TRỢ | 16 | `str_001` (1) + `str_002` (15) |
| TIẾT | 7 | `str_004` |
| FOLLOW / SPECIAL | 4 | `spc_001`×3 + `spc_003`×1 |

`spc_002` / `spc_004` Overall: **0**. Climate never becomes Overall.

---

## Control cases

Births: `Asia/Bangkok`. Internal favorable is engine truth. Customer Hỷ is presentation only. Kỵ is winner-row, unchanged.

| Person | Dụng | Archetype | Short reasoning chain | Internal favorable | Customer Hỷ | Hỷ class | Kỵ |
|--------|------|-----------|----------------------|--------------------|-------------|----------|-----|
| Nguyễn Tiến Sơn · 1987-01-21 04:30 male | Hỏa · Đinh · Chính Quan (`str_003`) | CHẾ | Canh Kim thân vượng → chế ước → Chế theo mô hình cân bằng V1.0 → Hỏa khắc Kim → Đinh = Chính Quan | Chính Quan, Thực Thần → Hỏa · Đinh · Chính Quan / Thủy · Nhâm · Thực Thần | Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng | STATIC_FAVORABLE_ONLY | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài |
| Vũ Thị Thanh Tuyền · 1984-07-13 21:01 female | Mộc · Ất · Chính Quan (`str_003`) | CHẾ | Mậu Thổ thân vượng → chế ước → Chế → Mộc khắc Thổ → Ất = Chính Quan | Chính Quan, Thực Thần → Mộc · Ất · Chính Quan / Kim · Canh · Thực Thần | Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng | STATIC_FAVORABLE_ONLY | Thổ · Mậu · Tỷ Kiên / Thổ · Kỷ · Kiếp Tài |
| Cao Xuân Trường · 1989-07-21 15:45 male | Kim · Tân · Chính Ấn (`str_001`) | SINH / TRỢ | Nhâm Thủy thân nhược → sinh trợ → Sinh / Trợ → Kim sinh Thủy → Tân = Chính Ấn | Chính Ấn, Thiên Ấn, Tỷ Kiên → Kim · Tân · Chính Ấn / Kim · Canh · Thiên Ấn / Thủy · Nhâm · Tỷ Kiên | Kim · Canh · Thiên Ấn / Thủy · Nhâm · Tỷ Kiên | SUPPORTED_ROLE ×2 | Hỏa · Đinh · Chính Tài / Hỏa · Bính · Thiên Tài |
| Lưu Hoàng Sơn · 1996-11-29 17:20 male | Mộc · Ất · Chính Tài (`str_005`) | BALANCED-WEALTH | Canh Kim thân trung hòa → lưu thông → Tài lưu thông (không đối chiếu sâu toàn cục) → Kim khắc Mộc → Ất = Chính Tài | Chính Tài, Thực Thần → Mộc · Ất · Chính Tài / Thủy · Nhâm · Thực Thần | Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng | STATIC_FAVORABLE_ONLY | Kim · Tân · Kiếp Tài |
| Phạm Thị Huyền · 1987-09-07 02:00 female | Kim · Tân · Thực Thần (`str_004`) | TIẾT | Kỷ Thổ thân vượng → tiết khí → Tiết → Thổ sinh Kim → Tân = Thực Thần | Thực Thần, Thương Quan → Kim · Tân · Thực Thần / Kim · Canh · Thương Quan | Kim · Canh · Thương Quan | SUPPORTED_ROLE | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài |
| Lương Văn Mạnh · 1987-06-29 06:00 male | Kim · Tân · Thực Thần (`str_004`) | TIẾT | Same class as Huyền | Thực Thần, Thương Quan | Kim · Canh · Thương Quan | SUPPORTED_ROLE | Thổ · Kỷ · Tỷ Kiên / Thổ · Mậu · Kiếp Tài |
| Ngô Đắc Dũng · 1985-09-18 08:00 male | Thủy · Nhâm · Thực Thần (`str_004`) | TIẾT | Canh Kim thân vượng → tiết khí → Tiết → Kim sinh Thủy → Nhâm = Thực Thần | Thực Thần, Thương Quan → Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan | Thủy · Quý · Thương Quan | SUPPORTED_ROLE | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài |
| Đặng Thị Dung · 1982-05-22 09:30 female | Thủy · Nhâm · Chính Ấn (`str_001`) | SINH / TRỢ | Ất Mộc thân nhược → sinh trợ → Sinh / Trợ → Thủy sinh Mộc → Nhâm = Chính Ấn | Chính Ấn, Thiên Ấn, Tỷ Kiên | Thủy · Quý · Thiên Ấn / Mộc · Ất · Tỷ Kiên | SUPPORTED_ROLE ×2 | Thổ · Mậu · Chính Tài / Thổ · Kỷ · Thiên Tài |
| Đoàn Quang Hưng · 1981-08-29 04:30 male | Thủy · Nhâm · Chính Tài (`str_005`) | BALANCED-WEALTH | Kỷ Thổ thân trung hòa → Tài lưu thông (không đối chiếu sâu toàn cục) → Thổ khắc Thủy → Nhâm = Chính Tài | Chính Tài, Thực Thần → Thủy · Nhâm · Chính Tài / Kim · Tân · Thực Thần | Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng | STATIC_FAVORABLE_ONLY | Thổ · Mậu · Kiếp Tài |
| Lương Ngọc Huỳnh · 1966-09-24 04:15 male | Kim · Tân · Chính Tài (`str_005`) | BALANCED-WEALTH | Bính Hỏa thân trung hòa → Tài lưu thông (không đối chiếu sâu toàn cục) → Hỏa khắc Kim → Tân = Chính Tài | Chính Tài, Thực Thần → Kim · Tân · Chính Tài / Thổ · Mậu · Thực Thần | Chưa đủ căn cứ tách Hỷ thần bổ trợ riêng | STATIC_FAVORABLE_ONLY | Hỏa · Đinh · Kiếp Tài |

### Product Owner checks

- **Dũng:** Overall unchanged. Exact Nhâm duplicate **removed** from customer Hỷ. Remaining Quý / Thương Quan is **SUPPORTED_ROLE** because `output_role` documents Thực Thần ↔ Thương Quan as the same Output channel. Same-element Thủy is allowed here because that sibling relation exists; it is not “another Water because Dụng is Water.”
- **Tuyền:** Overall unchanged (Ất / Mộc / Chính Quan). Remaining Canh / Thực Thần is **STATIC_FAVORABLE_ONLY**. No published concept that Output independently supports Officer Dụng. Customer Hỷ is the insufficient state — not a confident Hỷ thần.
- **Sơn / Hưng / Huỳnh (`str_005`):** Customer wording states the current V1.0 model uses Tài lưu thông and **does not deep-reconcile** the whole chart. Remaining Thực Thần leftover is STATIC.
- **Trường:** Strength / Dụng unchanged. Customer Hỷ keeps Thiên Ấn (resource sibling) and Tỷ Kiên (peer support on SINH / TRỢ). Kỵ remains Fire Tài; **no Earth added**.
- **Huyền / Mạnh:** exact Tân · Thực Thần omitted; Canh · Thương Quan kept as Output sibling. **No Fire added to Kỵ.**
- Climate / Điều hậu is not merged into Overall on any control case.

---

## Dũng same-element Hỷ (item 10)

| Item | Value |
|------|--------|
| Dụng | Nhâm / Thực Thần / Thủy |
| Remaining favorable | Quý / Thương Quan / Thủy |
| Canonical independent role? | **Yes** — sibling Output (`output_role`: Thực Thần / Thương Quan) |
| Customer | Display `Thủy · Quý · Thương Quan` |
| Blind hide-by-element? | **Not applied** |

There is **no** canonical knowledge that Quý is a distinct Hỷ *because it is Water*. The displayed role is the Ten God sibling of the Tiết path, not a second Water Dụng.

---

## Surfaces (fresh Analyze, not ResultStore)

Sơn and Dũng: View = ReportInput = presented HTML = DOCX = PDF customer Hỷ. Dụng line still prints Overall. Exact Dụng is not repeated under Hỷ. **Căn cứ chọn Dụng** is the published `short_reason`. Kỵ values unchanged; customer qualifier `Kỵ thần theo rule cân bằng hiện tại`.

Portal Canonical Desktop S02 and Full Report copy published `favorable_display` / `short_reason` (no independent reconstruction).
