# Unified Analysis Context V2

Data-driven context aggregation layer for BTE Platform.

## Pipeline

```
Calendar → Bazi → Strength → Temperature → Pattern → Useful God
                              ↓
                      ContextEngine (UnifiedAnalysisContext)
                              ↓
                      RuleContext → Score → Interpretation → Report
```

## Public API

```python
from engines.context_engine import ContextEngine

engine = ContextEngine()
unified, rule_context = engine.build_and_publish(
    calendar=calendar,
    bazi=bazi_chart,
    strength=strength_result,
    temperature=temperature_result,
    pattern=pattern_result,
    useful_god=useful_god_result,
)
```

## Output — UnifiedAnalysisContext

| Section | Key fields |
|---------|------------|
| `strength` | `level`, `score`, component scores |
| `temperature` | `level`, `type`, `score`, warm/cold/dry/humid |
| `pattern` | `main`, `follow`, `score` |
| `useful_god` | `primary`, `favorable`, `unfavorable` |
| `metadata.trace` | Engine, input, output, duration, confidence |

## Serializer

`analysis_context.json` — version `2.0.0`, schema in `serializers.py`.

## Design rules

- Does **not** modify Strength / Temperature / Pattern / Useful God engines
- RuleContext is **derived** from unified context via adapter
- Interpretation consumes RuleContext produced by ContextEngine only
