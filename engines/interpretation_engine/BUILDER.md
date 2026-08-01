# BUILDER.md

> Pack 03 Interpreter Framework — InterpretationSectionBuilder

## Class

`InterpretationSectionBuilder` (alias: `InterpreterBuilder`)

Builds frozen `InterpretationSection` (`SectionResult`) shells.

## Fluent API

- `with_id` / `with_section_type` / `with_title_ref` / `with_interpreter_id`
- `with_paragraphs` / `add_paragraph`
- `with_success` / `with_messages` / `add_message`
- `with_attributes` / `update_attributes`
- `for_interpreter(interpreter_id, section_type, context_id=...)`
- `build()`

## Rules

- `id` and `section_type` are required
- `build()` calls `section.validate()` and raises `ConfigurationError` on failure
- All framework interpreters should construct sections through this builder

## Example

```python
section = (
    InterpretationSectionBuilder()
    .for_interpreter(interpreter_id="demo", section_type="demo", context_id=ctx.id)
    .with_messages(("demo_ok",))
    .with_attributes({"framework": True})
    .build()
)
```
