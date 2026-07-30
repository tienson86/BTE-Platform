# Analysis Engine REST API

**Package:** `engines/analysis_engine/api/`  
**Version:** 1.0.0

## Run

```bash
uvicorn engines.analysis_engine.api.app:app --reload --port 8001
```

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI: `/openapi.json`
- Health: `/health` and `/api/v1/health`

## Endpoints

| Method | Path | Permission |
|--------|------|------------|
| POST | `/api/v1/charts` | `chart.create` |
| GET | `/api/v1/charts/{chart_id}` | `chart.read` |
| POST | `/api/v1/analysis` | `analysis.execute` |
| GET | `/api/v1/analysis/{analysis_id}` | `analysis.read` |
| POST | `/api/v1/interpretation` | `interpretation.execute` |
| GET | `/api/v1/interpretation/{id}` | `interpretation.read` |
| POST | `/api/v1/report` | `report.generate` |
| GET | `/api/v1/report/{report_id}` | `report.read` |
| POST | `/api/v1/auth/token` | `token.issue` |

## JWT Ready / Role Ready

- Bearer JWT via `Authorization: Bearer <token>`
- Roles: `ADMIN`, `ANALYST`, `VIEWER`
- Set `BTE_ANALYSIS_AUTH_REQUIRED=1` to require JWT
- Default (dev/tests): anonymous caller with `ANALYST` role
