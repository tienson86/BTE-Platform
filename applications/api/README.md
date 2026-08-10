# Public API Layer

Version: 1.0.0  
Sprint: Phase XI · Beta-2 — Public Service Platform

This package adds the stable public service API under `/api/v1/`.

Existing Applications API runtime (`applications.api.app:app`) is unchanged in this sprint.

## Mount

```python
from fastapi import FastAPI
from applications.api.api_router import register_public_service_layer

app = FastAPI(title="BTE Public API")
register_public_service_layer(app)
```

Or include the router only:

```python
from applications.api.api_router import public_router

app.include_router(public_router)
```

## Public endpoints

| Method | Path | Service |
|--------|------|---------|
| GET | `/health` | HealthService |
| GET | `/live` | HealthService |
| GET | `/ready` | HealthService |
| GET | `/version` | HealthService |
| GET | `/metrics` | reserved |
| POST | `/api/v1/analysis` | AnalysisService |
| GET | `/api/v1/analysis/{id}` | AnalysisService |
| GET | `/api/v1/report/{id}` | ReportService |
| GET | `/api/v1/knowledge/{id}` | KnowledgeService |

`/api/v2/` is not mounted.

## Design rules

- Design-only service layer. No business logic.
- Routers call public services only.
- Services call canonical pipelines through `CanonicalPipelinePort` only.
- No engine imports. No knowledge package imports.

OpenAPI: `applications/openapi/openapi.yaml`

---

END
