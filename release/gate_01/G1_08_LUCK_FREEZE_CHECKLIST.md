# G1-08 — Luck / Đại vận Freeze Checklist

Canonical production remains:

```text
CalendarEngine.build
  → BaziEngine.build(gender)
  → LuckEngine.build
       DefaultDayunProvider.provide
  → shape_luck_payload
  → API data.luck / Report luck_cycles / Portal copy
```

V1.0 lock (Product Owner **Option A**): year-level precision; 12-Jie calendar days; `round(days/3)` integer start age; current = `current_year - birth_year`. Exact giao vận datetime is **LUCK-PRECISION-V1.1**.

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Production Luck Engine unchanged except gender + evidence metadata | PASS |
| 2 | Direction formula locked: `is_male == is_yang(niên can)` | PASS |
| 3 | Year-stem polarity canonical `STEM_META` | PASS |
| 4 | 12-Jie method documented (no trung khí) | PASS |
| 5 | Year-level precision documented | PASS |
| 6 | `round(days/3)` formula unchanged | PASS |
| 7 | Missing gender no longer silently defaults male | PASS |
| 8 | Same-Jie-day limitation documented and tested | PASS |
| 9 | CASE-0001 start age = 5 | PASS |
| 10 | First cycle = Nhâm Dần | PASS |
| 11 | Full sequence deterministic | PASS |
| 12 | Current cycle = Ất Tỵ 2022–2031 (year-age in 2026) | PASS |
| 13 | JiaZi wrap tests PASS | PASS |
| 14 | Cycle boundaries no gap/overlap; 10-year spans; ±1 JiaZi | PASS |
| 15 | Portal/API use canonical `current_cycle` | PASS |
| 16 | Report false “cycles not provided” note removed when cycles exist | PASS |
| 17 | Report/PDF/DOCX use canonical sequence | PASS |
| 18 | Golden agrees with live sequence | PASS |
| 19 | No Deep Luck Interpretation added | PASS |
| 20 | G1-08 regression tests PASS | PASS |
| 21 | Customer display Nam/Nữ; no male/female leak | PASS |
| 22 | Missing/invalid gender → 422; never default male | PASS |
| 23 | Portal/Report gender labels identical (Nam/Nữ) | PASS |
| 24 | CASE-0001 customer Giới tính: Nam; Nam + Bính Dương → Thuận | PASS |

CASE-0001 freeze facts:

- Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
- Direction: **Thuận** (Nam · Bính Dương)
- Jie: Lập Xuân 1987-02-04 · 14 days · start age **5**
- Sequence: Nhâm Dần … Tân Hợi
- Current: **Ất Tỵ · 2022–2031 · tuổi 35–44**
- Evidence: `Nam · Niên can Bính Dương · Thuận`
- Method: `Khởi vận theo ngày lịch và Tiết khí, độ chính xác theo năm`

| Sync | Status |
|------|--------|
| Golden Dataset synchronized | **YES** (sequence unchanged; presentation fields added) |
| Remaining canonical Luck mismatch | **0** |

Stop: do not start Gate 2. Do not start G1-FINAL automatically.

G1-08 STATUS: FROZEN FOR BTE V1.0
