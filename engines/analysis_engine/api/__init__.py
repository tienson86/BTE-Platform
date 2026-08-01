"""Analysis Engine REST API package and architecture public API facade.

Legacy FastAPI application coexist with architecture facade modules:

- ``analysis_engine.py`` — ``AnalysisEngineAPI``
- ``analysis_service.py`` — architecture ``AnalysisService`` facade
- ``analysis_session.py`` / ``analysis_request.py`` / ``analysis_response.py``

FastAPI application exposing Chart → Analysis → Interpretation → Report.
JWT Ready and Role Ready. Swagger UI and OpenAPI enabled.
"""

from __future__ import annotations

from engines.analysis_engine.api.analysis_engine import AnalysisEngineAPI
from engines.analysis_engine.api.analysis_request import AnalysisRequest
from engines.analysis_engine.api.analysis_response import (
    AnalysisResponse,
    AnalysisResponseStatus,
)
from engines.analysis_engine.api.analysis_service import AnalysisService
from engines.analysis_engine.api.analysis_session import (
    AnalysisSession,
    AnalysisSessionStatus,
)
from engines.analysis_engine.api.app import app, create_app

__all__ = [
    "AnalysisEngineAPI",
    "AnalysisRequest",
    "AnalysisResponse",
    "AnalysisResponseStatus",
    "AnalysisService",
    "AnalysisSession",
    "AnalysisSessionStatus",
    "app",
    "create_app",
]

__version__ = "1.0.0"
