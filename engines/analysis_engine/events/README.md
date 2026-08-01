# Events Package

> **Path:** `engines/analysis_engine/events/`

Internal in-process event framework for Analysis Engine runtime signals.

## Modules

| Module | Surface |
|--------|---------|
| `event_types.py` | `EventType` |
| `events.py` | `Event`, `create_event` |
| `listeners.py` | `EventListener`, typed/wildcard/recording listeners |
| `dispatcher.py` | `EventDispatcher`, `DispatchResult` |
| `event_bus.py` | `EventBus` |

Internal runtime only. No external messaging brokers or network I/O.
