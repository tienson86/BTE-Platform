"""Load JSON Schema documents from knowledge/schema."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from services.knowledge.cache import MtimeCache
from services.knowledge.constants import (
    DEFAULT_SCHEMA_ROOT_RELATIVE,
    DOMAIN_SCHEMA_MAP,
)
from services.knowledge.exceptions import KnowledgeLoadError, KnowledgeSchemaError
from services.knowledge.models import SchemaDocument

logger = logging.getLogger(__name__)


class SchemaLoader:
    """Load and cache Knowledge Schema Foundation documents."""

    def __init__(self, schema_root: str | Path) -> None:
        """Initialize schema loader."""
        self.schema_root = Path(schema_root).resolve()
        self._cache: MtimeCache[SchemaDocument] = MtimeCache()
        self._registry: Any | None = None

    @classmethod
    def from_project_root(cls, project_root: str | Path) -> SchemaLoader:
        """Build loader from repository root."""
        root = Path(project_root).resolve() / DEFAULT_SCHEMA_ROOT_RELATIVE
        return cls(root)

    def clear_cache(self) -> None:
        """Clear schema and referencing registry caches."""
        self._cache.clear()
        self._registry = None

    def list_schema_paths(self) -> list[Path]:
        """Return all schema JSON files under the schema root."""
        if not self.schema_root.exists():
            raise KnowledgeLoadError(f"Schema root not found: {self.schema_root}")
        return sorted(self.schema_root.glob("*.schema.json"))

    def load_schema(self, name_or_path: str | Path) -> SchemaDocument:
        """Load one schema by filename or absolute/relative path."""
        path = Path(name_or_path)
        if not path.is_absolute():
            path = self.schema_root / path
        path = path.resolve()
        cached = self._cache.get(path)
        if cached is not None:
            return cached
        if not path.exists():
            raise KnowledgeLoadError(f"Schema not found: {path}")
        raw = self._read_json(path)
        doc = SchemaDocument(
            name=path.name,
            path=str(path),
            schema_id=str(raw.get("$id", path.name)),
            raw=raw,
        )
        return self._cache.set(path, doc)

    def load_all(self) -> list[SchemaDocument]:
        """Load every schema document."""
        return [self.load_schema(path) for path in self.list_schema_paths()]

    def schema_for_domain(self, domain_dir: str) -> SchemaDocument:
        """Resolve the module schema for a Canon domain directory."""
        schema_name = DOMAIN_SCHEMA_MAP.get(domain_dir)
        if not schema_name:
            raise KnowledgeSchemaError(
                f"No schema mapping for domain directory: {domain_dir}"
            )
        return self.load_schema(schema_name)

    def build_registry(self) -> Any:
        """Build a referencing.Registry for Draft 2020-12 $ref resolution."""
        if self._registry is not None:
            return self._registry
        try:
            from referencing import Registry, Resource
            from referencing.jsonschema import DRAFT202012
        except ImportError as exc:
            raise KnowledgeSchemaError(
                "referencing/jsonschema required for schema loading"
            ) from exc

        registry = Registry()
        for doc in self.load_all():
            resource = Resource.from_contents(
                doc.raw,
                default_specification=DRAFT202012,
            )
            registry = registry.with_resource(doc.schema_id, resource)
            registry = registry.with_resource(doc.name, resource)
        self._registry = registry
        logger.debug("Built schema registry with %s documents", len(self._cache))
        return registry

    def _read_json(self, path: Path) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise KnowledgeLoadError(f"Invalid schema JSON {path}: {exc}") from exc
        except OSError as exc:
            raise KnowledgeLoadError(f"Unable to read schema {path}: {exc}") from exc
        if not isinstance(payload, dict):
            raise KnowledgeLoadError(f"Schema root must be object: {path}")
        return payload
