# Temperature Rule Database V2

Data-driven rules for Temperature Engine V2 (`database/11_temperature/`).

## Pipeline

```
Calendar → Bazi → Strength → Temperature → Pattern → Useful God
```

## Files

| File | Purpose |
|------|---------|
| `01_season_rules.csv` | Mùa sinh ảnh hưởng nhiệt độ |
| `02_climate_rules.csv` | Khí hậu địa chi tháng |
| `03_dryness_rules.csv` | Khí táo (Hỏa/Thổ vượng) |
| `04_humidity_rules.csv` | Khí thấm (Thủy vượng) |
| `05_balance_rules.csv` | Cân bằng ấm-hàn, táo-thấm |
| `06_priority_rules.csv` | Group priority + level classification |
| `07_special_rules.csv` | Trường hợp đặc biệt + flow |
| `08_examples.csv` | Golden examples |
| `09_conditions.csv` | Normalization config |

## Rule Schema

```
rule_id, priority, score, score_target, conditions, temperature_level, recommendation, reason, description, reference, status, enabled
```

## Output Mapping

Temperature Engine sets `PatternContext.temperature_type` to one of:
`cold` | `cool` | `warm` | `hot` — consumed by Useful God Engine.
