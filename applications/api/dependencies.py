"""FastAPI dependency providers."""

from __future__ import annotations

from functools import lru_cache

from applications.api.config import APISettings, settings
from applications.api.services.orchestrator import OrchestratorService


@lru_cache(maxsize=1)
def get_settings() -> APISettings:
    """Return cached API settings."""
    return settings


@lru_cache(maxsize=1)
def get_orchestrator() -> OrchestratorService:
    """Return shared orchestrator (engine facades only)."""
    return OrchestratorService()
