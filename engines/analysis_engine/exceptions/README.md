# Exceptions Package

> **Path:** `engines/analysis_engine/exceptions/`

Analysis Engine exception hierarchy.

```text
AnalysisError
├── ContextError
├── ResultError
├── CacheError
├── RuleError
├── PipelineError
│   ├── PackageLoadError
│   ├── IncompatiblePackageError
│   ├── DependencyViolationError
│   └── DuplicateExecutionError
├── RegistryError
├── ValidationError
├── DecisionError
├── ScoreError
├── ConflictError
└── AnalysisRuntimeError
```

## Modules

`analysis_error.py`, `context_error.py`, `result_error.py`, `cache_error.py`, `rule_error.py`, `pipeline_error.py`,
`registry_error.py`, `validation_error.py`, `decision_error.py`, `score_error.py`,
`conflict_error.py`, `runtime_error.py`

Inheritance only. No business logic.
