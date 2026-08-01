# REGISTRY.md

> Pack 03 Runtime Registry Contract

---

## Contract

Every registry exposes:

- `register(entry_id, entry)`
- `unregister(entry_id)`
- `lookup(entry_id)`
- `list()`
- `validate()`

## Implementation

Shared base: `runtime/registry_base.py` → `BaseRegistry[T]`

Stage registries:

| Registry | Package |
|----------|---------|
| InterpreterRuntimeRegistry | `interpreter_runtime/registry.py` |
| SentenceRuntimeRegistry | `sentence_runtime/registry.py` |
| TemplateRuntimeRegistry | `template_runtime/registry.py` |
| PlaceholderRuntimeRegistry | `placeholder_runtime/registry.py` |
| ExplanationRuntimeRegistry | `explanation_runtime/registry.py` |

## Rules

- Dependency Injection only
- No singleton globals
- Registries store opaque descriptors/refs, never business content bodies
