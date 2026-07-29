# Strength Engine V2

Data-driven Strength Engine for BTE Platform.

## Pipeline

```
Calendar → Bazi → Strength Engine → Pattern Engine → Useful God Engine
```

## Public API

```python
from engines.strength_engine import StrengthEngine
from engines.strength_engine.utils.context_builder import build_strength_context

ctx = build_strength_context(bazi_chart, calendar=calendar)
result = StrengthEngine().calculate(ctx)
```

## Output — StrengthResult

| Field | Description |
|-------|-------------|
| `strength_level` | `strong` \| `weak` \| `balanced` |
| `strength_score` | Normalized 0–1 total score |
| `season_score` | Tháng lệnh component |
| `root_score` | Thông căn component |
| `support_score` | Trợ lực component |
| `drain_score` | Tiết khí component |
| `control_score` | Khắc chế component |
| `confidence` | Match confidence 0–1 |
| `matched_rules` | Rule IDs applied |
| `reasoning` | Human-readable summary |
| `metadata` | Full trace for debugging |

## Database

Rules live in `database/12_strength/`. Engine is read-only.

## Integration

Orchestrator injects `strength_level` and `strength_score` into `PatternContext`
before Pattern Engine runs — no Pattern Engine code changes required.
