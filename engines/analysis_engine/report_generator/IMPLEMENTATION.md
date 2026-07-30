# Implementation Location

The Python implementation for stage **10 Report Generator** lives in:

```text
engines/analysis_engine/report_generator/
```

This directory's sibling (`10_report_generator/`) remains the architecture
documentation baseline (V1.0.0 Frozen).

## Public import

```python
from engines.analysis_engine.report_generator import (
    ReportGenerator,
    ReportAssemblyContext,
    FormatProfile,
    ReportGeneratorResult,
)
```

## Public API

```text
ReportGenerator.assemble(context: ReportAssemblyContext) -> ReportGeneratorResult
```

`ReportEngine` is an alias of `ReportGenerator`.

## Components

- Report Builder — assembles `StructuredReport`
- Section Builder — binds InterpretationResult sections
- Theme — presentation tokens
- Template Loader — layout shells (HTML / Markdown)
- Serializers — HTML, Markdown, PDF, JSON

## Behavior

Assembly and serialization only. No interpretation. No domain recomputation.
