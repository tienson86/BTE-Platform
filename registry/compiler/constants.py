"""Constants for the Registry Compiler subsystem."""

from __future__ import annotations

from typing import Final

SCHEMA_VERSION: Final[str] = "1.0.0"
COMPILER_VERSION: Final[str] = "1.0.0"
DEFAULT_TIMESTAMP: Final[str] = "2026-08-01T00:00:00Z"

REGISTRY_ROOT_REL: Final[str] = "knowledge/registry"
GENERATED_ROOT_REL: Final[str] = "knowledge/generated"
ONTOLOGY_ROOT_REL: Final[str] = "knowledge/ontology"

DOMAIN_CATALOGS: Final[tuple[str, ...]] = (
    "global_registry/global_registry.json",
    "knowledge_registry/knowledge_registry.json",
    "rule_registry/rule_registry.json",
    "sentence_registry/sentence_registry.json",
    "reference_registry/reference_registry.json",
    "terminology_registry/terminology_registry.json",
    "dataset_registry/dataset_registry.json",
    "report_registry/report_registry.json",
)

AUXILIARY_CATALOGS: Final[tuple[str, ...]] = (
    "global_registry/namespace_registry.json",
    "global_registry/object_type_registry.json",
)

SIDECAR_INDEX_NAMES: Final[tuple[str, ...]] = (
    "category_index.json",
    "domain_index.json",
    "dependency_index.json",
    "knowledge_link_index.json",
    "sentence_link_index.json",
    "rule_link_index.json",
    "template_index.json",
)

OUTPUT_FILES: Final[tuple[str, ...]] = (
    "registry_index.json",
    "registry_lookup.json",
    "registry_reverse_lookup.json",
    "registry_statistics.json",
    "indexes/id_index.json",
    "indexes/name_index.json",
    "indexes/category_index.json",
    "indexes/ontology_index.json",
    "indexes/dependency_index.json",
    "indexes/relationship_index.json",
    "reports/registry_build_report.md",
    "reports/registry_statistics.md",
    "reports/registry_inventory.md",
    "cache/registry_cache.json",
    "registry_compiler_manifest.json",
)
