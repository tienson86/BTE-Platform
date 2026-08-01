"""Sentence runtime selector shell.

Selects registered sentence-ref ids structurally. No sentence library / NLG.
"""

from __future__ import annotations

from engines.interpretation_engine.sentence_runtime.registry import SentenceRuntimeRegistry


class SentenceRuntimeSelector:
    """Select sentence-ref ids from the injected registry."""

    def __init__(self, registry: SentenceRuntimeRegistry) -> None:
        """Initialize with registry dependency."""
        self._registry = registry

    def select(self, *, domain: str | None = None) -> tuple[str, ...]:
        """Return registered ids, optionally filtered by domain metadata."""
        selected: list[str] = []
        for entry_id in self._registry.list():
            entry = self._registry.lookup(entry_id)
            if domain is None:
                selected.append(entry_id)
                continue
            meta_domain = None
            if isinstance(entry, dict):
                meta_domain = entry.get("domain")
            if meta_domain == domain:
                selected.append(entry_id)
        return tuple(selected)
