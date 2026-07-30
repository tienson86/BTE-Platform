"""Registry infrastructure constants."""

from __future__ import annotations

from typing import Final

DEFAULT_REGISTRY_ROOT_RELATIVE: Final[str] = "knowledge/registry"

DOMAIN_REGISTRY_FILES: Final[tuple[str, ...]] = (
    "global_registry/global_registry.json",
    "knowledge_registry/knowledge_registry.json",
    "rule_registry/rule_registry.json",
    "sentence_registry/sentence_registry.json",
    "reference_registry/reference_registry.json",
    "terminology_registry/terminology_registry.json",
    "dataset_registry/dataset_registry.json",
    "report_registry/report_registry.json",
)

REGISTRY_ID_PATTERN: Final[str] = (
    r"^(REG|GREG|KREG|RREG|SREG|TREG|DREG|PREG|REFREG)-[0-9]{6}$"
)

ALLOWED_STATUSES: Final[frozenset[str]] = frozenset(
    {
        "draft",
        "validated",
        "approved",
        "registered",
        "published",
        "deprecated",
        "archived",
    }
)

RECORD_SCHEMA_RELATIVE: Final[str] = "schemas/registry_record.schema.json"
CONTAINER_SCHEMA_RELATIVE: Final[str] = "schemas/registry_container.schema.json"
REGISTRY_INDEX_RELATIVE: Final[str] = "global_registry/registry_index.json"
STATISTICS_RELATIVE: Final[str] = "global_registry/registry_statistics.json"
NAMESPACE_REGISTRY_RELATIVE: Final[str] = "global_registry/namespace_registry.json"
OBJECT_TYPE_REGISTRY_RELATIVE: Final[str] = (
    "global_registry/object_type_registry.json"
)

SEMVER_PATTERN: Final[str] = r"^[0-9]+\.[0-9]+\.[0-9]+$"
