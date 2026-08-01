# FACTORY.md

> Pack 03 Interpreter Framework — InterpreterFactory

## Class

`InterpreterFactory`

## Behavior

- Registers constructors by `interpreter_id`
- Creates instances via registry lookup
- **No switch/case / if-elif chains on interpreter id**

## API

| Method | Description |
|--------|-------------|
| `register(id, constructor)` | Bind id → callable/class |
| `unregister(id)` | Remove binding |
| `has(id)` / `registered_ids()` | Introspection |
| `create(id, **kwargs)` | Construct one `BaseInterpreter` |
| `create_all(**kwargs)` | Construct all registered |

## Errors

`ConfigurationError` when:

- id/constructor missing
- id not registered
- constructor does not return `BaseInterpreter`
- created instance has blank `interpreter_id`

## Example

```python
factory = InterpreterFactory()
factory.register("empty_framework_interpreter", EmptyFrameworkInterpreter)
interp = factory.create("empty_framework_interpreter")
```
