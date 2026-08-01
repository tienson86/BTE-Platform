"""Read-only registry loader for the Registry Compiler."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from registry.compiler.constants import (
    AUXILIARY_CATALOGS,
    DOMAIN_CATALOGS,
    ONTOLOGY_ROOT_REL,
    REGISTRY_ROOT_REL,
    SIDECAR_INDEX_NAMES,
)
from registry.compiler.io_utils import read_json, relative_posix, sha256_file

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class LoadedCatalog:
    """A loaded registry catalog or auxiliary JSON document."""

    name: str
    path: str
    kind: str
    version: str
    checksum: str
    payload: dict[str, Any]
    records: list[dict[str, Any]] = field(default_factory=list)


class RegistryLoader:
    """Load registry catalogs and related index sidecars (read-only)."""

    def __init__(self, project_root: Path) -> None:
        """Initialize loader rooted at the BTE project."""
        self.project_root = project_root.resolve()
        self.registry_root = self.project_root / REGISTRY_ROOT_REL
        self.ontology_root = self.project_root / ONTOLOGY_ROOT_REL

    def load_domain_catalogs(self) -> list[LoadedCatalog]:
        """Load the eight primary domain registry containers."""
        catalogs: list[LoadedCatalog] = []
        for rel in DOMAIN_CATALOGS:
            path = self.registry_root / rel
            catalogs.append(self._load_catalog(path, kind="domain_catalog"))
        return catalogs

    def load_auxiliary_catalogs(self) -> list[LoadedCatalog]:
        """Load namespace and object-type registries."""
        catalogs: list[LoadedCatalog] = []
        for rel in AUXILIARY_CATALOGS:
            path = self.registry_root / rel
            catalogs.append(self._load_catalog(path, kind="auxiliary_catalog"))
        return catalogs

    def load_sidecar_indexes(self) -> list[LoadedCatalog]:
        """Load existing domain sidecar index JSON files."""
        catalogs: list[LoadedCatalog] = []
        if not self.registry_root.is_dir():
            return catalogs
        for domain_dir in sorted(self.registry_root.iterdir()):
            if not domain_dir.is_dir():
                continue
            for name in SIDECAR_INDEX_NAMES:
                path = domain_dir / name
                if path.is_file():
                    catalogs.append(self._load_catalog(path, kind="sidecar_index"))
        return catalogs

    def load_ontology(self) -> dict[str, Any]:
        """Load ontology classes and entity types for ontology indexing."""
        result: dict[str, Any] = {
            "classes": [],
            "entity_types": [],
            "relationship_types": [],
            "files": [],
        }
        mapping = {
            "ontology_classes.json": "classes",
            "entity_types.json": "entity_types",
            "relationship_types.json": "relationship_types",
        }
        for filename, key in mapping.items():
            path = self.ontology_root / filename
            entry = {
                "filename": filename,
                "path": relative_posix(path, self.project_root),
                "exists": path.is_file(),
            }
            if path.is_file():
                entry["checksum"] = sha256_file(path)
                payload = read_json(path)
                if key == "classes":
                    result[key] = list(payload.get("classes", []))
                elif key == "entity_types":
                    result[key] = list(payload.get("entity_types", []))
                elif key == "relationship_types":
                    result[key] = list(payload.get("relationship_types", []))
            result["files"].append(entry)
        return result

    def load_all(self) -> dict[str, Any]:
        """Load all compiler inputs."""
        domains = self.load_domain_catalogs()
        auxiliary = self.load_auxiliary_catalogs()
        sidecars = self.load_sidecar_indexes()
        ontology = self.load_ontology()
        logger.info(
            "Loaded %s domain, %s auxiliary, %s sidecar catalogs",
            len(domains),
            len(auxiliary),
            len(sidecars),
        )
        return {
            "domains": domains,
            "auxiliary": auxiliary,
            "sidecars": sidecars,
            "ontology": ontology,
        }

    def _load_catalog(self, path: Path, *, kind: str) -> LoadedCatalog:
        rel = relative_posix(path, self.project_root)
        if not path.is_file():
            logger.warning("Missing registry catalog: %s", rel)
            return LoadedCatalog(
                name=path.stem,
                path=rel,
                kind=kind,
                version="",
                checksum="",
                payload={},
                records=[],
            )
        payload = read_json(path)
        if not isinstance(payload, dict):
            payload = {}
        records = payload.get("records")
        if not isinstance(records, list):
            records = payload.get("entries")
        if not isinstance(records, list):
            records = []
        return LoadedCatalog(
            name=str(payload.get("registry_name") or payload.get("index_name") or path.stem),
            path=rel,
            kind=kind,
            version=str(payload.get("version") or payload.get("schema_version") or "1.0.0"),
            checksum=sha256_file(path),
            payload=payload,
            records=[item for item in records if isinstance(item, dict)],
        )
