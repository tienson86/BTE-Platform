# HK-R1F — Refreeze checklist

**Date:** 2026-08-20  
**Gate:** Customer Dụng / Hỷ presentation semantics (V1.0)

---

## Freeze decision

- [x] Internal `UsefulGodResult` / `favorable_gods` / engine `favorable_display` unchanged
- [x] Customer Hỷ omits **only** exact Dụng (element + stem + Ten God)
- [x] Same-element distinct stem/Ten God preserved
- [x] Empty remainder → `Chưa có Hỷ thần bổ trợ riêng` (never reinsert Dụng)
- [x] One SSOT: `engines/useful_god_engine/presentation.py`
- [x] Portal / Report / HTML / PDF / DOCX copy customer `favorable_display`
- [x] Narrative uses filtered customer Hỷ
- [x] Kỵ unchanged (winner-row only)
- [x] Useful God CSV / winner / Strength / Pattern / Five Elements / Temperature / Điều hậu / Ten Gods / ShenSha / Luck / priorities unchanged
- [x] Golden Dataset **not** updated
- [x] G1-FINAL **not** started

---

## 101-case live recompute

- [x] Customer exact-Dụng-in-Hỷ: 101 → **0**
- [x] Internal favorable set changed: **0**
- [x] Overall Dụng changed: **0**
- [x] Kỵ changed: **0**
- [x] Same-element remainder: **27** preserved
- [x] Empty customer Hỷ: **0** (safety implemented)

---

## Control cases (fresh)

- [x] Nguyễn Tiến Sơn
- [x] Vũ Thị Thanh Tuyền
- [x] Cao Xuân Trường
- [x] Lưu Hoàng Sơn
- [x] Phạm Thị Huyền
- [x] Lương Văn Mạnh
- [x] Ngô Đắc Dũng
- [x] Đặng Thị Dung
- [x] Đoàn Quang Hưng
- [x] Lương Ngọc Huỳnh

---

## Kỵ V1.0 limitation (technical, not customer UI)

> Kỵ thần V1.0 follows the selected structural Useful God rule and does not yet perform full-chart Kỵ reconciliation.

---

## Tests

```
python -m pytest tests/useful_god -q
38 passed, 1 failed
```

- [x] New `tests/useful_god/test_hk_r1f_customer_hy.py`
- [x] Existing G1-06 engine-internal asserts still pass
- [ ] Existing G1-06 **API/Report HTML** tests still expect Dụng printed under Hỷ — **not edited** (testing rules). Remaining failures documented in the polish report.

---

## Remaining before G1-FINAL

- Product Owner authorization to update Golden / G1-06 expected strings
- HK-V1.1 Hỷ/Kỵ reconciliation (non-blocking)

**HK-R1F: DỤNG/HỶ CUSTOMER SEMANTICS REPAIRED — HỶ/KỴ V1.0 FREEZE READY**
