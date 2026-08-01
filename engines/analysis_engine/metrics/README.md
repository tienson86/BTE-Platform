# Metrics Package

> **Path:** `engines/analysis_engine/metrics/`

Infrastructure metrics collectors for Analysis Engine runtime.

## Modules

| Module | Surface |
|--------|---------|
| `execution_metrics.py` | `ExecutionMetrics`, `ExecutionMetricsSnapshot` |
| `performance_metrics.py` | `PerformanceMetrics`, `TimingSample`, snapshot |
| `rule_metrics.py` | `RuleMetrics`, `RuleMetricsSnapshot` |
| `pipeline_metrics.py` | `PipelineMetrics`, `StageMetricRecord`, snapshot |
| `result_metrics.py` | `ResultMetrics`, `ResultMetricsSnapshot` |

Counters, timings, and immutable snapshots only. No dashboards.
