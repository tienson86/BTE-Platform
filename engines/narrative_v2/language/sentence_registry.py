"""Sentence asset registry. Loads approved JSON files. No generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engines.narrative_v2.language.language_asset_status import SENTENCE_LIBRARY_VERSION
from engines.narrative_v2.language.sentence_asset import SentenceAsset, SentenceReference

_REPO_ROOT = Path(__file__).resolve().parents[3]
ASSET_ROOT = (
    _REPO_ROOT
    / "knowledge"
    / "narrative_v2"
    / "runtime_assets"
    / "vi"
    / "sentence_library"
)


class SentenceRegistry:
    """Index of runtime sentence assets. Loader only."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = root or ASSET_ROOT
        self._assets: tuple[SentenceAsset, ...] | None = None

    def assets(self) -> tuple[SentenceAsset, ...]:
        """Return loaded assets in stable sentence_id order."""
        if self._assets is None:
            loaded = [_from_payload(path, json.loads(path.read_text(encoding="utf-8"))) for path in _json_files(self._root)]
            self._assets = tuple(sorted(loaded, key=lambda item: item.sentence_id))
        return self._assets

    def version(self) -> str:
        """Return the library version from manifest or the package default."""
        manifest = self._root / "manifest.json"
        if not manifest.is_file():
            return SENTENCE_LIBRARY_VERSION
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        return str(payload.get("sentence_library_version", SENTENCE_LIBRARY_VERSION))


def _json_files(root: Path) -> tuple[Path, ...]:
    if not root.is_dir():
        return ()
    return tuple(
        sorted(
            path
            for path in root.rglob("*.json")
            if path.name != "manifest.json"
        )
    )


def _from_payload(path: Path, payload: Any) -> SentenceAsset:
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid sentence asset: {path}")
    refs = tuple(
        SentenceReference(
            knowledge_id=str(entry.get("knowledge_id", "")),
            source_path=str(entry.get("source_path", "")),
        )
        for entry in payload.get("references", ())
        if isinstance(entry, dict)
    )
    knowledge_ids = tuple(str(item) for item in payload.get("source_knowledge_ids", ()))
    meta = payload.get("metadata") or {}
    metadata = tuple((str(key), str(value)) for key, value in meta.items())
    return SentenceAsset(
        sentence_id=str(payload.get("sentence_id", "")),
        semantic_key=str(payload.get("semantic_key", "")),
        domain=str(payload.get("domain", "")),
        category=str(payload.get("category", "")),
        meaning_key=str(payload.get("meaning_key", "")),
        text=str(payload.get("text", "")),
        locale=str(payload.get("locale", "vi")),
        audience=str(payload.get("audience", "customer")),
        style=str(payload.get("style", "consultant")),
        status=str(payload.get("status", "")),
        priority=int(payload.get("priority", 0)),
        source_knowledge_ids=knowledge_ids,
        references=refs,
        version=str(payload.get("version", SENTENCE_LIBRARY_VERSION)),
        metadata=metadata,
    )
