# DISPATCHER.md

> Pack 03 Interpreter Dispatcher

---

## Location

`interpreter_runtime/dispatcher.py`

## Capabilities

- `register(entry_id, handler, *, priority, dependencies, enabled, metadata)`
- `unregister(entry_id)`
- `list()`
- `execution_order()` — dependency topology + priority ordering
- `dispatch(context)` — synchronous ordered execution

## Ordering

1. Enabled handlers only
2. Topological order by registered dependencies
3. Within ready set: lower `priority` value first, then id

## Future Design

- Parallel-ready structure
- Async-capable handler contract reserved
- **No asyncio implementation yet**

## Errors

- Circular dependencies raise `RegistryError("dispatcher_circular_dependency")`
