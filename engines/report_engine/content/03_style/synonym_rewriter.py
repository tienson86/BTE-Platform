"""Rewrite expression via Dictionary/Terminology aliases → canonical terms."""

from __future__ import annotations

import re
from typing import Iterable

from .style_models import StyleKnowledge


class SynonymRewriter:
    """
    Normalize expression using KB synonym map only.

    Rules
    -----
    - Never invent wording
    - Only replace known aliases with canonical terms from Dictionary/Terminology
    - Protected canonical terms are never altered into non-KB forms
    - Meaning preserved (alias ≡ term in KB)
    """

    def __init__(self, knowledge: StyleKnowledge) -> None:
        self.knowledge = knowledge
        # Longest alias first to avoid partial clobber
        self._aliases = sorted(
            knowledge.synonym_map.items(),
            key=lambda item: len(item[0]),
            reverse=True,
        )

    def rewrite(self, text: str) -> str:
        """Apply alias→canonical replacements."""
        if not text or not self._aliases:
            return text
        result = text
        for alias, canonical in self._aliases:
            if not alias or alias == canonical:
                continue
            # Skip if alias is somehow empty after strip
            pattern = re.compile(re.escape(alias), flags=re.IGNORECASE)
            result = pattern.sub(canonical, result)
        return result

    def rewrite_many(self, texts: Iterable[str]) -> list[str]:
        """Rewrite a sequence of texts."""
        return [self.rewrite(text) for text in texts]
