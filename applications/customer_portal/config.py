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
    narrative_provider: str = Field(default_factory=lambda: _narrative_provider())
    host: str = "127.0.0.1"
    port: int = 8081
    title: str = "BTE Portal"


def _narrative_provider() -> str:
    """Release flag. Rollback is NARRATIVE_PROVIDER=pack05. No rebuild."""
    raw = (os.getenv("NARRATIVE_PROVIDER") or "v2").strip().lower()
    if raw in {"pack05", "v2", "auto"}:
        return raw
    return "v2"


settings = PortalSettings()
