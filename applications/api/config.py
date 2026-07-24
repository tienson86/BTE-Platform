"""Applications API configuration."""

from __future__ import annotations

from pydantic import BaseModel


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
    log_level: str = "INFO"


settings = APISettings()
