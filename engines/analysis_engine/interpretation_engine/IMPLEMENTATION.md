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
Sentence Ranking
        │
        ▼
Conflict Resolution
        │
        ▼
Placeholder Binding
        │
        ▼
Paragraph Builder
        │
        ▼
Chapter Builder
        │
        ▼
Explanation Builder
        │
        ▼
Markdown / HTML / JSON Builders
        │
        ▼
InterpretationResult
```

## Knowledge consumption

- Knowledge SDK session (`get_module` / `get_asset`)
- Sentence Library (`interpretation.sentences` + templates)
- Phrase Library (`interpretation.phrases`)
- Terminology Library (`interpretation.terminology`)

## Behavior

- Consumes published `AnalysisResult` only (read-only)
- Rule-based only — no AI generation
- Deterministic, explainable, and traceable via `explanations` + `evidence`
- Outputs `InterpretationResult` with `markdown`, `html`, and `json_text`
- Does not recompute analytical stages
- Does not render PDF (Report Generator responsibility)
