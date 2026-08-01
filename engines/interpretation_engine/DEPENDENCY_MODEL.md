# DEPENDENCY_MODEL.md

> Pack 03 Interpreter Framework — Dependency & Priority

## Dependency Edge

`InterpreterDependency(interpreter_id, depends_on, required=True)`

- Required vs optional is modeled explicitly
- Self-dependencies are invalid

## Resolver

`DependencyResolver.resolve(interpreter_ids, required, optional=None)`

Returns `DependencyResolution`:

- `order` — topological execution order (required edges)
- `missing_optional` — optional gaps (non-fatal)
- raises `DependencyError` for missing required deps or cycles

## Priority

`InterpreterPriority(interpreter_id, priority)` — lower runs first.

Helpers:

- `sort_by_priority(...)`
- `order_ids_by_priority(priority_map, ids=...)`

## Capability Integration

`InterpreterCapability` carries:

- `dependencies` (required)
- `optional_dependencies`
- `priority`

Overlapping required/optional ids invalidate the capability.
