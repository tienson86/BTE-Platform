"""Analysis Engine REST API configuration."""

from __future__ import annotations

import os

from pydantic import BaseModel, Field


class AnalysisAPISettings(BaseModel):
    """Runtime settings for Analysis Engine REST API."""

    app_name: str = "BTE Analysis Engine API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    log_level: str = "INFO"

    # When False, endpoints accept anonymous callers with a default role.
    # When True, a valid Bearer JWT is required (JWT-ready enforcement).
    auth_required: bool = Field(
        default_factory=lambda: os.getenv("BTE_ANALYSIS_AUTH_REQUIRED", "0")
        in {"1", "true", "True", "yes"}
    )
    default_anonymous_role: str = "ANALYST"

    jwt_secret: str = Field(
        default_factory=lambda: os.getenv(
            "BTE_ANALYSIS_JWT_SECRET",
            "bte-analysis-dev-jwt-secret-change-me",
        )
    )
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "bte-analysis-engine-api"
    jwt_audience: str = "bte-analysis-clients"
    access_token_expire_minutes: int = 60


settings = AnalysisAPISettings()
