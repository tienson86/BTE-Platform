# Service Layer

Version: 1.0.0  
Sprint: Beta-2

## Services

- `AnalysisService`
- `ReportService`
- `KnowledgeService`
- `HealthService`

Registered by `ServiceRegistry`.

## Pipeline rule

Every service calls canonical pipelines **only**, through `CanonicalPipelinePort`.

Default binding: `UnboundPipelineGateway`

- Validates and acknowledges requests
- Does not execute engines
- Does not persist resources
- Does not import knowledge packages

Runtime hosts replace the gateway with an adapter that invokes canonical pipeline public entry points.

## Forbidden

- Engine internal imports
- Knowledge package imports
- Report rendering
- Business rule evaluation
- Direct database or CSV access

See [`../services/README.md`](../services/README.md).

---

END
