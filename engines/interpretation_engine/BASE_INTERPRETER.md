# BASE_INTERPRETER.md

> Pack 03 Interpreter Framework — BaseInterpreter

## Class

`engines.interpretation_engine.interpreter_framework.base_interpreter.BaseInterpreter`

Extends frozen `InterpreterSkeletonRuntime` → `BaseRuntime`.

## Lifecycle

| Method | Role |
|--------|------|
| `initialize()` | Ready runtime (frozen) |
| `validate()` | Readiness check (frozen) |
| `before_execute(context)` | Framework hook (overridable) |
| `execute(context)` | Frozen wrapper calling `_execute_body` |
| `after_execute(context, result, error=...)` | Framework hook (overridable) |
| `shutdown()` | Disable runtime (frozen) |
| `health()` / `metrics()` | Frozen snapshots |

## Subclass Contract

Implement:

```python
def interpret(self, context: PackInterpretationContext) -> FrameworkInterpreterResult:
    ...
```

Rules:

- Build sections with `InterpretationSectionBuilder` / `self.new_builder()`
- Do not reimplement lifecycle counters
- Declare `interpreter_id`, `section_type`, `version`, `category`, `dependencies`, `default_priority`

## Standard Output

`FrameworkInterpreterResult` includes:

- `section` (`InterpretationSection` / `SectionResult`)
- `metadata`
- `trace`
- `confidence`
- `warnings`
- `statistics`
- `messages`

## Reference Implementation

`EmptyFrameworkInterpreter` — empty section only, used by tests/factory demos.
