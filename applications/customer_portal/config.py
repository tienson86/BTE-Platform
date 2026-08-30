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
    pack05_legacy: bool = Field(default_factory=lambda: _pack05_legacy())
    host: str = "127.0.0.1"
    port: int = 8081
    title: str = "BTE Portal"


def _narrative_provider() -> str:
    """Production provider is Narrative V2 only. Pack05 flags are ignored."""
    return "v2"


def _pack05_legacy() -> bool:
    """Read-only Pack05 archive flag. Not a production switch."""
    raw = (os.getenv("PACK05_LEGACY") or "").strip().lower()
    return raw in {"1", "true", "pack05", "yes"}


settings = PortalSettings()
