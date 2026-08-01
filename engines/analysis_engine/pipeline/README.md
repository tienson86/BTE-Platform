# Pipeline Package

Architecture skeleton for Analysis Engine pipeline orchestration.

## Public Modules

| Module | Interface |
|--------|-----------|
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

Public interfaces only. No algorithms. No BaZi analysis.
