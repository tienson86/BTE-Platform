"""Sentence Library selector.

N-IMP-07C: selects approved runtime SentenceAsset records. Never generates prose.
"""

from __future__ import annotations

from engines.narrative_v2.language.sentence_asset import SentenceAsset
from engines.narrative_v2.language.sentence_library import SentenceLibrary
from engines.narrative_v2.rewrite.language_profile import LanguageProfile

DEFAULT_CATEGORY = "meaning"


class SentenceSelector:
    """Select an approved customer sentence. Returns None when none matches."""

    def __init__(self, library: SentenceLibrary | None = None) -> None:
        self._library = library or SentenceLibrary()

    def select(
        self,
        semantic_key: str,
        *,
        profile: LanguageProfile,
        category: str = DEFAULT_CATEGORY,
        domain: str | None = None,
        meaning_key: str | None = None,
    ) -> SentenceAsset | None:
        """Return one approved SentenceAsset, or None when unresolved."""
        return self._library.select(
            semantic_key,
            category=category,
            locale=profile.locale,
            audience=profile.audience,
            domain=domain,
            meaning_key=meaning_key,
        )
