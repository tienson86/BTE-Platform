"""Semantic repetition prevention. IDs first, then wording."""

from __future__ import annotations


class RepetitionGuard:
    """Track explained findings, catalog keys, actions, and sentence openings."""

    def __init__(self) -> None:
        self._finding_keys: set[str] = set()
        self._catalog_keys: set[str] = set()
        self._action_intents: set[str] = set()
        self._openings: list[str] = []
        self._texts: set[str] = set()

    def claim_finding(self, semantic_key: str | None, finding_id: str) -> bool:
        """Return True once for a finding semantic key."""
        key = semantic_key or finding_id
        if key in self._finding_keys:
            return False
        self._finding_keys.add(key)
        return True

    def explained_finding(self, semantic_key: str | None, finding_id: str) -> bool:
        """Return True when this finding meaning was already explained."""
        key = semantic_key or finding_id
        return key in self._finding_keys

    def claim_catalog(self, catalog_key: str) -> bool:
        """Return True once for a catalog key in the same composition pass."""
        if catalog_key in self._catalog_keys:
            return False
        self._catalog_keys.add(catalog_key)
        return True

    def claim_action(self, action_type: str, objective: str | None) -> bool:
        """Return True once for a recommendation intent."""
        key = f"{action_type}:{objective or ''}"
        if key in self._action_intents:
            return False
        self._action_intents.add(key)
        return True

    def claim_text(self, text: str) -> bool:
        """Return True once for an exact customer sentence."""
        if text in self._texts:
            return False
        self._texts.add(text)
        return True

    def register_text(self, text: str) -> None:
        """Record the sentence opening for later repetition checks."""
        opening = _opening(text)
        if opening:
            self._openings.append(opening)

    def opening_repeats(self, text: str) -> bool:
        """Return True when the last two registered openings match this one."""
        opening = _opening(text)
        if not opening:
            return False
        return len(self._openings) >= 2 and self._openings[-1] == opening and self._openings[-2] == opening


def _opening(text: str) -> str:
    """Return a stable opening key from the first three words."""
    words = text.strip().split()
    return " ".join(words[:3]).lower()
