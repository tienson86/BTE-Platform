# Pipeline Package

> **Path:** `engines/analysis_engine/pipeline/`

Pipeline orchestration interfaces and contracts.

## Modules

| Module | Surface |
|--------|---------|
| `pipeline.py` | `Pipeline` |
| `stage_base.py` | `StageBase` |
| `pipeline_context.py` | `PipelineContext` |
| `pipeline_result.py` | `PipelineResult`, `StageOutcome` |
| `registry.py` | `StageRegistry` |
| `execution_graph.py` | `ExecutionGraph` |
| `scheduler.py` | `Scheduler` |
| `stage_loader.py` | `StageLoader` |
| `stage_validator.py` | `StageValidator` |
| `stage_executor.py` | `StageExecutor` |
| `stage_finalizer.py` | `StageFinalizer` |
| `contracts.py` | Stage/Context/Result/Policy contracts |

Public interfaces and contracts only. No algorithms.
