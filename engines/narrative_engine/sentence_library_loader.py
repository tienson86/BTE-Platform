"""Read-only loader for Knowledge ``07_sentence_library``."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def default_sentence_library_root() -> Path:
    """Resolve ``knowledge/07_sentence_library``."""
    return (
        Path(__file__).resolve().parents[1]
        / "interpretation_engine"
        / "knowledge"
        / "07_sentence_library"
    )


@dataclass(slots=True)
class SentenceModule:
    """One sentence-library module folder."""

    module_id: str
    module_name: str
    module_title: str
    path: Path
    metadata: dict[str, Any] = field(default_factory=dict)
    index: dict[str, Any] = field(default_factory=dict)
    labels: dict[str, Any] = field(default_factory=dict)
    examples: dict[str, Any] = field(default_factory=dict)

    def label_display(self, label_code: str, default: str = "") -> str:
        """Resolve display_name for label_code."""
        for label in self.labels.get("labels") or []:
            if str(label.get("label_code")) == label_code and label.get("enabled", True):
                return str(
                    label.get("display_name")
                    or label.get("label_name")
                    or default
                )
        return default

    def labels_by_code(self) -> dict[str, dict[str, Any]]:
        """Map label_code → label row."""
        result: dict[str, dict[str, Any]] = {}
        for label in self.labels.get("labels") or []:
            code = str(label.get("label_code") or "")
            if code:
                result[code] = dict(label)
        return result

    def enabled_sentences(self) -> list[dict[str, Any]]:
        """Return enabled sentence definitions (index file_ref or enabled examples)."""
        sentences: list[dict[str, Any]] = []
        for entry in self.index.get("sentences") or self.index.get("templates") or []:
            if not entry.get("enabled", True):
                continue
            file_ref = entry.get("file_ref")
            if file_ref:
                path = self.path / str(file_ref)
                if path.exists():
                    try:
                        payload = json.loads(path.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        continue
                    if isinstance(payload, dict):
                        sentences.append(payload)
        for item in self.examples.get("examples") or []:
            sentence = item.get("sentence")
            if isinstance(sentence, dict) and sentence.get("enabled", False):
                sentences.append(sentence)
        return sentences


class SentenceLibraryLoader:
    """Load sentence schema, modules, labels (read-only)."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else default_sentence_library_root()
        self._schema: dict[str, Any] | None = None
        self._modules: dict[str, SentenceModule] | None = None

    def load_schema(self) -> dict[str, Any]:
        """Load ``sentence_schema.json``."""
        if self._schema is not None:
            return self._schema
        path = self.root / "sentence_schema.json"
        self._schema = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return self._schema

    def tones(self) -> tuple[str, ...]:
        """Allowed tones from schema."""
        return tuple(str(item) for item in (self.load_schema().get("tones") or ["neutral"]))

    def intents(self) -> tuple[str, ...]:
        """Allowed intents from schema."""
        return tuple(str(item) for item in (self.load_schema().get("intents") or ["describe"]))

    def load_modules(self) -> dict[str, SentenceModule]:
        """Load all sentence modules."""
        if self._modules is not None:
            return self._modules
        modules: dict[str, SentenceModule] = {}
        if not self.root.exists():
            logger.warning("Sentence library missing: %s", self.root)
            self._modules = modules
            return modules
        for path in sorted(self.root.iterdir()):
            if not path.is_dir():
                continue
            metadata_path = path / "metadata.json"
            if not metadata_path.exists():
                continue
            metadata = self._read_json(metadata_path)
            module = SentenceModule(
                module_id=str(metadata.get("module_id") or path.name),
                module_name=str(metadata.get("module_name") or path.name),
                module_title=str(
                    metadata.get("module_title")
                    or metadata.get("module_name")
                    or path.name
                ),
                path=path,
                metadata=metadata,
                index=self._read_json(path / "sentence_index.json"),
                labels=self._read_json(path / "sentence_labels.json"),
                examples=self._read_json(path / "sentence_examples.json"),
            )
            modules[module.module_id] = module
            modules[module.module_name] = module
        self._modules = modules
        return modules

    def get_module(self, module_id_or_name: str) -> SentenceModule | None:
        """Lookup by module id or name."""
        return self.load_modules().get(module_id_or_name)

    def transition_module(self) -> SentenceModule | None:
        """Return ``02_transition`` module."""
        return self.get_module("02_transition") or self.get_module("transition")

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed reading %s: %s", path, exc)
            return {}
        return data if isinstance(data, dict) else {}
