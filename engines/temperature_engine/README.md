# Temperature Engine V2

Data-driven Temperature Engine for BTE Platform.

## Pipeline

```
Calendar → Bazi → Strength → Temperature → Pattern → Useful God
```

## Public API

```python
from engines.temperature_engine import TemperatureEngine
from engines.temperature_engine.utils.context_builder import build_temperature_context

ctx = build_temperature_context(bazi_chart, calendar=calendar)
result = TemperatureEngine().calculate(ctx)
```

## Output — TemperatureResult

| Field | Description |
|-------|-------------|
| `temperature_level` | `cold` \| `cool` \| `warm` \| `hot` |
| `temperature_score` | Normalized 0–1 |
| `warm_score` | Ấm/nóng component |
| `cold_score` | Hàn/lạnh component |
| `dry_score` | Táo component |
| `humid_score` | Thấm component |
| `confidence` | Match confidence 0–1 |
| `matched_rules` | Rule IDs applied |
| `reasoning` | Human-readable summary |
| `recommendations` | Điều hậu suggestions |
| `metadata.trace` | Full debug trace |

## Integration

Orchestrator injects `temperature_type` into `PatternContext` before Pattern runs.
