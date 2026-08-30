"""Rewrite strategy registry. Registration order is the fallback."""

from __future__ import annotations

from engines.narrative_v2.rewrite.rewrite_strategy import ALLOWED_STRATEGIES


class RewriteRegistry:
    """Documented rewrite strategies. Does not invent strategies."""

    def __init__(self, strategies: tuple[str, ...] | None = None) -> None:
        self._strategies = strategies or tuple(sorted(ALLOWED_STRATEGIES))

    def strategies(self) -> tuple[str, ...]:
        """Return registered strategy names."""
        return self._strategies

    def contains(self, strategy: str) -> bool:
        """True when the strategy is registered."""
        return strategy in self._strategies
