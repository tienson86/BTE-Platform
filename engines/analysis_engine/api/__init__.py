"""Analysis Engine REST API package.

FastAPI application exposing Chart → Analysis → Interpretation → Report.

JWT Ready and Role Ready. Swagger UI and OpenAPI enabled.
"""

from __future__ import annotations

from engines.analysis_engine.api.app import app, create_app

__all__ = ["app", "create_app"]

__version__ = "1.0.0"
