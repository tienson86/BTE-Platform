"""Customer Portal configuration."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field

PORTAL_ROOT = Path(__file__).resolve().parent


class PortalSettings(BaseModel):
    """UI process settings (API is separate)."""

    api_base_url: str = Field(
        default_factory=lambda: os.getenv(
            "BTE_API_BASE_URL",
            "http://127.0.0.1:8000",
        )
    )
    host: str = "127.0.0.1"
    port: int = 8081
    title: str = "BTE Portal"


settings = PortalSettings()
