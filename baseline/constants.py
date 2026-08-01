"""Constants for Pack 01 baseline generation."""

from __future__ import annotations

from typing import Final

PACK_ID: Final[str] = "PACK_01"
PACK_NAME: Final[str] = "Pack 01 — Fundamental Theory"
PACK_CLASSIFICATION: Final[str] = "Golden Foundation Pack"
BASELINE_VERSION: Final[str] = "1.0.0"
SCHEMA_VERSION: Final[str] = "1.0.0"
DEFAULT_BUILD_TIMESTAMP: Final[str] = "2026-08-01T00:00:00Z"

RECORDS_REL_DIR: Final[str] = "knowledge/bazi/01_fundamental_knowledge/records"
ONTOLOGY_REL_DIR: Final[str] = "knowledge/ontology"
REGISTRY_REL_DIR: Final[str] = "knowledge/registry"
COMPILER_REL_DIR: Final[str] = "knowledge/compiler"
VALIDATION_REL_DIR: Final[str] = "knowledge/validation"
GRAPH_REL_DIR: Final[str] = "knowledge/graph"
DEPENDENCY_REL_DIR: Final[str] = "knowledge/dependency"
GOVERNANCE_REL_DIR: Final[str] = "knowledge/governance"

BASELINE_OUTPUT_REL_DIR: Final[str] = "knowledge/baseline"
GOVERNANCE_GENERATED_REL_DIR: Final[str] = "knowledge/governance/generated"
COMPILER_GENERATED_REL_DIR: Final[str] = "knowledge/compiler/generated"
VALIDATION_GENERATED_REL_DIR: Final[str] = "knowledge/validation/generated"
GRAPH_GENERATED_REL_DIR: Final[str] = "knowledge/graph/generated"

REGISTRY_DOMAINS: Final[tuple[str, ...]] = (
    "global_registry",
    "knowledge_registry",
    "rule_registry",
    "sentence_registry",
    "reference_registry",
    "terminology_registry",
    "dataset_registry",
    "report_registry",
)

ONTOLOGY_DATA_FILES: Final[tuple[str, ...]] = (
    "ontology_classes.json",
    "entity_types.json",
    "relationship_types.json",
    "relationship_constraints.json",
    "property_definitions.json",
    "node_types.json",
    "edge_types.json",
    "semantic_levels.json",
    "namespace_registry.json",
)

COMPILER_DATA_FILES: Final[tuple[str, ...]] = (
    "pipeline.json",
    "stage_registry.json",
    "compiler_config.json",
    "artifact_registry.json",
    "plugin_registry.json",
    "error_registry.json",
    "version_registry.json",
    "compiler.schema.json",
    "statistics.json",
)

VALIDATION_DATA_FILES: Final[tuple[str, ...]] = (
    "validation_schema.json",
    "record_validator.json",
    "ontology_validator.json",
    "registry_validator.json",
    "relationship_validator.json",
    "dependency_validator.json",
    "metadata_validator.json",
    "compiler_validation.json",
)

