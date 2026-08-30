"""Deterministic rewrite strategy selection."""

from __future__ import annotations

from engines.narrative_v2.rewrite.language_profile import LanguageProfile
from engines.narrative_v2.rewrite.rewrite_strategy import (
    STRATEGY_CLARIFICATION,
    STRATEGY_PROFESSIONALIZATION,
)


class RewriteSelector:
    """Choose one documented strategy. No random variants. No language-model calls."""

    def select(
        self,
        *,
        source_meaning: str,
        profile: LanguageProfile,
    ) -> str:
        """Return clarification when address must be added, else professionalization."""
        del profile
        text = source_meaning.strip()
        if text.startswith("Bạn"):
            return STRATEGY_PROFESSIONALIZATION
        return STRATEGY_CLARIFICATION
