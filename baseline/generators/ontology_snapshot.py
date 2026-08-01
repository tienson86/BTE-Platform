"""Ontology snapshot generator."""

from __future__ import annotations

from typing import Any

from baseline.constants import SCHEMA_VERSION
from baseline.models import BuildContext


def generate_ontology_snapshot(
    context: BuildContext,
    ontology: dict[str, Any],
) -> dict[str, Any]:
    """Generate ontology snapshot from discovered ontology inventory."""
    classes = ontology.get("classes", [])
    entity_types = ontology.get("entity_types", [])
    semantic_categories = sorted(
        {
            str(item.get("canonical_name") or item.get("id") or "")
            for item in classes
            if item.get("canonical_name") or item.get("id")
        }
    )
    canonical_object_types = sorted(
        {
            str(item.get("canonical_name") or item.get("id") or "")
            for item in entity_types
            if item.get("canonical_name") or item.get("id")
        }
    )
    return {
        "artifact": "ontology_snapshot",
        "schema_version": SCHEMA_VERSION,
        "pack_id": context.pack_id,
        "version": context.version,
        "timestamp": context.timestamp,
        "ontology_classes": classes,
        "ontology_hierarchy": ontology.get("hierarchy", []),
        "semantic_categories": semantic_categories,
        "canonical_object_types": canonical_object_types,
        "relationship_types": ontology.get("relationship_types", []),
        "node_types": ontology.get("node_types", []),
        "edge_types": ontology.get("edge_types", []),
        "semantic_levels": ontology.get("semantic_levels", []),
        "files": ontology.get("files", []),
        "ontology_statistics": ontology.get("statistics", {}),
    }
