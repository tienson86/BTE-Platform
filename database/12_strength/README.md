# Strength Rule Database V2

Database-driven rules for Strength Engine V2 (`database/12_strength/`).

## Files

| File | Purpose |
|------|---------|
| `01_season_rules.csv` | Tháng lệnh (Đắc lệnh / Tướng / Hưu / Tù / Tử) |
| `02_root_rules.csv` | Thông căn / Vô căn |
| `03_support_rules.csv` | Trợ lực (Ấn, Tỷ Kiên, hợp hóa) |
| `04_control_rules.csv` | Khắc chế (Quan, Thực, Tài) |
| `05_flow_rules.csv` | Tiết khí / hao tán |
| `06_priority_rules.csv` | Group priority + level classification |
| `07_special_rules.csv` | Trường hợp đặc biệt + hợp hóa |
| `08_examples.csv` | Golden examples for validation |
| `09_conditions.csv` | Normalization config (baseline, scale, thresholds) |

## Rule Schema

```
rule_id, priority, score, score_target, conditions, strength_level, reason, description, reference, status, enabled
```

- `score_target`: `season` | `root` | `support` | `drain` | `control` | `combination` | `special` | `level` | `config`
- `conditions`: JSON array of `{field, operator, value}`
- `strength_level`: optional output hint (`strong` | `weak` | `balanced`)

## Pipeline Position

```
Calendar → Bazi → Strength Engine → Pattern Engine → Useful God Engine
```

Strength Engine populates `PatternContext.strength_level` and `strength_score` before Pattern runs.
