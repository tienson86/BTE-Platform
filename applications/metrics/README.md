# Metrics

Version: 1.0.0  
Sprint: Beta-3

Catalog only. No Prometheus client, no `/metrics` implementation, no pipeline hooks.

| Domain | Metrics |
|--------|---------|
| API | `request_count`, `request_latency`, `error_rate`, `availability` |
| Pipeline | `analysis_duration`, `decision_duration`, `luck_duration`, `interpretation_duration`, `report_duration` |
| System | `cpu`, `memory`, `disk`, `network` |

External scrape of existing `/health` remains a deployment concern (`deployment/monitoring/`).

---

END
