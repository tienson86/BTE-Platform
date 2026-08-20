# HK-R1G — Refreeze checklist

**Date:** 2026-08-20  
**Gate:** Dụng reasoning chain + Hỷ independent-role semantics (V1.0)

---

## Freeze decision

- [x] Overall Useful God winner selection **not** reopened
- [x] Internal `UsefulGodResult` / `favorable_gods` / engine `favorable_display` unchanged
- [x] Customer exact-Dụng duplication = **0**
- [x] Remaining Hỷ classified SUPPORTED_ROLE / STATIC_FAVORABLE_ONLY / UNKNOWN from published concept groups only
- [x] STATIC / UNKNOWN not presented as a fully justified Hỷ thần
- [x] Same-element Hỷ **not** hidden by a blind UI rule
- [x] Every Overall Dụng publishes a customer reasoning chain (no rule IDs)
- [x] Customer wording uses **mô hình cân bằng V1.0**; does not claim the only possible Dụng
- [x] `str_005` customer reason states no deep whole-chart reconciliation
- [x] Điều hậu stays a separate climate layer (not merged into Overall)
- [x] Kỵ algorithm unchanged (winner-row only)
- [x] Customer Kỵ qualifier: `Kỵ thần theo rule cân bằng hiện tại`
- [x] Shared SSOT: `engines/useful_god_engine/reasoning.py` + `presentation.py`
- [x] Portal / Report / HTML / PDF / DOCX copy View `favorable_display` / `short_reason`
- [x] Useful God CSV / Strength / Pattern / Five Elements / Temperature / Ten Gods / ShenSha / Luck / priorities unchanged
- [x] Golden Dataset **not** updated
- [x] G1-PREFINAL / G1-FINAL **not** started

---

## 101-case live recompute

- [x] Customer exact-Dụng-in-Hỷ: 101 → **0**
- [x] Internal favorable set changed: **0**
- [x] Overall Dụng changed: **0**
- [x] Kỵ changed: **0**
- [x] SUPPORTED leftover entries: **43**
- [x] STATIC leftover entries: **74**
- [x] UNKNOWN leftover entries: **0**
- [x] Customer insufficient Hỷ cases: **74**
- [x] Same-element SUPPORTED remainder cases: **27**

---

## Control cases (fresh)

- [x] Nguyễn Tiến Sơn — CHẾ; STATIC Hỷ insufficient
- [x] Vũ Thị Thanh Tuyền — CHẾ; STATIC Hỷ insufficient; Overall still Ất / Mộc / Chính Quan
- [x] Cao Xuân Trường — SINH / TRỢ; Kim sinh Thủy → Tân Chính Ấn
- [x] Lưu Hoàng Sơn — BALANCED-WEALTH; honest Tài lưu thông wording
- [x] Phạm Thị Huyền — TIẾT; Thương Quan sibling displayed
- [x] Lương Văn Mạnh — TIẾT; same as Huyền; Overall still Kim / Tân / Thực Thần
- [x] Ngô Đắc Dũng — TIẾT; no exact Nhâm under Hỷ; Quý Thương Quan SUPPORTED
- [x] Đặng Thị Dung — SINH / TRỢ
- [x] Đoàn Quang Hưng — BALANCED-WEALTH
- [x] Lương Ngọc Huỳnh — BALANCED-WEALTH

---

## Live Dũng verification

- [x] Backend restarted after HK-R1F/R1G (stale uvicorn was the Phase 1 cause)
- [x] Portal Result bundle rebuilt (`npm run build:result`)
- [x] Fresh Analyze — do **not** reuse ResultStore
- [x] Live Result + Print/PDF: Dụng `Thủy · Nhâm · Thực Thần`
- [x] Customer Hỷ: `Thủy · Quý · Thương Quan` (no exact Nhâm duplicate)
- [x] Reason visible: Canh Kim vượng → Tiết → Kim sinh Thủy → Nhâm = Thực Thần
- [x] Điều hậu remains Hỏa / separate from Overall
- [x] Kỵ unchanged: Canh / Tỷ Kiên, Tân / Kiếp Tài

---

## Kỵ V1.0 limitation (technical, not a new algorithm)

> Kỵ thần V1.0 follows the selected structural Useful God rule and does not yet perform full-chart Kỵ reconciliation.

---

## Tests

```
python -m pytest tests/useful_god -q
40 passed, 3 failed
```

- [x] New `tests/useful_god/test_hk_r1g_reasoning.py` (4 passed)
- [ ] Existing G1-06 API test still expects Dụng printed under Hỷ / older contract — **not edited**
- [ ] Existing HK-R1F Tuyền test still expects leftover `Canh · Thực Thần` as customer Hỷ — **not edited**
- [ ] Existing UG-R3F Tuyền test still expects `"Thực Thần" in favorable_display` — **not edited**

Those remaining failures are leftover expected strings from earlier presentation contracts. Product Owner may authorize expected-string updates later. They do **not** reopen winner selection.

---

## Remaining before G1-PREFINAL / G1-FINAL

- Product Owner authorization to start G1-PREFINAL
- Product Owner authorization to update Golden / G1-06 expected strings
- HK-V1.1 / UG-V1.1 knowledge items (non-blocking): Tiết vs Chế, Hao, absent-element candidates, same-element Hỷ theory, independently derived Hỷ, full-chart Kỵ, competing candidates, alternative theory explanations

**HK-R1G: DỤNG REASONING + HỶ ROLE SEMANTICS REPAIRED — V1.0 SEMANTIC FREEZE READY**
