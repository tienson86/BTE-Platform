"""Sentence Library selector.

N-IMP-05: interface only. No invented runtime library.
"""

from __future__ import annotations

from engines.narrative_v2.rewrite.language_profile import LanguageProfile


class SentenceSelector:
    """Select an approved customer sentence. Returns None when the library is missing."""

    def select(
        self,
        semantic_key: str,
        *,
        profile: LanguageProfile,
    ) -> str | None:
        """Return a library sentence, or None when none is approved for runtime."""
        del semantic_key, profile
        return None
