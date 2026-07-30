# Implementation Location

The Python implementation for **Interpretation Engine** lives in:

```text
engines/analysis_engine/interpretation_engine/
```

Interpretation sits **after** AnalysisResult and **before** Report Generator.
It is not an Analysis Runtime stage (01–09).

## Public import

```python
from engines.analysis_engine.interpretation_engine import (
    InterpretationEngine,
    InterpretationContext,
    InterpretationResult,
    create_default_knowledge_session,
)
```

## Pipeline

```text
AnalysisResult
        │
        ▼
Sentence Selection
        │
        ▼
Template Binding
        │
        ▼
Placeholder Binding
        │
        ▼
Paragraph Builder
        │
        ▼
Interpretation Builder
        │
        ▼
InterpretationResult
```

## Behavior

- Consumes published `AnalysisResult` only (read-only)
- Selects sentences from Knowledge SDK (`interpretation_knowledge`)
- Binds templates and placeholders deterministically
- Does not recompute analytical stages
- Does not render HTML/PDF reports
