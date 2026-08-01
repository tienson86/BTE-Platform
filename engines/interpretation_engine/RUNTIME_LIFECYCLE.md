# RUNTIME_LIFECYCLE.md

> Pack 03 Runtime Lifecycle

---

## Lifecycle

```
CREATED (UNKNOWN)
    ↓ initialize()
READY
    ↓ execute()
RUNNING → READY (success) | FAILED (failure)
    ↓ shutdown()
DISABLED
```

## Contract Methods

| Method | Responsibility |
|--------|----------------|
| `initialize()` | Acquire resources, set READY |
| `validate()` | Confirm READY/RUNNING and dependencies |
| `execute(context)` | Run stage shell; update metrics/health |
| `metrics()` | Return RuntimeMetricsSnapshot |
| `health()` | Return HealthStatus |
| `shutdown()` | Release resources, set DISABLED |

## Pipeline Lifecycle

`ExecutionManager` wraps `RuntimePipeline`:

1. `initialize()` — pipeline + all stages
2. `validate()` — pipeline + stages
3. `execute(PackInterpretationContext)`
4. `shutdown()` — reverse stage order

## Metrics Collected

- execution_count
- success_count
- failure_count
- execution_time
- average_time
- last_execution
- health
