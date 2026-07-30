# Implementation Location

The Python implementation for stage **10 Report Generator** lives in:

```text
engines/analysis_engine/report_generator/
```

This directory (`10_report_generator/`) remains the architecture documentation
baseline (V1.0.0 Frozen).

## Public import

```python
from engines.analysis_engine.report_generator import (
    ReportGenerator,
    ReportAssemblyContext,
    FormatProfile,
    ReportGeneratorResult,
)
```

## Behavior

- Consumes published `InterpretationResult` (mandatory)
- Optionally binds `AnalysisResult` structured data (read-only)
- Produces HTML / Markdown / PDF / JSON from one `StructuredReport`
- No interpretation and no analytical recomputation
