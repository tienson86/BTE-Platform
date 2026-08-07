"""Sentence selection from Pack 04 sentence library."""

from __future__ import annotations

from typing import Any

from .library_loader import NarrativeLibrary


class SentenceSelector:
    """Stage — Sentence Selection."""

    def __init__(self, library: NarrativeLibrary | None = None) -> None:
        self.library = library or NarrativeLibrary()

    def select(self, matched_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Resolve matched rules to sentence templates.

        Returns list of {rule, sentence} payloads.
        """
        catalog = self.library.load_sentences()
        selected: list[dict[str, Any]] = []
        for rule in matched_rules:
            sentence_id = str(rule.get("sentence_id") or "")
            sentence = catalog.get(sentence_id)
            if sentence is None:
                continue
            selected.append({"rule": rule, "sentence": dict(sentence)})
        return selected
