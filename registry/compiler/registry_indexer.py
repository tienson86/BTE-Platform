"""Registry indexer building compiler-ready indexes."""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any

from registry.compiler.registry_loader import LoadedCatalog

logger = logging.getLogger(__name__)


class RegistryIndexer:
    """Build deterministic ID/name/category/ontology/dependency/relationship indexes."""

    def build_all(
        self,
        domains: list[LoadedCatalog],
        auxiliary: list[LoadedCatalog],
        sidecars: list[LoadedCatalog],
        ontology: dict[str, Any],
    ) -> dict[str, Any]:
        """Build all required indexes and lookup tables."""
        objects = self._collect_objects(domains, auxiliary, sidecars)
        id_index = self._build_id_index(objects)
        name_index = self._build_name_index(objects)
        category_index = self._build_category_index(objects, sidecars)
        ontology_index = self._build_ontology_index(ontology, auxiliary)
        dependency_index = self._build_dependency_index(objects, sidecars)
        relationship_index = self._build_relationship_index(objects, ontology)

        lookup = {
            object_id: {
                "object_id": object_id,
                "canonical_name": item.get("canonical_name", ""),
                "registry": item.get("registry", ""),
                "category": item.get("category", ""),
                "kind": item.get("kind", ""),
                "path": item.get("path", ""),
            }
            for object_id, item in sorted(id_index.items())
        }
        reverse_lookup: dict[str, list[str]] = defaultdict(list)
        for object_id, item in sorted(lookup.items()):
            name = str(item.get("canonical_name") or "").strip().lower()
            if name:
                reverse_lookup[name].append(object_id)
            registry = str(item.get("registry") or "").strip().lower()
            if registry:
                reverse_lookup[f"registry:{registry}"].append(object_id)

        indexes = {
            "id_index": id_index,
            "name_index": name_index,
            "category_index": category_index,
            "ontology_index": ontology_index,
            "dependency_index": dependency_index,
            "relationship_index": relationship_index,
        }
        logger.info(
            "Built indexes: ids=%s names=%s categories=%s",
            len(id_index),
            len(name_index),
            len(category_index),
        )
        return {
            "objects": objects,
            "indexes": indexes,
            "lookup": lookup,
            "reverse_lookup": {
                key: sorted(values) for key, values in sorted(reverse_lookup.items())
            },
        }

    def _collect_objects(
        self,
        domains: list[LoadedCatalog],
        auxiliary: list[LoadedCatalog],
        sidecars: list[LoadedCatalog],
    ) -> list[dict[str, Any]]:
        objects: list[dict[str, Any]] = []

        for catalog in domains:
            objects.append(
                {
                    "object_id": f"REGDOM-{catalog.name}",
                    "canonical_name": catalog.name,
                    "registry": catalog.name,
                    "category": "registry_domain",
                    "kind": "registry_domain",
                    "path": catalog.path,
                    "version": catalog.version,
                    "checksum": catalog.checksum,
                    "record_count": len(catalog.records),
                    "dependencies": [],
                    "relationships": [],
                    "ontology_refs": [],
                }
            )
            for record in catalog.records:
                objects.append(self._normalize_record(record, catalog))

        for catalog in auxiliary:
            for record in catalog.records:
                objects.append(self._normalize_auxiliary(record, catalog))

        for catalog in sidecars:
            for entry in catalog.records:
                objects.append(self._normalize_sidecar_entry(entry, catalog))

        return objects

    def _normalize_record(
        self,
        record: dict[str, Any],
        catalog: LoadedCatalog,
    ) -> dict[str, Any]:
        identity = record.get("identity") if isinstance(record.get("identity"), dict) else {}
        classification = (
            record.get("classification")
            if isinstance(record.get("classification"), dict)
            else {}
        )
        object_id = str(
            identity.get("registry_id")
            or identity.get("object_id")
            or record.get("id")
            or record.get("record_id")
            or ""
        )
        return {
            "object_id": object_id or f"ANON-{catalog.name}-{len(record)}",
            "canonical_name": str(
                identity.get("canonical_name")
                or record.get("canonical_name")
                or object_id
            ),
            "registry": catalog.name,
            "category": str(
                classification.get("category")
                or record.get("category")
                or "uncategorized"
            ),
            "kind": "registry_record",
            "path": catalog.path,
            "version": str(identity.get("version") or catalog.version),
            "checksum": "",
            "record_count": 1,
            "dependencies": list(record.get("dependencies") or []),
            "relationships": list(record.get("relationships") or []),
            "ontology_refs": list(
                record.get("ontology_refs")
                or record.get("ontology_class_ids")
                or []
            ),
        }

    def _normalize_auxiliary(
        self,
        record: dict[str, Any],
        catalog: LoadedCatalog,
    ) -> dict[str, Any]:
        if "namespace" in record:
            object_id = f"NS-{record.get('namespace')}"
            name = str(record.get("namespace"))
            category = "namespace"
        elif "object_type" in record:
            object_id = f"OTYPE-{record.get('object_type')}"
            name = str(record.get("object_type"))
            category = "object_type"
        else:
            object_id = str(record.get("id") or f"AUX-{catalog.name}")
            name = object_id
            category = "auxiliary"
        return {
            "object_id": object_id,
            "canonical_name": name,
            "registry": catalog.name,
            "category": category,
            "kind": "auxiliary_record",
            "path": catalog.path,
            "version": catalog.version,
            "checksum": "",
            "record_count": 1,
            "dependencies": [],
            "relationships": [],
            "ontology_refs": [],
            "prefix": record.get("prefix") or record.get("object_id_prefix") or "",
            "namespace": record.get("namespace") or "",
        }

    def _normalize_sidecar_entry(
        self,
        entry: dict[str, Any],
        catalog: LoadedCatalog,
    ) -> dict[str, Any]:
        object_id = str(
            entry.get("id")
            or entry.get("key")
            or entry.get("registry_id")
            or f"SIDE-{catalog.name}"
        )
        return {
            "object_id": object_id,
            "canonical_name": str(entry.get("name") or entry.get("key") or object_id),
            "registry": catalog.name,
            "category": str(entry.get("category") or catalog.name),
            "kind": "sidecar_entry",
            "path": catalog.path,
            "version": catalog.version,
            "checksum": "",
            "record_count": 1,
            "dependencies": list(entry.get("dependencies") or entry.get("depends_on") or []),
            "relationships": list(entry.get("relationships") or []),
            "ontology_refs": list(entry.get("ontology_refs") or []),
        }

    def _build_id_index(self, objects: list[dict[str, Any]]) -> dict[str, Any]:
        index: dict[str, Any] = {}
        for item in objects:
            object_id = str(item.get("object_id") or "")
            if not object_id:
                continue
            index[object_id] = item
        return dict(sorted(index.items()))

    def _build_name_index(self, objects: list[dict[str, Any]]) -> dict[str, Any]:
        index: dict[str, list[str]] = defaultdict(list)
        for item in objects:
            name = str(item.get("canonical_name") or "").strip()
            object_id = str(item.get("object_id") or "")
            if name and object_id:
                index[name].append(object_id)
        return {key: sorted(set(values)) for key, values in sorted(index.items())}

    def _build_category_index(
        self,
        objects: list[dict[str, Any]],
        sidecars: list[LoadedCatalog],
    ) -> dict[str, Any]:
        index: dict[str, list[str]] = defaultdict(list)
        for item in objects:
            category = str(item.get("category") or "uncategorized")
            object_id = str(item.get("object_id") or "")
            if object_id:
                index[category].append(object_id)
        for catalog in sidecars:
            if catalog.name == "category_index" or catalog.path.endswith(
                "category_index.json"
            ):
                for entry in catalog.records:
                    key = str(entry.get("key") or entry.get("category") or "")
                    ids = entry.get("registry_ids") or entry.get("ids") or []
                    if key and isinstance(ids, list):
                        index[key].extend(str(item) for item in ids)
        return {key: sorted(set(values)) for key, values in sorted(index.items())}

    def _build_ontology_index(
        self,
        ontology: dict[str, Any],
        auxiliary: list[LoadedCatalog],
    ) -> dict[str, Any]:
        classes = {
            str(item.get("id")): {
                "id": item.get("id"),
                "canonical_name": item.get("canonical_name"),
                "parent_class": item.get("parent_class"),
            }
            for item in ontology.get("classes", [])
            if item.get("id")
        }
        entity_types = []
        for item in ontology.get("entity_types", []):
            entity_types.append(
                {
                    "id": item.get("id"),
                    "canonical_name": item.get("canonical_name"),
                    "ontology_class_id": item.get("ontology_class_id"),
                }
            )
        object_types = []
        for catalog in auxiliary:
            if "object_type" in catalog.name:
                for record in catalog.records:
                    object_types.append(
                        {
                            "object_type": record.get("object_type"),
                            "namespace": record.get("namespace"),
                            "object_id_prefix": record.get("object_id_prefix"),
                        }
                    )
        return {
            "classes": dict(sorted(classes.items())),
            "entity_types": entity_types,
            "registry_object_types": object_types,
            "statistics": {
                "class_count": len(classes),
                "entity_type_count": len(entity_types),
                "registry_object_type_count": len(object_types),
            },
        }

    def _build_dependency_index(
        self,
        objects: list[dict[str, Any]],
        sidecars: list[LoadedCatalog],
    ) -> dict[str, Any]:
        edges: list[dict[str, Any]] = []
        for item in objects:
            source = str(item.get("object_id") or "")
            deps = item.get("dependencies") or []
            if isinstance(deps, list):
                for dep in deps:
                    if isinstance(dep, str):
                        edges.append(
                            {
                                "source": source,
                                "target": dep,
                                "level": "depends_on",
                            }
                        )
                    elif isinstance(dep, dict):
                        target = str(
                            dep.get("target")
                            or dep.get("registry_id")
                            or dep.get("object_id")
                            or ""
                        )
                        if target:
                            edges.append(
                                {
                                    "source": source,
                                    "target": target,
                                    "level": str(dep.get("level") or "depends_on"),
                                }
                            )
        for catalog in sidecars:
            if catalog.path.endswith("dependency_index.json"):
                for entry in catalog.records:
                    source = str(entry.get("source") or entry.get("key") or "")
                    target = str(entry.get("target") or "")
                    if source and target:
                        edges.append(
                            {
                                "source": source,
                                "target": target,
                                "level": str(entry.get("level") or "depends_on"),
                            }
                        )
        # Domain load-order dependencies for compiler readiness.
        domain_order = [
            item["object_id"]
            for item in objects
            if item.get("kind") == "registry_domain"
        ]
        for idx in range(1, len(domain_order)):
            edges.append(
                {
                    "source": domain_order[idx],
                    "target": domain_order[idx - 1],
                    "level": "load_order",
                }
            )
        return {
            "edge_count": len(edges),
            "edges": edges,
        }

    def _build_relationship_index(
        self,
        objects: list[dict[str, Any]],
        ontology: dict[str, Any],
    ) -> dict[str, Any]:
        relationships: list[dict[str, Any]] = []
        for item in objects:
            source = str(item.get("object_id") or "")
            for rel in item.get("relationships") or []:
                if isinstance(rel, dict):
                    relationships.append(
                        {
                            "source": source,
                            "target": rel.get("target") or rel.get("object_id"),
                            "type": rel.get("type") or rel.get("relationship"),
                        }
                    )
        for rel_type in ontology.get("relationship_types", []):
            relationships.append(
                {
                    "source": "ONTOLOGY",
                    "target": rel_type.get("id"),
                    "type": "DECLARES_RELATIONSHIP_TYPE",
                    "canonical_name": rel_type.get("canonical_name"),
                }
            )
        return {
            "relationship_count": len(relationships),
            "relationships": relationships,
        }
