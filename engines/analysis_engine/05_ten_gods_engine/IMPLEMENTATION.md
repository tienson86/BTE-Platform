# Implementation Location

The Python implementation for stage **05 Ten Gods Engine** lives in the
importable package:

```text
engines/analysis_engine/ten_gods_engine/
```

This directory (`05_ten_gods_engine/`) remains the architecture documentation
baseline (V1.0.0 Frozen).

## Why a separate package name?

Python module path segments cannot start with a digit, so
`engines.analysis_engine.05_ten_gods_engine` is not a legal import path.

## Public import

```python
from engines.analysis_engine.ten_gods_engine import (
    TenGodsEngine,
    TenGodsResult,
    create_default_knowledge_session,
)
```
