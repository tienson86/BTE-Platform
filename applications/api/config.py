"""Applications API configuration."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field


class APISettings(BaseModel):
    """Runtime settings for Applications API V1."""

    app_name: str = "BTE Applications API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    default_timezone: str = "Asia/Ho_Chi_Minh"
    request_id_header: str = "X-Request-ID"
    elapsed_header: str = "X-Elapsed-Ms"
    api_key_header: str = "X-API-Key"
    log_level: str = "INFO"

    # JWT (secret from env when set; otherwise development default)
    jwt_secret: str = Field(
        default_factory=lambda: os.getenv(
            "BTE_JWT_SECRET",
            "bte-dev-jwt-secret-change-me",
        )
    )
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "bte-applications-api"
    jwt_audience: str = "bte-clients"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Password hashing
    password_hash_iterations: int = 120_000
    password_salt_bytes: int = 16

    # WP11 JSON data root (override with BTE_DATA_DIR)
    data_dir: str = Field(
        default_factory=lambda: os.getenv(
            "BTE_DATA_DIR",
            str(
                Path(__file__).resolve().parents[1]
                / "data"
            ),
        )
    )


settings = APISettings()
