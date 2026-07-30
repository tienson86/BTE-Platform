"""Route package."""

from __future__ import annotations

from engines.analysis_engine.api.routes import (
    analysis,
    auth,
    charts,
    health,
    interpretation,
    report,
)

__all__ = [
    "analysis",
    "auth",
    "charts",
    "health",
    "interpretation",
    "report",
]
