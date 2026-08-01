# INTERPRETER_FRAMEWORK.md

> Pack 03 — Common Interpreter Framework  
> Location: `engines/interpretation_engine/interpreter_framework/`  
> Status: Implemented

## Purpose

Reusable business framework for Pack 03 interpreters.

Runtime infrastructure remains frozen. This package wraps those contracts so every future interpreter can share:

- lifecycle hooks
- capability / dependency / priority models
- section builder
- validation
- factory creation
- standard result shape

**No BaZi interpretation logic lives here.**

## Package Layout

```
interpreter_framework/
  base_interpreter.py
  interpreter_context.py
  interpreter_result.py
  interpreter_metadata.py
  interpreter_trace.py
  interpreter_capability.py
  interpreter_priority.py
  interpreter_dependency.py
  interpreter_factory.py
  interpreter_builder.py
  interpreter_validator.py
  interpreter_exception.py
  __init__.py
```

## Design Principles

1. **Wrap, do not mutate** frozen Pack 03 contracts (`BaseRuntime`, `InterpreterSkeletonRuntime`, `PackInterpretationContext`, `SectionResult`).
2. **One lifecycle** in `BaseInterpreter` — subclasses implement `interpret()` only.
3. **Builder required** for `InterpretationSection` construction.
4. **Factory is registry-driven** — no switch/case.
5. **DI** — validators/builders injected via constructors.

## Quick Start

```python
from engines.interpretation_engine.interpreter_framework import (
    EmptyFrameworkInterpreter,
    InterpreterFactory,
)

factory = InterpreterFactory()
factory.register("empty_framework_interpreter", EmptyFrameworkInterpreter)
runtime = factory.create("empty_framework_interpreter")
runtime.initialize()
result = runtime.execute(pack_context)
```

## Related Docs

- `BASE_INTERPRETER.md`
- `FACTORY.md`
- `BUILDER.md`
- `DEPENDENCY_MODEL.md`
- `VALIDATION_MODEL.md`
- `INTERPRETER_FRAMEWORK_AUDIT.md`
