# HK-R1H — Useful God reasoning binding

**Date:** 2026-08-20  
**Scope:** Bind the existing HK-R1G reason object onto live customer cards.  
**Not in scope:** new winner theory, frontend reconstruction of why Dụng was chosen.

## Status

Reasoning object existed after HK-R1G. Live Result / Print / Full Report **did not show it as a readable Căn cứ**.

---

## Trace

```
UsefulGodEngine result
→ engines/useful_god_engine/reasoning.py  (short_reason, no rule IDs)
→ build_useful_god_view  (UsefulGodView@1.5.short_reason)
→ API /api/v1/analyze
→ ResultStore (must be a fresh Analyze)
→ Portal adapters copy short_reason only
→ ReportInputV1.short_reason
→ Report V1 HTML / PDF / DOCX section 07
```

SSOT remains `build_customer_reason`. Portal / PDF / DOCX do **not** rebuild the chain.

---

## Where the live card lost the reason

| Surface | Loss point | Proof |
|---------|------------|-------|
| **/result Core Indicators** | `resultPresentationAdapter` took `adaptPreviewList(s02.items, 6)`. After HK-R1G inserted Cách cục / Điều hậu / Căn cứ, the first six tiles were Ngũ hành → … → Dụng. **Căn cứ, Hỷ, Kỵ were dropped.** | `adaptPreviewList(..., 6)` on a 9-item list |
| **Canonical Desktop S02** | Căn cứ was a 3×2 **tile** (`font-size: 18px` bold). A 1–2 sentence chain does not fit. Visually not an explanation. | `.cd-s02__tile-value` |
| **Full Report HTML/Print** | Căn cứ sat in `.bte-full-grid` (`minmax(180px, 1fr)` with Dụng/Hỷ/Kỵ). The chain wrapped into a cramped cell. | `godsSupport()` four-cell grid |

This is **not** “cache.” The API already published `short_reason`. The presentation layout discarded or crushed it.

A stale ResultStore would also hide a later payload; live verification requires **fresh Analyze after API restart**.

---

## Repair

One published string: `useful_god.short_reason`.

| Surface | After |
|---------|--------|
| Canonical Desktop S02 | Restore 3×2: Ngũ hành / Âm dương / Thế cục / Dụng / Hỷ / Kỵ. Full-width line under the grid: **Căn cứ chọn Dụng** |
| Result | Indicators explicitly pick Dụng, Hỷ, Kỵ, Điều hậu, Thế cục, Phân bố. Full-width unclamped reason under the list |
| Full Report | 3-cell Dụng / Hỷ / Kỵ grid + full-width `<p>Căn cứ chọn Dụng: …</p>` |
| Report V1 HTML/PDF/DOCX | Existing meta row **Căn cứ chọn Dụng** (already on `short_reason`) |

---

## Dũng chain (no rule IDs)

> Nhật chủ Canh Kim thân vượng → cần tiết bớt khí Kim → áp dụng nguyên tắc Tiết theo mô hình cân bằng V1.0 → Kim sinh Thủy → Nhâm đối với Canh là Thực Thần → chọn Thủy · Nhâm · Thực Thần làm Dụng.

Does **not** claim Thủy is the only possible Dụng.

Fresh API (PID 11296) returns that `short_reason`. Report V1 HTML contains the label and the chain. PDF 155 259 bytes / DOCX 38 544 bytes generated from the same `ReportInputV1`.

---

## Climate remains separate

Dũng Report V1 rows:

- Nhu cầu điều hòa: **Cần ôn ấm**
- Ứng dụng Điều hậu: **Hỏa · Đinh · Chính Quan**
- Điều hậu ưu tiên: **Điều hậu ưu tiên Hỏa**

Not merged into Overall Dụng.
