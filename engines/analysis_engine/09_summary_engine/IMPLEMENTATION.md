# Implementation Location

The Python implementation for stage **09 Summary Engine** lives in:

```text
engines/analysis_engine/summary_engine/
```

This directory (`09_summary_engine/`) remains the architecture documentation
baseline (V1.0.0 Frozen).

## Public import

```python
from engines.analysis_engine.summary_engine import (
    SummaryEngine,
    SummaryResult,
)
```

## Behavior

Aggregation only:

- Strength
- Temperature
- Pattern
- Useful God
- Ten Gods
- Combination
- ShenSha
- Luck

No Knowledge SDK. No domain recomputation.