# Canonical Pack 01 inventory (authoritative per PACK_01_MANIFEST).
PACK01_KR_INVENTORY: Final[tuple[dict[str, str], ...]] = (
    {
        "record_id": "KR-000001",
        "canonical_name": "Yin Yang System",
        "pattern": "Principle",
        "filename": "KR-000001_YIN_YANG.md",
        "layer": "Fundamental Principles",
    },
    {
        "record_id": "KR-000002",
        "canonical_name": "Qi System",
        "pattern": "Principle",
        "filename": "KR-000002_QI.md",
        "layer": "Fundamental Principles",
    },
    {
        "record_id": "KR-000003",
        "canonical_name": "Wu Xing System",
        "pattern": "Principle",
        "filename": "KR-000003_WU_XING.md",
        "layer": "Fundamental Principles",
    },
    {
        "record_id": "KR-000004",
        "canonical_name": "Heavenly Stem System",
        "pattern": "Entity",
        "filename": "KR-000004_Heavenly_Stems.md",
        "layer": "Canonical Entities",
    },
    {
        "record_id": "KR-000005",
        "canonical_name": "Earthly Branch System",
        "pattern": "Entity",
        "filename": "KR-000005_Earthly_Branches.md",
        "layer": "Canonical Entities",
    },
    {
        "record_id": "KR-000006",
        "canonical_name": "Hidden Stem System",
        "pattern": "Composition",
        "filename": "KR-000006_Hidden_Stems_Composition_System.md",
        "layer": "Canonical Entities",
    },
    {
        "record_id": "KR-000007",
        "canonical_name": "Sexagenary Cycle System",
        "pattern": "Composite Entity",
        "filename": "KR-000007_Sexagenary_Cycle_Registry.md",
        "layer": "Canonical Entities",
    },
    {
        "record_id": "KR-000008",
        "canonical_name": "Na Yin System",
        "pattern": "Classification",
        "filename": "KR-000008_Na_Yin_System.md",
        "layer": "Canonical Structures",
    },
    {
        "record_id": "KR-000009",
        "canonical_name": "Void Branch System",
        "pattern": "Resolution",
        "filename": "KR-000009_Void_Branch_System.md",
        "layer": "Canonical Structures",
    },
    {
        "record_id": "KR-000010",
        "canonical_name": "Cycle Mapping System",
        "pattern": "Infrastructure",
        "filename": "KR-000010_Cycle_Mapping_System.md",
        "layer": "Canonical Structures",
    },
    {
        "record_id": "KR-000011",
        "canonical_name": "Ten Gods System",
        "pattern": "Derivation",
        "filename": "KR-000011_Ten_Gods.md",
        "layer": "Analytical Foundations",
    },
    {
        "record_id": "KR-000012",
        "canonical_name": "Twelve Growth Phases System",
        "pattern": "State Derivation",
        "filename": "KR-000012_Twelve_Growth_Phases.md",
        "layer": "Analytical Foundations",
    },
    {
        "record_id": "KR-000013",
        "canonical_name": "Shen Sha System",
        "pattern": "Composite Rule",
        "filename": "KR-000013_Shen_Sha_System.md",
        "layer": "Analytical Foundations",
    },
    {
        "record_id": "KR-000014",
        "canonical_name": "Stem & Branch Relationship System",
        "pattern": "Relationship",
        "filename": "KR-000014_Combination_Clash_System.md",
        "layer": "Analytical Foundations",
    },
    {
        "record_id": "KR-000015",
        "canonical_name": "Seasonal Influence & Climate Context System",
        "pattern": "Context",
        "filename": "KR-000015_Seasonal_Influence_System.md",
        "layer": "Analytical Foundations",
    },
)

# Academic hard dependencies for Pack 01 foundation layering.
# Edges are (source, target) meaning source depends on target.
PACK01_ACADEMIC_HARD_DEPS: Final[tuple[tuple[str, str], ...]] = (
    ("KR-000002", "KR-000001"),
    ("KR-000003", "KR-000001"),
    ("KR-000004", "KR-000001"),
    ("KR-000004", "KR-000003"),
    ("KR-000005", "KR-000001"),
    ("KR-000005", "KR-000003"),
    ("KR-000006", "KR-000004"),
    ("KR-000006", "KR-000005"),
    ("KR-000007", "KR-000004"),
    ("KR-000007", "KR-000005"),
    ("KR-000008", "KR-000003"),
    ("KR-000008", "KR-000007"),
    ("KR-000009", "KR-000007"),
    ("KR-000010", "KR-000004"),
    ("KR-000010", "KR-000005"),
    ("KR-000010", "KR-000007"),
    ("KR-000011", "KR-000001"),
    ("KR-000011", "KR-000003"),
    ("KR-000011", "KR-000004"),
    ("KR-000012", "KR-000003"),
    ("KR-000012", "KR-000005"),
    ("KR-000013", "KR-000004"),
    ("KR-000013", "KR-000005"),
    ("KR-000013", "KR-000007"),
    ("KR-000014", "KR-000004"),
    ("KR-000014", "KR-000005"),
    ("KR-000015", "KR-000003"),
    ("KR-000015", "KR-000005"),
)

PACK01_SEMANTIC_DEPS: Final[tuple[tuple[str, str], ...]] = (
    ("KR-000003", "KR-000002"),
    ("KR-000011", "KR-000005"),
    ("KR-000013", "KR-000011"),
    ("KR-000014", "KR-000003"),
    ("KR-000015", "KR-000014"),
)

SNAPSHOT_FILENAMES: Final[tuple[str, ...]] = (
    "baseline_manifest.json",
    "ontology_snapshot.json",
    "registry_snapshot.json",
    "dependency_snapshot.json",
    "compiler_snapshot.json",
    "validation_snapshot.json",
    "knowledge_graph.json",
    "knowledge_graph.graphml",
    "knowledge_graph.dot",
    "knowledge_graph.mmd",
    "governance_metadata.json",
    "compiler_validation_report.json",
    "ontology_validation_report.json",
    "registry_validation_report.json",
    "graph_validation_report.json",
    "build_report.md",
    "validation_report.md",
    "release_candidate.md",
    "freeze_readiness.md",
    "checksums.json",
    "statistics.json",
    "release_manifest.json",
    "release_metadata.json",
    "release_artifacts.json",
    "release_inventory.json",
    "freeze_inventory.json",
    "known_issues.json",
)
