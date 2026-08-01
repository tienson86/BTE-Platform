# RUNTIME_PIPELINE.md

> Pack 03 Runtime Pipeline

---

## Execution Pipeline (Interpreter-focused)

```
PackInterpretationContext
        ↓
Registry
        ↓
Interpreter Dispatcher
        ↓
Interpreter Runtime
        ↓
Section Collection
        ↓
Explanation Runtime
        ↓
InterpretationResult
```

Implementation: `orchestration/execution_pipeline.py` (`ExecutionPipeline`)

Supports:

- ordered execution
- dependency execution
- future async execution (sync fallback today)
- error isolation

---

## Stage Pipeline (Stage-runtime orchestration)

```
PackInterpretationContext
        ↓
Interpreter Runtime
        ↓
Sentence Runtime
        ↓
Template Runtime
        ↓
Placeholder Runtime
        ↓
Explanation Runtime
        ↓
InterpretationResult
```

Implementation: `orchestration/runtime_pipeline.py` (`RuntimePipeline`)

---

## Non-Goals

- No BaZi rules
- No sentence generation
- No template bodies
- No placeholder value interpretation
- No explanation narrative
- No report rendering (PDF/HTML/DOCX)
- No AI rewrite
