# Analysis Runtime — Developer Guide

**Module:** `engines.analysis_engine.runtime`  
**Version:** 1.0.0  
**Status:** Implementation Baseline

---

# 1. Purpose

This guide explains how to use and extend the Analysis Runtime framework.

The runtime orchestrates analysis stage modules. It does **not** implement business rules, interpretation, or report rendering.

---

# 2. Install / Import

```python
from engines.analysis_engine.runtime import (
    AnalysisContext,
    AnalysisResult,
    AnalysisRuntime,
    BaseAnalysisModule,
    StageResult,
)
```

Or:

```python
from engines.analysis_engine import AnalysisRuntime, AnalysisContext, AnalysisResult
```

---

# 3. Public API

| Method | Description |
|--------|-------------|
| `register(module)` | Register a stage module by `stage_id` |
| `validate(context)` | Admission validation without full execution |
| `execute(module, context)` | Run one stage (module instance or stage id) |
| `run(context)` | Execute full sequential pipeline → `AnalysisResult` |
| `evaluate(context)` | Alias of `run` (Analysis Engine contract) |

---

# 4. Minimal Example

```python
from engines.analysis_engine.runtime import (
    AnalysisContext,
    AnalysisRuntime,
    BaseAnalysisModule,
    StageResult,
)
from engines.analysis_engine.runtime.constants import DEFAULT_DEPENDENCIES


class StrengthStub(BaseAnalysisModule):
    stage_id = "strength"
    dependencies = ()

    def evaluate(self, context: AnalysisContext) -> StageResult:
        return StageResult(
            stage_id=self.stage_id,
            payload={"day_master": context.chart.get("day_master")},
        )


runtime = AnalysisRuntime(require_all_canonical_stages=False)
runtime.register(StrengthStub())

context = AnalysisContext(
    request_id="demo-1",
    chart={"day_master": "Jia"},
)

report = runtime.validate(context)
assert report.is_valid

result = runtime.run(context)
print(result.strength_result.payload)
```

---

# 5. Implementing a Stage Module

Implement the `AnalysisModule` protocol (or subclass `BaseAnalysisModule`):

```python
class TemperatureModule(BaseAnalysisModule):
    stage_id = "temperature"
    version = "1.0.0"
    dependencies = ("strength",)

    def evaluate(self, context: AnalysisContext) -> StageResult:
        strength = context.strength_result  # read from shared context
        return StageResult(
            stage_id=self.stage_id,
            payload={"based_on": strength.payload if strength else None},
        )
```

Rules:

- Return `StageResult` with matching `stage_id`
- Read upstream results only from `AnalysisContext`
- Do not call sibling modules
- Do not mutate prior stage results
- Do not perform interpretation or report rendering

---

# 6. Canonical Pipeline

```text
strength → temperature → pattern → useful_god → ten_gods
→ combination → shensha → luck → summary
```

Default: `require_all_canonical_stages=True` — all nine modules must be registered before `run()`.

For partial harnesses/tests:

```python
AnalysisRuntime(require_all_canonical_stages=False)
```

---

# 7. Shared Context

`AnalysisContext` holds:

- immutable input snapshot (`chart`, `calendar`)
- append-only stage results
- optional `knowledge_session` / `knowledge_version`

Access published results:

```python
context.strength_result
context.get_stage_result("luck")
context.publish_stage_result(result)  # runtime-owned; modules return results instead
```

---

# 8. Dependency Injection

```python
runtime = AnalysisRuntime(
    dependency_resolver=DependencyResolver(),
    cache_manager=CacheManager(),
    error_handler=ErrorHandler(),
    validation_manager=ValidationManager(),
    knowledge_binder=lambda ctx: setattr(ctx, "knowledge_version", "1.0.0"),
)
```

---

# 9. Observability

Successful `AnalysisResult` includes:

- `execution_metadata` — request timing / status
- `performance_metrics` — total and per-stage latency, cache stats
- `execution_trace` — ordered stage spans
- structured logging via the `logging` module (`stage_executed`, `pipeline_completed`, …)

---

# 10. Errors

Failures are fail-closed. No successful `AnalysisResult` is published on mandatory failure.

Common classes:

- `AdmissionError`
- `PrerequisiteError`
- `StageExecutionError`
- `ValidationError`
- `StateError`
- `RegistrationError`

---

# 11. Testing

```bash
pytest tests/analysis_runtime -q
```

Use stub modules (no business rules) for unit and integration coverage.

---

# 12. Boundaries

| In scope | Out of scope |
|----------|--------------|
| Orchestration | Business rule logic |
| Shared context | Interpretation narrative |
| Validation / cache / tracing | Report HTML/PDF/JSON rendering |
| Module registration | Knowledge content authoring |

---

# 13. Version

Runtime implementation version: **1.0.0**

Aligned with Analysis Runtime Specification V1.0.0 (Frozen Runtime Baseline).
