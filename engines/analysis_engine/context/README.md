# Context Package

> **Path:** `engines/analysis_engine/context/`

Typed context architecture and lifecycle runtime for the Analysis Engine.

## Lifecycle Runtime

| Module | Surface |
|--------|---------|
| `context_builder.py` | `ContextBuilder`, `utc_now` |
| `context_factory.py` | `ContextFactory` |
| `context_manager.py` | `ContextManager` |
| `context_snapshot.py` | `ContextSnapshot` |
| `context_revision.py` | `ContextRevision`, `ContextLifecyclePhase` |
| `context_history.py` | `ContextHistory` |
| `context_serializer.py` | `ContextSerializer` |

Lifecycle: Create → Initialize → Expand → Validate → Finalize → Dispose.

## Typed Context Contracts

| Module | Type |
|--------|------|
| `interfaces.py` | `ContextInterface`, `ContextBuilderInterface` |
| `chart_context.py` | `ChartContext` |
| `strength_context.py` | `StrengthContext` |
| `pattern_context.py` | `PatternContext` |
| `temperature_context.py` | `TemperatureContext` |
| `ten_gods_context.py` | `TenGodsContext` |
| `dayun_context.py` | `DayunContext` |
| `liunian_context.py` | `LiunianContext` |
| `runtime_context.py` | `RuntimeContext` |

Context lifecycle only. No analyzer / BaZi logic.
