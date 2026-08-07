"""Load Pack 04 sentence library and narrative rules (read-only)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


_LIBRARY_DIR = Path(__file__).resolve().parent / "library"


class NarrativeLibrary:
    """Knowledge loader for Pack 04 narrative assets."""

    def __init__(self, library_dir: str | Path | None = None) -> None:
        self.library_dir = Path(library_dir) if library_dir else _LIBRARY_DIR
        self._sentences: dict[str, dict[str, Any]] | None = None
        self._rules: list[dict[str, Any]] | None = None

    def load_sentences(self) -> dict[str, dict[str, Any]]:
        """Return sentence catalog keyed by sentence_id."""
        if self._sentences is not None:
            return self._sentences
        path = self.library_dir / "sentences.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        catalog: dict[str, dict[str, Any]] = {}
        for item in payload.get("sentences") or []:
            sentence_id = str(item.get("sentence_id") or "")
            if sentence_id:
                catalog[sentence_id] = dict(item)
        self._sentences = catalog
        return catalog

    def load_rules(self) -> list[dict[str, Any]]:
        """Return narrative matching rules sorted by priority desc."""
        if self._rules is not None:
            return self._rules
        path = self.library_dir / "narrative_rules.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        rules = [dict(item) for item in (payload.get("rules") or [])]
        rules.sort(key=lambda row: int(row.get("priority") or 0), reverse=True)
        self._rules = rules
        return rules
