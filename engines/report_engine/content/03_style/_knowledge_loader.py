"""Load Dictionary + Terminology + Sentence Library assets for Style Layer."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from .style_models import StyleKnowledge

logger = logging.getLogger(__name__)


def _knowledge_root() -> Path:
    return (
        Path(__file__).resolve().parents[3]
        / "interpretation_engine"
        / "knowledge"
    )


class StyleKnowledgeLoader:
    """
    Read-only loader.

    - Terminology / Dictionary → protected terms + alias→canonical synonyms
    - Sentence Library → tones + emphasis/warning/positive labels
    """

    def __init__(self, knowledge_root: str | Path | None = None) -> None:
        self.root = Path(knowledge_root) if knowledge_root else _knowledge_root()

    def load(self) -> StyleKnowledge:
        """Build StyleKnowledge from KB files."""
        protected: set[str] = set()
        synonym_map: dict[str, str] = {}

        terminology_dir = self.root / "03_terminology"
        dictionary_dir = self.root / "02_dictionary"
        sentence_dir = self.root / "07_sentence_library"

        if terminology_dir.exists():
            for path in sorted(terminology_dir.glob("*.json")):
                self._ingest_terminology(self._read_json(path), protected, synonym_map)

        if dictionary_dir.exists():
            for path in sorted(dictionary_dir.glob("*.json")):
                self._ingest_dictionary(self._read_json(path), protected, synonym_map)

        tones = ("neutral", "positive", "negative", "professional", "friendly", "serious")
        emphasis_label = "emphasis"
        warning_label = "warning"
        positive_label = "positive"
        schema_path = sentence_dir / "sentence_schema.json"
        if schema_path.exists():
            schema = self._read_json(schema_path)
            if isinstance(schema, dict) and schema.get("tones"):
                tones = tuple(str(item) for item in schema["tones"])

        transition_labels = sentence_dir / "02_transition" / "sentence_labels.json"
        labels_payload = self._read_json(transition_labels)
        if isinstance(labels_payload, dict):
            for label in labels_payload.get("labels") or []:
                code = str(label.get("label_code") or "")
                display = str(label.get("display_name") or label.get("label_name") or "")
                if not display:
                    continue
                if code == "emphasis":
                    emphasis_label = display
                elif code == "warning":
                    warning_label = display
                elif code == "positive":
                    positive_label = display

        # Longest-first matching later — store unique keys
        return StyleKnowledge(
            protected_terms=tuple(sorted(protected, key=len, reverse=True)),
            synonym_map=synonym_map,
            tones=tones,
            emphasis_label=emphasis_label,
            warning_label=warning_label,
            positive_label=positive_label,
        )

    def _ingest_terminology(
        self,
        payload: Any,
        protected: set[str],
        synonym_map: dict[str, str],
    ) -> None:
        rows = payload if isinstance(payload, list) else []
        if isinstance(payload, dict):
            rows = payload.get("terms") or payload.get("items") or []
        for row in rows:
            if not isinstance(row, dict):
                continue
            term = str(row.get("term") or row.get("display_name") or "").strip()
            if not term:
                continue
            protected.add(term)
            for alias in row.get("aliases") or []:
                alias_text = str(alias).strip()
                if not alias_text or alias_text == term:
                    continue
                protected.add(alias_text)
                # Alias → canonical term (expression normalization, same meaning)
                synonym_map.setdefault(alias_text, term)

    def _ingest_dictionary(
        self,
        payload: Any,
        protected: set[str],
        synonym_map: dict[str, str],
    ) -> None:
        if not isinstance(payload, dict):
            if isinstance(payload, list):
                for row in payload:
                    if isinstance(row, dict):
                        self._ingest_term_row(row, protected, synonym_map)
            return
        # glossary style
        for row in payload.get("terms") or []:
            if isinstance(row, dict):
                self._ingest_term_row(row, protected, synonym_map)
        # grouped dictionaries (ten_gods, patterns, ...)
        groups = payload.get("groups")
        if isinstance(groups, dict):
            iterable = groups.values()
        elif isinstance(groups, list):
            iterable = [groups]
        else:
            iterable = []
        for group in iterable:
            if not isinstance(group, list):
                continue
            for row in group:
                if isinstance(row, dict):
                    self._ingest_term_row(row, protected, synonym_map)
        # top-level list-like keys
        for key in ("items", "entries", "data"):
            rows = payload.get(key)
            if isinstance(rows, list):
                for row in rows:
                    if isinstance(row, dict):
                        self._ingest_term_row(row, protected, synonym_map)

    def _ingest_term_row(
        self,
        row: dict[str, Any],
        protected: set[str],
        synonym_map: dict[str, str],
    ) -> None:
        display = str(
            row.get("display_name") or row.get("name") or row.get("term") or ""
        ).strip()
        if display:
            protected.add(display)
        for alias in row.get("aliases") or []:
            alias_text = str(alias).strip()
            if alias_text and display and alias_text != display:
                protected.add(alias_text)
                synonym_map.setdefault(alias_text, display)

    @staticmethod
    def _read_json(path: Path) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Style KB read failed %s: %s", path, exc)
            return {}
