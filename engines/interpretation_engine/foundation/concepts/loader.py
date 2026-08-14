"""JSON concept loader for interpretation concept layer."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.interpretation_engine.foundation.concepts.entity import (
    ConceptEntity,
    ConceptMetadata,
    ConceptRelationship,
)
from engines.interpretation_engine.foundation.concepts.relationships import (
    ConceptRelationshipType,
)
from engines.interpretation_engine.foundation.references import KnowledgeEntityReference
from engines.interpretation_engine.foundation.knowledge.status import KnowledgeStatus


class ConceptLoadError(Exception):
    """Raised when concept files cannot be loaded."""


class JsonConceptLoader:
    """Load ConceptEntity records from JSON files."""

    def __init__(self, root: Path) -> None:
        """Bind loader to concept root directory."""
        self._root = root

    @property
    def root(self) -> Path:
        """Return concept root path."""
        return self._root

    def load_registry(self) -> dict[str, Any]:
        """Load concept_registry.json."""
        path = self._root / "concept_registry.json"
        if not path.is_file():
            raise ConceptLoadError(f"missing registry: {path}")
        return self._read_json(path)

    def load_category_concepts(self, category: str, source_path: str) -> list[ConceptEntity]:
        """Load all JSON concepts for one category source path."""
        category_dir = self._root / source_path
        if not category_dir.is_dir():
            return []
        concepts: list[ConceptEntity] = []
        for path in sorted(category_dir.glob("*.json")):
            payload = self._read_json(path)
            concept = self._parse_concept(payload)
            if concept.category != category:
                raise ConceptLoadError(
                    f"category mismatch in {path}: expected {category}, got {concept.category}"
                )
            concepts.append(concept)
        return concepts

    def load_all(self) -> list[ConceptEntity]:
        """Load all concepts declared in registry sources."""
        registry = self.load_registry()
        concepts: list[ConceptEntity] = []
        for source in registry.get("sources") or []:
            if not isinstance(source, Mapping):
                continue
            if str(source.get("format") or "json") != "json":
                continue
            category = str(source.get("category") or "")
            path = str(source.get("path") or "")
            if category and path:
                concepts.extend(self.load_category_concepts(category, path))
        return concepts

    def _parse_concept(self, payload: Mapping[str, Any]) -> ConceptEntity:
        """Parse one JSON object into ConceptEntity."""
        meta_raw = dict(payload.get("metadata") or {})
        status_raw = str(meta_raw.get("status") or "draft")
        try:
            status = KnowledgeStatus(status_raw)
        except ValueError as exc:
            raise ConceptLoadError(f"invalid status: {status_raw}") from exc

        related_concepts: list[ConceptRelationship] = []
        for item in payload.get("related_concepts") or []:
            if not isinstance(item, Mapping):
                continue
            rel_raw = str(item.get("relationship") or "")
            try:
                rel_type = ConceptRelationshipType(rel_raw)
            except ValueError as exc:
                raise ConceptLoadError(f"invalid relationship: {rel_raw}") from exc
            related_concepts.append(
                ConceptRelationship(
                    target_id=str(item.get("target_id") or ""),
                    relationship=rel_type,
                )
            )

        related_entities: list[KnowledgeEntityReference] = []
        for item in payload.get("related_entities") or []:
            if isinstance(item, Mapping):
                related_entities.append(
                    KnowledgeEntityReference(
                        domain=str(item.get("domain") or ""),
                        key=str(item.get("key") or ""),
                    )
                )

        apps = payload.get("applications") or {}
        if not isinstance(apps, Mapping):
            apps = {}

        conditions = tuple(
            str(item)
            for item in (payload.get("conditions") or [])
            if str(item)
        )

        return ConceptEntity(
            id=str(payload.get("id") or ""),
            category=str(payload.get("category") or ""),
            title=str(payload.get("title") or ""),
            summary=str(payload.get("summary") or ""),
            meaning=str(payload.get("meaning") or ""),
            conditions=conditions,
            applications=dict(apps),
            related_concepts=tuple(related_concepts),
            related_entities=tuple(related_entities),
            metadata=ConceptMetadata(
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
            raise ConceptLoadError(f"cannot read {path}: {exc}") from exc
        if not isinstance(raw, dict):
            raise ConceptLoadError(f"invalid json object: {path}")
        return raw
