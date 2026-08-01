# Events

Local in-process Event Bus for Pack 03 runtime.

## Supported events

- `before_interpreter`
- `after_interpreter`
- `pipeline_started`
- `pipeline_finished`
- `runtime_error`
- `health_changed`

## Rules

- No external broker
- Local runtime only
- Dependency Injection only (no singleton)
- Handler failures are isolated

## Modules

| File | Role |
|------|------|
| `event_bus.py` | `LocalEventBus` / `EventBus` |
| `event_types.py` | Event type enum |
| `event_model.py` | `RuntimeEvent` envelope |
| `event_bus_interface.py` | Abstract contract |
