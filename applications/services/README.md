# Public Service Layer

Version: 1.0.0  
Sprint: Phase XI · Beta-2 — Public Service Platform

Public services are the only application entry points that talk to canonical pipelines.

```
API routers
    → AnalysisService / ReportService / KnowledgeService / HealthService
        → CanonicalPipelinePort
            → canonical pipelines (runtime binding)
```

## Services

| Service | Responsibility | Pipeline port |
|---------|----------------|---------------|
| `AnalysisService` | Validate analysis requests; submit/get analysis | `canonical_analysis_pipeline` |
| `ReportService` | Get report by id | `canonical_report_pipeline` |
| `KnowledgeService` | Get published knowledge by id | `canonical_knowledge_pipeline` |
| `HealthService` | `/health` `/live` `/ready` `/version`; reserve `/metrics` | health probe |

## Rules

- Call canonical pipelines **only** through `CanonicalPipelinePort`.
- Never import engine internals.
- Never import knowledge packages.
- Never expose engine objects.
- No business logic in this layer.
- Default binding is `UnboundPipelineGateway` (design-time, no persistence).

## Registry

```python
from applications.services.service_registry import ServiceRegistry

registry = ServiceRegistry.create_default()
```

Runtime hosts inject a bound pipeline adapter. This sprint does not modify pipelines or engines.

---

END
