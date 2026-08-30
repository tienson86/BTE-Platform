"""Load approved interpretation knowledge files. Read-only. No network."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Mapping

from engines.narrative_v2.knowledge.knowledge_index import IndexedKnowledge, KnowledgeIndex
from engines.narrative_v2.knowledge.knowledge_registry import normalize_domain
from engines.narrative_v2.knowledge.knowledge_status import (
    ELIGIBLE_SOURCE_STATUSES,
    STATUS_APPROVED,
)

logger = logging.getLogger(__name__)

_REPO_ROOT = Path(__file__).resolve().parents[3]
DOMAIN_ROOT = _REPO_ROOT / "knowledge" / "interpretation" / "domains"

_INDEX_CACHE: KnowledgeIndex | None = None


class KnowledgeLoader:
    """Load and cache approved JSON knowledge. Version-aware. Analysis-free."""

    def __init__(self, roots: tuple[Path, ...] | None = None) -> None:
        self._roots = roots if roots is not None else (DOMAIN_ROOT,)

    def load_index(self, *, use_cache: bool = True) -> KnowledgeIndex:
        """Build a deterministic approved-knowledge index."""
        global _INDEX_CACHE
        if use_cache and _INDEX_CACHE is not None and self._roots == (DOMAIN_ROOT,):
            return _INDEX_CACHE
        records = tuple(self._load_records())
        index = KnowledgeIndex(records)
        if use_cache and self._roots == (DOMAIN_ROOT,):
            _INDEX_CACHE = index
        return index

    def _load_records(self) -> list[IndexedKnowledge]:
        records: list[IndexedKnowledge] = []
        seen_ids: set[str] = set()
        for path in _iter_json_files(self._roots):
            payload = _read_json(path)
            if payload is None:
                continue
            record = _record_from_payload(payload, path)
            if record is None:
                continue
            if record.knowledge_id in seen_ids:
                continue
            seen_ids.add(record.knowledge_id)
            records.append(record)
        records.sort(key=lambda item: item.knowledge_id)
        logger.debug("Loaded %s approved knowledge records", len(records))
        return records


def _iter_json_files(roots: tuple[Path, ...]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.json")):
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            files.append(resolved)
    files.sort()
    return files


def _read_json(path: Path) -> Mapping[str, Any] | None:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.debug("Skipping unreadable knowledge file %s", path)
        return None
    if not isinstance(raw, Mapping):
        return None
    return raw


def _record_from_payload(
    payload: Mapping[str, Any],
    path: Path,
) -> IndexedKnowledge | None:
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    status = metadata.get("status")
    if status not in ELIGIBLE_SOURCE_STATUSES:
        return None
    knowledge_id = str(payload.get("id") or "").strip()
    key = str(payload.get("key") or "").strip()
    domain = str(payload.get("domain") or "").strip()
    if not knowledge_id or not key or not domain:
        return None
    version_raw = metadata.get("version")
    version = str(version_raw).strip() if version_raw not in (None, "") else None
    source_path = str(metadata.get("source") or _relative_source(path))
    aliases = _aliases(knowledge_id, key)
    customer = payload.get("customer_meaning")
    customer_text = str(customer).strip() if isinstance(customer, str) and customer.strip() else None
    meaning = payload.get("meaning")
    technical = str(meaning).strip() if isinstance(meaning, str) and meaning.strip() else None
    return IndexedKnowledge(
        knowledge_id=knowledge_id,
        domain=normalize_domain(domain),
        key=key,
        knowledge_type="meaning",
        status=STATUS_APPROVED,
        technical_meaning=technical,
        customer_meaning_candidate=customer_text,
        boundaries=_boundary_copies(payload),
        recommendations=_recommendation_copies(payload),
        source_path=source_path,
        version=version,
        aliases=aliases,
    )


def _aliases(knowledge_id: str, key: str) -> tuple[str, ...]:
    suffix = knowledge_id.rsplit(".", 1)[-1]
    aliases = []
    if suffix and suffix != key:
        aliases.append(suffix)
    return tuple(aliases)


def _recommendation_copies(payload: Mapping[str, Any]) -> tuple[str, ...]:
    raw = payload.get("recommendations")
    if not isinstance(raw, list):
        return ()
    copied: list[str] = []
    for entry in raw:
        if not isinstance(entry, Mapping):
            continue
        action = entry.get("action")
        if isinstance(action, str) and action.strip():
            copied.append(action.strip())
    return tuple(copied)


def _boundary_copies(payload: Mapping[str, Any]) -> tuple[str, ...]:
    copied: list[str] = []
    warnings = payload.get("warnings")
    if isinstance(warnings, list):
        for entry in warnings:
            if not isinstance(entry, Mapping):
                continue
            risk = entry.get("risk")
            if isinstance(risk, str) and risk.strip():
                copied.append(risk.strip())
    contra = payload.get("contraindications")
    if isinstance(contra, list):
        for entry in contra:
            if not isinstance(entry, Mapping):
                continue
            avoid = entry.get("avoid")
            if isinstance(avoid, str) and avoid.strip():
                copied.append(avoid.strip())
    return tuple(copied)


def _relative_source(path: Path) -> str:
    try:
        return path.relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()
