# G1-06 — Useful God Freeze Checklist

Canonical production remains:

```text
StrengthEngine.strength_level
    + TemperatureResult.climate_state  →  useful_god_temperature_overlay()
    → PatternContext.temperature_type
    → UsefulGodEngine.calculate
    → UsefulGodResult (Ten God + stem + element)
    → data.useful_god / ReportUsefulGodV1
```

V1.0 lock: Overall Useful God from rule groups + priority. Điều hậu stays Temperature climate/need. Mapping reuses G1-01. Portal/Report copy rich fields.

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Useful God reads G1-02 Strength canonical (`strength_level`) | PASS |
| 2 | Useful God reads G1-04 climate canonical (`climate_state` via overlay) | PASS |
| 3 | Does not classify `0.72` as hot | PASS |
| 4 | Flow predicate bug fixed | PASS |
| 5 | Flow rules evaluate values, not key presence | PASS |
| 6 | Candidate list traceable (`rule_id`, group, token, Ten God/stem/element, priority, evidence, match) | PASS |
| 7 | Winner deterministic (`max` group → score → rule priority) | PASS |
| 8 | Winner rule traceable (`winning_rule_id` = `sea_001` on CASE-0001) | PASS |
| 9 | `UsefulGodResult` stores Ten God + stem + element | PASS |
| 10 | Hỷ items enriched from winner row | PASS |
| 11 | Kỵ items enriched from winner row | PASS |
| 12 | G1-01 mapping reused (`ten_god_name` / `stem_for_ten_god`) | PASS |
| 13 | Điều hậu remains separate (`cold` / `warming` ≠ Dụng unless UG selects it) | PASS |
| 14 | Five Elements 19-count not misused as strength | PASS |
| 15 | Portal / Report / PDF / DOCX same rich result | PASS |
| 16 | Regression PASS (module suites listed in repair report) | PASS |
| 17 | No upstream frozen module calculation changed | PASS |
| 18 | Group priorities unchanged (90 / 80 / 70 / 60) | PASS |
| 19 | Golden Dataset synchronized with live CASE-0001 Useful God | PASS |

CASE-0001 freeze facts:

- Strength: `strong` / `0.87`
- Climate: Sửu / winter / `cold` / warming; score `0.72` intensity
- Pattern: Chính Ấn
- Ten Gods visible stems: Bính, Tân, Canh, Mậu
- Useful God overlay input: **`cold`**
- Winner: **`sea_001` → Hỏa · Bính · Thất Sát**
- Hỷ: Bính, Đinh, Giáp (enriched)
- Kỵ: Nhâm, Quý (enriched)

| Sync | Status |
|------|--------|
| Golden Dataset synchronized | **YES** |
| Remaining canonical mismatch | **0** |

Golden `tests/golden_dataset/report_v1/CASE-0001/expected_report_input.json` matches live ReportInputV1 / API / Portal / HTML / DOCX Useful God canonical result.

Stop: do not start G1-07.

G1-06 STATUS: FROZEN FOR BTE V1.0
