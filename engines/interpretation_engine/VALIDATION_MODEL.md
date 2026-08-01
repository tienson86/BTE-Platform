# VALIDATION_MODEL.md

> Pack 03 Interpreter Framework — Validation

## Class

`InterpreterValidator`

## Checks

| Method | Purpose |
|--------|---------|
| `validate_input` / `require_input` | `PackInterpretationContext` |
| `validate_capability` / `require_capability` | Capability contract |
| `validate_section` / `require_section` | `InterpretationSection` |
| `validate_result` / `require_result` | `FrameworkInterpreterResult` |
| `validate_dependencies` / `require_dependencies` | Dependency graph |
| `validate_dependency_edge` | Single edge |

## Exceptions

- `ValidationError` — input/result/contract failures
- `DependencyError` — graph failures (from resolver)

## Framework Context Wrapper

`FrameworkInterpreterContext` wraps frozen `PackInterpretationContext` plus optional `InterpreterMetadata` without replacing Pack 03 contracts.
