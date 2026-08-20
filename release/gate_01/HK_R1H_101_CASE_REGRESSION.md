# HK-R1H — 101-case customer semantic regression

**Date:** 2026-08-20  
**Input:** `tests/golden_dataset/inputs` (n=101). Golden **not** edited.  
**Pipeline:** Calendar → BaZi → Strength → Temperature → Pattern → Useful God → `build_useful_god_view`.

Control births are the Product Owner set (not all ten sit in Golden by date). They were run with the same orchestrator as live Analyze.

---

## Required vs after

| Check | AFTER | Required |
|-------|------:|----------|
| A. Exact Dụng in customer Hỷ | **0** | 0 |
| B. Same-element unsupported Hỷ displayed | **0** | 0 |
| C. Different-element unsupported Hỷ displayed | **0** | 0 |
| D. Supported independent Hỷ displayed (cases) | **16** | count |
| E. Neutral Hỷ state (cases) | **85** | count |
| F. Overall Dụng changed | **0** | 0 |
| G. Internal `favorable_gods` changed | **0** | 0 |
| H. Kỵ changed | **0** | 0 |
| I. Reasoning chain missing | **0** | 0 |
| Reasoning contains `str_*` / `spc_*` | **0** | 0 |

### Leftover entries after exact-Dụng omit

| Class | Entries |
|-------|--------:|
| SUPPORTED_INDEPENDENT_ROLE | **16** |
| STATIC_SAME_ELEMENT_SIBLING | **27** |
| STATIC_OTHER | **74** |
| UNKNOWN | **0** |

16 independent cases + 85 neutral = 101. The 16 independent remainders are Tỷ/Kiếp on SINH/TRỢ paths (different element from Ấn Dụng). The 27 same-element Output/Resource siblings are no longer published as Hỷ.

---

## Control cases

| Case | Strength | Overall Dụng | Archetype | Customer reasoning | Internal favorable | Customer Hỷ | Hỷ evidence | Kỵ | Điều hậu |
|------|----------|--------------|-----------|--------------------|--------------------|-------------|-------------|-----|----------|
| Nguyễn Tiến Sơn | 0.87 strong | Hỏa · Đinh · Chính Quan | CHẾ | Canh Kim vượng → Chính Quan đủ điều kiện Chế → Hỏa khắc Kim → Đinh = Chính Quan | CQ, Thực Thần | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_OTHER | Canh/Tỷ, Tân/Kiếp | Hỏa · Bính · Thất Sát / ưu tiên Hỏa |
| Vũ Thị Thanh Tuyền | 0.66 strong | Mộc · Ất · Chính Quan | CHẾ | Mậu Thổ vượng → Chính Quan đủ điều kiện Chế → Mộc khắc Thổ → Ất = Chính Quan | CQ, Thực Thần | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_OTHER | Mậu/Tỷ, Kỷ/Kiếp | Thủy · Nhâm · Thiên Tài / ưu tiên Thủy |
| Cao Xuân Trường | 0.34 weak | Kim · Tân · Chính Ấn | SINH / TRỢ | Nhâm Thủy nhược → Sinh/Trợ → Kim sinh Thủy → Tân = Chính Ấn | Ấn, Thiên Ấn, Tỷ | **Thủy · Nhâm · Tỷ Kiên** (Canh Thiên Ấn suppressed) | SUPPORTED_INDEPENDENT + STATIC_SAME_ELEMENT sibling leftover | Fire Tài | Thủy / ưu tiên Thủy |
| Lưu Hoàng Sơn | 0.51 balanced | Mộc · Ất · Chính Tài | BALANCED-WEALTH | Canh trung hòa → Tài lưu thông (không đối chiếu sâu toàn cục) → Kim khắc Mộc → Ất = Chính Tài | Tài, Thực Thần | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_OTHER | Tân/Kiếp | Hỏa / ưu tiên Hỏa |
| Phạm Thị Huyền | 0.74 strong | Kim · Tân · Thực Thần | TIẾT | Kỷ Thổ vượng → tiết bớt khí Thổ → Thổ sinh Kim → Tân = Thực Thần | Thực, Thương | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_SAME_ELEMENT_SIBLING | Earth peers | Hỏa · Đinh · Thiên Ấn / ưu tiên Hỏa |
| Lương Văn Mạnh | 1.00 strong | Kim · Tân · Thực Thần | TIẾT | same class as Huyền | Thực, Thương | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_SAME_ELEMENT_SIBLING | Earth peers | Thủy / ưu tiên Thủy |
| Ngô Đắc Dũng | 1.00 strong | Thủy · Nhâm · Thực Thần | TIẾT | Canh Kim vượng → tiết bớt khí Kim → Kim sinh Thủy → Nhâm = Thực Thần | Thực, Thương | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_SAME_ELEMENT_SIBLING | Canh/Tỷ, Tân/Kiếp | **Hỏa · Đinh · Chính Quan / Cần ôn ấm / ưu tiên Hỏa** |
| Đặng Thị Dung | 0.24 weak | Thủy · Nhâm · Chính Ấn | SINH / TRỢ | Ất nhược → Sinh/Trợ → Thủy sinh Mộc → Nhâm = Chính Ấn | Ấn, Thiên Ấn, Tỷ | **Mộc · Ất · Tỷ Kiên** (Quý Thiên Ấn suppressed) | SUPPORTED_INDEPENDENT + STATIC_SAME_ELEMENT leftover | Earth Tài | Thủy / ưu tiên Thủy |
| Đoàn Quang Hưng | 0.61 balanced | Thủy · Nhâm · Chính Tài | BALANCED-WEALTH | Kỷ trung hòa → Tài lưu thông (không đối chiếu sâu) → Thổ khắc Thủy | Tài, Thực Thần | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_OTHER | Mậu/Kiếp | Hỏa / ưu tiên Hỏa |
| Lương Ngọc Huỳnh | 0.64 balanced | Kim · Tân · Chính Tài | BALANCED-WEALTH | Bính trung hòa → Tài lưu thông (không đối chiếu sâu) → Hỏa khắc Kim | Tài, Thực Thần | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng | STATIC_OTHER | Đinh/Kiếp | Hỏa / ưu tiên Hỏa |

Overall Dụng, internal favorable, and Kỵ match the frozen HK-R1G values. Customer Hỷ no longer publishes Quý/Thủy or Canh/Thương Quan as justified Hỷ.

---

## Live Dũng (API PID 11296, fresh POST `/api/v1/analyze`)

```
useful_display: Thủy · Nhâm · Thực Thần
favorable_display: Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng
canonical_favorable_display: Thủy · Nhâm · Thực Thần / Thủy · Quý · Thương Quan
short_reason: …Tiết… Kim sinh Thủy… Nhâm đối với Canh là Thực Thần…
unfavorable_display: Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài
climate_display: Hỏa · Đinh · Chính Quan
```

Report V1 HTML checks: Dụng, Căn cứ label, Tiết chain, neutral Hỷ, no Quý under Hỷ, no `str_004`, Cần ôn ấm, Hỏa · Đinh · Chính Quan — all true. PDF 155 KB / DOCX 38 KB from the same input.
