# G1-01 — Ten Gods Freeze Checklist

Canonical production remains:

```text
engines/ten_gods_engine
    → engines.bazi_engine.ten_god.ten_god_name
```

Do not freeze if production was switched to `engines/analysis_engine/ten_gods_engine`.

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Canonical production engine not replaced | PASS |
| 2 | 4 Fire×Wood conflicts diagnosed (CSV polarity inverted) | PASS |
| 3 | Wrong source fixed (CSV TT021/022/031/032 only) | PASS |
| 4 | Truth matrix 100/100 | PASS |
| 5 | Golden CASE visible 4/4 | PASS |
| 6 | Golden CASE hidden 11/11 | PASS |
| 7 | Visible and hidden have provenance (pillar/branch/stem/element/ten god/visibility) | PASS |
| 8 | Ngũ hành shown with stems where appropriate | PASS |
| 9 | Summary distinguishes Lộ can vs Tàng can | PASS |
| 10 | Portal uses canonical Ten Gods payload | PASS |
| 11 | Report uses the same canonical data (no recalculation) | PASS |
| 12 | PDF/DOCX share `build_presented_report` and keep hidden Ten Gods | PASS |
| 13 | No duplicate Ten God calculation in presentation | PASS |
| 14 | Regression tests PASS | PASS |
| 15 | No Deep Interpretation added | PASS |
| 16 | Same-stem relationship is Tỷ Kiên except Day Pillar heavenly stem → Nhật Chủ | PASS |
| 17 | Hidden same-stem for all 10 Day Masters → Tỷ Kiên | PASS |
| 18 | Compact `ten_gods.hidden` stem-name list is NON-BLOCKING V1.1 compatibility debt | PASS (non-blocking) |

Stop: do not start G1-02. Do not edit Strength, Temperature, Pattern, or Useful God.

G1-01 STATUS: FINAL FREEZE READY
