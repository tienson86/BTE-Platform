"""Deterministic consulting-frame selection."""

from __future__ import annotations

from engines.narrative_v2.communication.consulting_style_profile import ConsultingStyleProfile
from engines.narrative_v2.communication.consulting_style_registry import (
    FRAGMENT_OPENERS,
    LANGUAGE_ISSUE_APPROVED,
    LANGUAGE_ISSUE_SENTENCE_GAP,
    LANGUAGE_ISSUE_SHORTHAND,
    ConsultingStyleRegistry,
)


class ConsultingStyleSelector:
    """Select one approved frame from role, issue class, and profile."""

    def __init__(self, registry: ConsultingStyleRegistry | None = None) -> None:
        self._registry = registry or ConsultingStyleRegistry()

    def select(
        self,
        *,
        role: str,
        source_text: str,
        prior_fragment: bool,
        profile: ConsultingStyleProfile,
    ) -> str:
        """Return a frame_id. Same inputs → same frame."""
        del profile
        issue = classify_language_issue(source_text)
        if role == "observation":
            return "frame.observation.highlight"
        if role == "reasoning":
            return "frame.reasoning.shows"
        if role == "meaning":
            if issue == LANGUAGE_ISSUE_SENTENCE_GAP:
                return "frame.meaning.practice"
            return "frame.positive.side"
        if role == "impact":
            return "frame.impact.when"
        if role == "recommendation":
            if prior_fragment or issue == LANGUAGE_ISSUE_SENTENCE_GAP:
                return "frame.recommendation.note"
            return "frame.observation.notable"
        if role == "closing":
            return "frame.closing.overall"
        return "frame.observation.notable"

    def registry(self) -> ConsultingStyleRegistry:
        """Return the frame registry."""
        return self._registry


def classify_language_issue(text: str) -> str:
    """Classify surface language. Does not invent a replacement meaning."""
    stripped = text.strip()
    for opener in FRAGMENT_OPENERS:
        if stripped.startswith(opener):
            return LANGUAGE_ISSUE_SENTENCE_GAP
    if _looks_like_shorthand(stripped):
        return LANGUAGE_ISSUE_SHORTHAND
    return LANGUAGE_ISSUE_APPROVED


def _looks_like_shorthand(text: str) -> bool:
    clauses = [part.strip() for part in text.replace("Bạn có ", "").split(",") if part.strip()]
    compact = [part for part in clauses if 1 <= len(part.split()) <= 6]
    return len(clauses) >= 2 and len(compact) >= 1
