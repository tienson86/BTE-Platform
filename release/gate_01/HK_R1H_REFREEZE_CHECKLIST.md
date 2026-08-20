# HK-R1H — Refreeze checklist

**Date:** 2026-08-20  
**Gate:** Customer Hỷ element separation + Dụng reasoning binding (V1.0)

---

## Freeze decision

- [x] Overall Useful God winner **not** reopened (Dũng remains Water / Nhâm / Thực Thần)
- [x] Internal `favorable_gods` / engine `favorable_display` / Kỵ unchanged
- [x] Customer exact-Dụng duplication = **0**
- [x] Same-element static sibling **not** published as Hỷ thần
- [x] No blind “Hỷ element ≠ Dụng element” UI rule
- [x] Neutral Hỷ wording: `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng`
- [x] One reasoning SSOT (`reasoning.py` → View `short_reason`)
- [x] Portal / Report / HTML / PDF / DOCX copy that string; no frontend reconstruction
- [x] Live card shows **Căn cứ chọn Dụng** as a full-width line, not a crushed grid tile
- [x] No rule IDs on the customer chain
- [x] Điều hậu stays a separate climate layer
- [x] Useful God CSV / Strength / Pattern / Temperature / Flow / Five Elements / Ten Gods / ShenSha / Luck unchanged
- [x] Golden Dataset **not** updated
- [x] G1-PREFINAL / G1-FINAL **not** started
- [x] Stale G1-06 / HK-R1F / HK-R1G expected strings **not** edited (sync in G1-PREFINAL)

---

## Hard acceptance — Ngô Đắc Dũng

- [x] Dụng = Thủy · Nhâm · Thực Thần
- [x] Customer Hỷ ≠ Thủy · Quý · Thương Quan
- [x] Customer Hỷ = Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng
- [x] Căn cứ visible: Canh Kim vượng → Tiết → Kim sinh Thủy → Nhâm = Thực Thần
- [x] No `str_004` in customer reason
- [x] Kỵ unchanged
- [x] Điều hậu Hỏa / Cần ôn ấm separate

---

## 101-case

- [x] A–C, F–I = 0
- [x] D supported independent cases = 16
- [x] E neutral Hỷ cases = 85

---

## Live runtime

- [x] Stale API stopped
- [x] API restarted from current repo/venv (worker PID 11296)
- [x] Portal `npm run build:result` succeeded
- [x] Fresh Analyze — do **not** reuse ResultStore
- [x] Report V1 HTML / PDF / DOCX generated for Dũng

---

## Tests

```
python -m pytest tests/useful_god -q
42 passed, 7 failed
```

- [x] New `tests/useful_god/test_hk_r1h_customer_hy.py` (6 passed)
- [ ] Stale G1-06 / HK-R1F / HK-R1G / UG-R3F expected customer Hỷ strings — **not edited**

---

## Remaining before G1-PREFINAL

- Product Owner authorization to start G1-PREFINAL
- Synchronize stale expected strings / Golden
- HK-V1.1: independently derived Hỷ, same-element Hỷ theory, full-chart Kỵ, Tiết vs Chế, Hao

**HK-R1H: CUSTOMER HỶ ROLE + DỤNG REASONING BINDING REPAIRED — V1.0 CUSTOMER SEMANTIC FREEZE READY**
