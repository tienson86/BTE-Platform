# Pipeline

Interpretation pipeline contracts and runtime orchestration.

## Runtime modules

| Module | Role |
|--------|------|
| `pipeline.py` | Public pipeline orchestration entry |
| `pipeline_executor.py` | Multi-stage ordered execution |
| `stage_executor.py` | Single-stage prepare → execute → finalize |
| `execution_context.py` | Immutable/mutable orchestration contexts |
| `execution_result.py` | `ExecutionResult` / `StageOutcome` |
| `execution_state.py` | Immutable state + `ExecutionStatus` |
| `execution_policy.py` | Deterministic fail-fast policy |
| `hooks.py` | Lifecycle hooks |
| `stage_base.py` | Abstract stage contract |

Legacy ``InterpretationPipeline`` is re-exported for backward compatibility.

Architecture/runtime orchestration only. No interpretation business logic.
