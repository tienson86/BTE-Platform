"""Web Admin configuration (UI only — talks to REST API)."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field

WEB_ADMIN_ROOT = Path(__file__).resolve().parent


class WebAdminSettings(BaseModel):
    """Runtime settings for the Web Admin UI process."""

    api_base_url: str = Field(
        default_factory=lambda: os.getenv(
            "BTE_API_BASE_URL",
            "http://127.0.0.1:8000",
        )
    )
    host: str = "127.0.0.1"
    port: int = 8080
    title: str = "BTE Web Admin"


settings = WebAdminSettings()
