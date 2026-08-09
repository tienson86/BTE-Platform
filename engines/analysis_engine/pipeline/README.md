# Pipeline Package

> **Path:** `engines/analysis_engine/pipeline/`

Pipeline orchestration runtime and contracts.

## Modules

| Module | Surface |
|--------|---------|
| `executor.py` | `Executor` |
| `pipeline_executor.py` | `PipelineExecutor` |
| `stage_executor.py` | `StageExecutor` |
| `execution_context.py` | `ExecutionContext` |
| `execution_result.py` | `ExecutionResult` |
| `execution_state.py` | `ExecutionState` |
| `execution_policy.py` | `ExecutionPolicy` |
| `execution_hooks.py` | `ExecutionHooks`, `NoOpExecutionHooks` |
| `pipeline.py` | `Pipeline` |
| `stage_base.py` | `StageBase` |
| `pipeline_context.py` | `PipelineContext` |
| `pipeline_result.py` | `PipelineResult`, `StageOutcome` |
| `stage_finalizer.py` | `StageFinalizer` |
| `registry.py` | `StageRegistry` |
| `execution_graph.py` | `ExecutionGraph` |
| `scheduler.py` | `Scheduler` |
| `stage_loader.py` | `StageLoader` |
| `stage_validator.py` | `StageValidator` |
| `contracts.py` | Stage/Context/Result/Policy contracts |
| `analysis_pipeline.py` | `AnalysisPipeline` (AX-1 knowledge orchestration) |
| `canonical_pipeline.py` | `CanonicalPipeline` (AX-2 end-to-end orchestration) |
| `stage_registry.py` | `CanonicalStageRegistry` |
| `package_contract.py` | `PackageContractVerifier` |
| `diagnostics.py` | Structured AX-2 diagnostic codes |
| `execution_report.py` | `CanonicalAnalysisResult`, `ExecutionTrace` |
| `package_loader.py` | `PackageLoader`, `LoadedPackage` |
| `dependency_resolver.py` | Knowledge Dependency Map resolver |

See `engines/analysis_engine/ANALYSIS_PIPELINE.md` and `documentation/ANALYSIS_PIPELINE_V2.md`.

Orchestration only. No rule evaluation, BaZi logic, or scoring algorithms.
