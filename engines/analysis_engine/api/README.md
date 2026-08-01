# API Package

> **Path:** `engines/analysis_engine/api/`

Public API surface for Analysis Engine.

## Architecture Facade

| Module | Surface |
|--------|---------|
| `analysis_engine.py` | `AnalysisEngineAPI` |
| `analysis_service.py` | `AnalysisService` (architecture facade) |
| `analysis_session.py` | `AnalysisSession` |
| `analysis_request.py` | `AnalysisRequest` |
| `analysis_response.py` | `AnalysisResponse` |

Facade only. No BaZi business implementation.

## Legacy FastAPI (coexistence)

| Path | Role |
|------|------|
| `app.py` | FastAPI application |
| `routes/` | HTTP routes |
| `services/` | Legacy HTTP services (includes a different `AnalysisService`) |
| `schemas.py` | Pydantic HTTP schemas |

Architecture facade types are distinct from Pydantic `schemas.AnalysisRequest`
and from `services.analysis_service.AnalysisService`.
