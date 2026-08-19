# G1-05 — Five Elements Freeze Checklist

Canonical production remains:

```text
BaziEngine
    → RuleContextBuilder._build_wuxing
    → data.five_elements.counts
```

V1.0 lock: **Phân bố Ngũ hành** only (structural occurrence). Not strength, not balance, not vượng/suy, not weighted power.

```text
Thiên can +1 · bản hành Địa chi +1 · Tàng can occurrence +1
```

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Canonical count formula unchanged (`_build_wuxing`) | PASS |
| 2 | CASE-0001 = Mộc 4 / Hỏa 5 / Thổ 6 / Kim 3 / Thủy 1 | PASS |
| 3 | Total = 19 (4 stems + 4 branch elements + 11 hidden) | PASS |
| 4 | S04 semantic = Phân bố Ngũ hành | PASS |
| 5 | No unsupported Mạnh/Yếu from count | PASS |
| 6 | No unsupported Vượng/Thiếu from count | PASS |
| 7 | No `Thổ nổi` / hành trội from max(count) | PASS |
| 8 | `wuxing_score` not mixed into distribution | PASS |
| 9 | Score grade not mixed into S04 | PASS |
| 10 | Minimum provenance shown | PASS |
| 11 | Internal 15-tally not used as customer 19-count | PASS |
| 12 | Portal / Report / PDF / DOCX same 4/5/6/3/1 | PASS |
| 13 | Missing element ≠ Dụng/Hỷ/Kỵ / khuyết hành | PASS |
| 14 | Regression tests PASS | PASS |
| 15 | Strength unchanged (CASE-0001 `0.87` / `strong`) | PASS |
| 16 | Temperature unchanged (Sửu / cold / warming) | PASS |
| 17 | Pattern unchanged (Chính Ấn / `pat_ca_01`) | PASS |
| 18 | Ten Gods unchanged (Bính, Tân, Canh, Mậu) | PASS |
| 19 | Useful God unchanged (Thực Thần); engine/CSV not edited | PASS |
| 20 | No Deep Five Elements interpretation added | PASS |

Stop: do not start G1-06. Do not edit Useful God.

G1-05 STATUS: FINAL FREEZE READY
