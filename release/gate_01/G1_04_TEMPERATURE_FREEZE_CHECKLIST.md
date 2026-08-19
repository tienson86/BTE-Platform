# G1-04 — Temperature Freeze Checklist

Canonical production remains:

```text
engines/temperature_engine
    → build_temperature_context (BaZi month branch)
    → TemperatureEngine.calculate
    → AnalysisResult.temperature (TemperatureView)
    → climate_state + balancing_need + evidence_compact
```

V1.0 lock: **minimal Điều hậu** (climate state + balancing need). Not Deep Điều Hậu. Not Overall Useful God.

```text
Season / Climate → Climate State → Balancing Need / Điều hậu
```

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Temperature score semantic determined (Case 2: imbalance / intensity) | PASS |
| 2 | Cold/hot **published** direction not inverted by score thresholds | PASS |
| 3 | Classification follows climate facts (`temperature_level` = `climate_state`) | PASS |
| 4 | Season source is canonical BaZi month branch | PASS |
| 5 | CASE-0001 Sửu = winter | PASS |
| 6 | CASE-0001 base climate = cold | PASS |
| 7 | Điều hậu balancing need has canonical source (`cli_*` mapping) | PASS |
| 8 | Điều hậu is not Overall Useful God | PASS |
| 9 | Adapter no longer emits `Điều hậu: —` when climate data exists | PASS |
| 10 | `pattern.dieu_hau` not used as Temperature Điều hậu (relabeled Đắc lệnh) | PASS |
| 11 | Portal / Full Report / PDF / DOCX share TemperatureView source | PASS |
| 12 | Strength G1-02 unchanged (`0.87` / `strong`) | PASS |
| 13 | Pattern G1-03 unchanged (`Chính Ấn` / `pat_ca_01`) | PASS |
| 14 | Ten Gods G1-01 unchanged (Bính, Tân, Canh, Mậu) | PASS |
| 15 | Useful God Engine/CSV not edited; CASE-0001 winner still Thực Thần | PASS |
| 16 | Representative seasonal matrix PASS (12 branches + Fire/Water modifiers) | PASS |
| 17 | CASE-0001 / Report / portal regression PASS | PASS |
| 18 | No Deep Điều Hậu narrative added | PASS |
| 19 | Customer UI does not lead with numeric `0.72` | PASS |
| 20 | No tài vận / sức khỏe / nghề / cải vận Điều hậu copy | PASS |

Stop: do not start G1-05. Do not edit Useful God selection or Deep Interpretation.

G1-04 STATUS: FINAL FREEZE READY
