# HK-R1H — Customer Hỷ element separation

**Date:** 2026-08-20  
**Scope:** Customer presentation only.  
**Not in scope:** Overall winner, CSV, Kỵ algorithm, Golden, G1-PREFINAL / G1-FINAL.

## Status

**HK-R1H: CUSTOMER HỶ ROLE + DỤNG REASONING BINDING REPAIRED — V1.0 CUSTOMER SEMANTIC FREEZE READY**

Do **not** start G1-PREFINAL. Do **not** update Golden.

---

## Defect A — Dũng same-element Hỷ

After HK-R1G, customer Hỷ for Ngô Đắc Dũng was:

`Thủy · Quý · Thương Quan`

That is no longer an exact Dụng duplicate, but it is the **same element** as Overall Dụng (`Thủy · Nhâm · Thực Thần`) and exists only because `str_004` statically groups Output Ten Gods.

V1.0 does **not** treat that sibling grouping as an independently justified Hỷ thần.

### After

| Surface | Customer Hỷ |
|---------|-------------|
| API View `@1.5` | `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng` |
| Report V1 HTML / PDF / DOCX | same |
| Portal Result / Full Report | copies published `favorable_display` |

Internal `favorable_gods` remains `Thực Thần, Thương Quan`. Canonical engine display still includes Nhâm + Quý.

---

## Customer Hỷ policy (HK-R1H)

Start from HK-R1G leftover (exact Dụng already omitted). Classify each remainder:

| Class | Meaning | Customer |
|-------|---------|----------|
| `SUPPORTED_INDEPENDENT_ROLE` | Documented independent support (V1.0: Tỷ/Kiếp on SINH/TRỢ only) | display |
| `STATIC_SAME_ELEMENT_SIBLING` | Same element as Dụng, winner-row family sibling | neutral |
| `STATIC_OTHER` | CSV leftover without independent role | neutral |
| `UNKNOWN` | Missing identity | neutral |

Neutral wording (all surfaces):

**Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng**

Not implemented: “Hỷ must always have a different element from Dụng.”

Same-element Hỷ is allowed **only** with independent canonical evidence. Current V1.0 knowledge does **not** give Output/Resource/Wealth/Officer siblings that evidence. Peer Tỷ/Kiếp on a weak SINH/TRỢ path remains the only published independent remainder.

---

## Dũng expected vs live (fresh Analyze after restart)

| Field | Value |
|-------|--------|
| Dụng | Thủy · Nhâm · Thực Thần |
| Căn cứ | Canh Kim thân vượng → tiết bớt khí Kim → Tiết → Kim sinh Thủy → Nhâm đối với Canh là Thực Thần |
| Customer Hỷ | Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng |
| Hỷ status | `STATIC_SAME_ELEMENT_SIBLING` |
| Kỵ | Kim · Canh · Tỷ Kiên / Kim · Tân · Kiếp Tài (unchanged) |
| Điều hậu | Hỏa · Đinh · Chính Quan · Cần ôn ấm · ưu tiên Hỏa (separate) |

PASS: customer does not show Dụng=Thủy and Hỷ=Thủy.

---

## Files

| File | Change |
|------|--------|
| `engines/useful_god_engine/presentation.py` | same-element sibling is not independent Hỷ; new wording |
| `engines/useful_god_engine/reasoning.py` | TIẾT / CHẾ chain wording |
| `applications/api/services/useful_god_truth.py` | View `@1.5` |
| Portal S02 / Result / Full Report | Dụng/Hỷ/Kỵ row + full-width Căn cứ |
| Report section 07 | same card; climate display row |

**Not changed:** Strength, Pattern, Useful God CSV, engine `favorable_gods`, Kỵ lists, climate winner, Golden.

---

**HK-R1H: CUSTOMER HỶ ROLE + DỤNG REASONING BINDING REPAIRED — V1.0 CUSTOMER SEMANTIC FREEZE READY**
