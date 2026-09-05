"""MingJu Decision Service."""

from __future__ import annotations

from engines.mingju.engine import MingJuDecisionEngine
from engines.mingju.models import MingJuContext, MingJuDecisionResult


class MingJuDecisionService:
    """Service wrapper around MingJuDecisionEngine."""

    def __init__(self, engine: MingJuDecisionEngine | None = None) -> None:
        self.engine = engine or MingJuDecisionEngine()

    def analyze(self, context: MingJuContext) -> MingJuDecisionResult:
        """Analyze Mệnh Cục from a normalized context."""
        return self.engine.analyze(context)
