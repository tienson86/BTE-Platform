"""JSON knowledge loader for interpretation knowledge system."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.interpretation_engine.foundation.knowledge.entity import (
    KnowledgeEntity,
    KnowledgeMetadata,
)
from engines.interpretation_engine.foundation.references import KnowledgeEntityReference
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus


class KnowledgeLoadError(Exception):
    """Raised when knowledge files cannot be loaded."""


class JsonKnowledgeLoader:
    """Load KnowledgeEntity records from JSON files."""

    def __init__(self, root: Path) -> None:
        """Bind loader to knowledge root directory."""
        self._root = root

    @property
    def root(self) -> Path:
        """Return knowledge root path."""
        return self._root

    def load_registry(self) -> dict[str, Any]:
        """Load knowledge_registry.json."""
        path = self._root / "knowledge_registry.json"
        if not path.is_file():
            raise KnowledgeLoadError(f"missing registry: {path}")
        return self._read_json(path)

    def load_domain_entities(self, domain: str, source_path: str) -> list[KnowledgeEntity]:
        """Load all JSON entities for one domain source path."""
        domain_dir = self._root / source_path
        if not domain_dir.is_dir():
            return []
        entities: list[KnowledgeEntity] = []
        for path in sorted(domain_dir.glob("*.json")):
            payload = self._read_json(path)
            entity = self._parse_entity(payload)
            if entity.domain != domain:
                raise KnowledgeLoadError(
                    f"domain mismatch in {path}: expected {domain}, got {entity.domain}"
                )
            entities.append(entity)
        return entities

    def load_all(self) -> list[KnowledgeEntity]:
        """Load all entities declared in registry sources."""
        registry = self.load_registry()
        entities: list[KnowledgeEntity] = []
        for source in registry.get("sources") or []:
            if not isinstance(source, Mapping):
                continue
            if str(source.get("format") or "json") != "json":
                continue
            domain = str(source.get("domain") or "")
            path = str(source.get("path") or "")
            if domain and path:
                entities.extend(self.load_domain_entities(domain, path))
        return entities

    def _parse_entity(self, payload: Mapping[str, Any]) -> KnowledgeEntity:
        """Parse one JSON object into KnowledgeEntity."""
        meta_raw = dict(payload.get("metadata") or {})
        status_raw = str(meta_raw.get("status") or "draft")
        try:
            status = KnowledgeStatus(status_raw)
        except ValueError as exc:
            raise KnowledgeLoadError(f"invalid status: {status_raw}") from exc

        related: list[KnowledgeEntityReference] = []
        for item in payload.get("related_entities") or []:
            if isinstance(item, Mapping):
                related.append(
                    KnowledgeEntityReference(
                        domain=str(item.get("domain") or ""),
                        key=str(item.get("key") or ""),
                    )
                )

        apps = payload.get("applications") or {}
        if not isinstance(apps, Mapping):
            apps = {}

        recs = tuple(
            dict(item)
            for item in (payload.get("recommendations") or [])
            if isinstance(item, Mapping)
        )
        warns = tuple(
            dict(item)
            for item in (payload.get("warnings") or [])
            if isinstance(item, Mapping)
        )

        concept_ids = tuple(
            str(item)
            for item in (payload.get("concept_ids") or [])
            if str(item)
        )
        contraindications = tuple(
            dict(item)
            for item in (payload.get("contraindications") or [])
            if isinstance(item, Mapping)
        )
        activation_conditions = _string_tuple(payload.get("activation_conditions"))
        typical_triggers = _string_tuple(payload.get("typical_triggers"))
        suppression_conditions = _string_tuple(payload.get("suppression_conditions"))
        interaction_conditions = _string_tuple(payload.get("interaction_conditions"))

        return KnowledgeEntity(
            id=str(payload.get("id") or ""),
            domain=str(payload.get("domain") or ""),
            key=str(payload.get("key") or ""),
            title=str(payload.get("title") or ""),
            meaning=str(payload.get("meaning") or ""),
            positive_meaning=str(payload.get("positive_meaning") or ""),
            negative_meaning=str(payload.get("negative_meaning") or ""),
            applications=dict(apps),
            recommendations=recs,
            warnings=warns,
            related_entities=tuple(related),
            concept_ids=concept_ids,
            evidence_notes=str(payload.get("evidence_notes") or ""),
            entity_type=str(payload.get("entity_type") or ""),
            mechanism=str(payload.get("mechanism") or ""),
            manifestation=str(payload.get("manifestation") or ""),
            contraindications=contraindications,
            activation_conditions=activation_conditions,
            typical_triggers=typical_triggers,
            luck_relationship=str(payload.get("luck_relationship") or ""),
            pattern_relationship=str(payload.get("pattern_relationship") or ""),
            ten_gods_relationship=str(payload.get("ten_gods_relationship") or ""),
            suppression=str(payload.get("suppression") or ""),
            base_influence=str(payload.get("base_influence") or ""),
            conditional_influence=str(payload.get("conditional_influence") or ""),
            activation_dependency=str(payload.get("activation_dependency") or ""),
            suppression_conditions=suppression_conditions,
            interaction_conditions=interaction_conditions,
            relationship_notes=str(payload.get("relationship_notes") or ""),
            metadata=KnowledgeMetadata(
                author=str(meta_raw.get("author") or ""),
                version=str(meta_raw.get("version") or ""),
                status=status,
                source=str(meta_raw.get("source") or ""),
                created=str(meta_raw.get("created") or ""),
                updated=str(meta_raw.get("updated") or ""),
                quality=str(meta_raw.get("quality") or ""),
            ),
        )

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        """Read JSON file."""
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise KnowledgeLoadError(f"cannot read {path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise KnowledgeLoadError(f"invalid json object: {path}")
        return raw


def _string_tuple(value: Any) -> tuple[str, ...]:
    """Copy a JSON string list into a tuple."""
    if not value:
        return ()
    return tuple(str(item) for item in value if str(item).strip())
