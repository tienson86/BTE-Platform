"""Constants for Knowledge Graph Builder V2."""

from __future__ import annotations

from typing import Final

SCHEMA_VERSION: Final[str] = "1.0.0"
BUILDER_VERSION: Final[str] = "2.0.0"
DEFAULT_TIMESTAMP: Final[str] = "2026-08-01T00:00:00Z"
PACK_ID: Final[str] = "PACK_01"

OUTPUT_REL: Final[str] = "knowledge/graph/generated/v2"
RECORDS_REL: Final[str] = "knowledge/bazi/01_fundamental_knowledge/records"
ONTOLOGY_REL: Final[str] = "knowledge/ontology"
REGISTRY_REL: Final[str] = "knowledge/registry"
COMPILER_REL: Final[str] = "knowledge/compiler"

GRAPH_TYPES: Final[tuple[str, ...]] = (
    "academic_graph",
    "ontology_graph",
    "dependency_graph",
    "registry_graph",
    "runtime_graph",
)

EXPORT_FORMATS: Final[tuple[str, ...]] = (
    "json",
    "graphml",
    "dot",
    "mmd",
    "jsonld",
)

# Canonical Pack 01 KR inventory (read-only references).
PACK01_RECORDS: Final[tuple[dict[str, str], ...]] = (
    {"record_id": "KR-000001", "canonical_name": "Yin Yang System", "layer": "Fundamental Principles", "filename": "KR-000001_YIN_YANG.md"},
    {"record_id": "KR-000002", "canonical_name": "Qi System", "layer": "Fundamental Principles", "filename": "KR-000002_QI.md"},
    {"record_id": "KR-000003", "canonical_name": "Wu Xing System", "layer": "Fundamental Principles", "filename": "KR-000003_WU_XING.md"},
    {"record_id": "KR-000004", "canonical_name": "Heavenly Stem System", "layer": "Canonical Entities", "filename": "KR-000004_Heavenly_Stems.md"},
    {"record_id": "KR-000005", "canonical_name": "Earthly Branch System", "layer": "Canonical Entities", "filename": "KR-000005_Earthly_Branches.md"},
    {"record_id": "KR-000006", "canonical_name": "Hidden Stem System", "layer": "Canonical Entities", "filename": "KR-000006_Hidden_Stems_Composition_System.md"},
    {"record_id": "KR-000007", "canonical_name": "Sexagenary Cycle System", "layer": "Canonical Entities", "filename": "KR-000007_Sexagenary_Cycle_Registry.md"},
    {"record_id": "KR-000008", "canonical_name": "Na Yin System", "layer": "Canonical Structures", "filename": "KR-000008_Na_Yin_System.md"},
    {"record_id": "KR-000009", "canonical_name": "Void Branch System", "layer": "Canonical Structures", "filename": "KR-000009_Void_Branch_System.md"},
    {"record_id": "KR-000010", "canonical_name": "Cycle Mapping System", "layer": "Canonical Structures", "filename": "KR-000010_Cycle_Mapping_System.md"},
    {"record_id": "KR-000011", "canonical_name": "Ten Gods System", "layer": "Analytical Foundations", "filename": "KR-000011_Ten_Gods.md"},
    {"record_id": "KR-000012", "canonical_name": "Twelve Growth Phases System", "layer": "Analytical Foundations", "filename": "KR-000012_Twelve_Growth_Phases.md"},
    {"record_id": "KR-000013", "canonical_name": "Shen Sha System", "layer": "Analytical Foundations", "filename": "KR-000013_Shen_Sha_System.md"},
    {"record_id": "KR-000014", "canonical_name": "Stem & Branch Relationship System", "layer": "Analytical Foundations", "filename": "KR-000014_Combination_Clash_System.md"},
    {"record_id": "KR-000015", "canonical_name": "Seasonal Influence & Climate Context System", "layer": "Analytical Foundations", "filename": "KR-000015_Seasonal_Influence_System.md"},
)

ACADEMIC_HARD_DEPS: Final[tuple[tuple[str, str], ...]] = (
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

ACADEMIC_SEMANTIC_DEPS: Final[tuple[tuple[str, str], ...]] = (
    ("KR-000003", "KR-000002"),
    ("KR-000011", "KR-000005"),
    ("KR-000013", "KR-000011"),
    ("KR-000014", "KR-000003"),
    ("KR-000015", "KR-000014"),
)

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

RUNTIME_STAGES: Final[tuple[str, ...]] = (
    "STAGE-LOAD",
    "STAGE-PARSE",
    "STAGE-VALIDATE",
    "STAGE-DEPENDENCY",
    "STAGE-TRANSFORM",
    "STAGE-GENERATE",
    "STAGE-VERIFY",
    "STAGE-PUBLISH",
)
